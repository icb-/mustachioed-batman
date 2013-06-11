#!/usr/bin/env python

import os
import sys
import signal
import time
import urllib
#from sets import Set
import json
import getopt
import logging
import logging.config

config_file = "/etc/rtbh/config.json"
reconfig = True
routes = set([])
config = None
logger = None

def load_config():
	global config
	f=open(config_file, 'r')
	config = json.load(f)
	f.close()

def setup_logging():
	global logger
	logging.config.fileConfig(config['log'])
	logger = logging.getLogger('RTBH')

def main():
	global routes
	global config
	global reconfig

	load_config()

	# Signal handling
	## Translate SIGINT, SIGTERM to SIGKILL
	def sig (signum, frame):
		os.kill(os.getpid(),signal.SIGKILL)
	signal.signal(signal.SIGINT, sig)
	signal.signal(signal.SIGTERM, sig)

	## Reload config on SIGHUP
	def sig_reconfig(signum, frame):
		global reconfig
		global logger
		logger.debug("SIGHUP received; queuing config reload")
		reconfig = True
	signal.signal(signal.SIGHUP, sig_reconfig)

	setup_logging()

	while True:
		now = time.time()
		if reconfig:
			logger.info("Reloading Config")
			load_config()
			logger.debug("Loaded: %s" %config)
			reconfig = False
		try:
			was = len(routes)
			f=urllib.urlopen(config['url'])
			s = set(json.load(f))
			f.close()
			toAdd = s-routes
			toDel = routes-s
			routes = s
			for r in toAdd:
				logger.debug('Announcing: %s' %r)
				sys.stdout.write('announce %s\n' % r)
			sys.stdout.flush()
			for r in toDel:
				logger.debug('Withdrawing: %s' %r)
				sys.stdout.write('withdraw %s\n' %r)
			sys.stdout.flush()
			logger.info("Route count: was %d, now %d" %(was, len(routes)))
		except Exception, e:
			logger.error("Something went bad... %s" %e)
			sys.stderr.flush()
		took = (time.time() - now)
		sleeptime = max(0,30-took)
		logger.info("Took %2.1f seconds; Sleeping %2.1f seconds"%(took, sleeptime))
		time.sleep(sleeptime)

if __name__ == "__main__":
	main()
