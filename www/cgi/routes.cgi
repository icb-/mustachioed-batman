#!/usr/bin/perl -T

use warnings;
use strict;
use utf8;
use DBI;
use CGI;
use JSON;
use Data::Dumper;

my $config_file = $ENV{RTBH_CONF};
if($config_file =~ m/^([0-9a-z_.]+)\z/)
{ # Untaint
	$config_file = $1;
}

my $config;
{ # Grab config
	local $/;
	open(my $fh, '<', $config_file);
	$config = decode_json(<$fh>);
	close($fh);
}

my $cgi = new CGI();
my $version = $cgi->param('version') || '4';
if($version =~ m/^([46])$/)
{ # Untaint
	$version = $1;
}
else { die 'Untaint $version'; }

my $hop = $cgi->param('hop');
if($hop =~ m/^([0-9a-zA-Z:.]+)$/)
{ # Untaint
	$hop = $1;
}

# Connect to DB
my $dbh = DBI->connect("DBI:mysql:host=$config->{database}{host};database=$config->{database}{database}", $config->{database}{username}, $config->{database}{password}) || die "Could not connect to database: $DBI::errstr";

my $sth = $dbh->prepare("select * from route where route.end_epoch > ? and route.start_epoch < ? and route.version = ?");

my $now = time;
my @routes;

$sth->execute($now, $now, $version);

while (my $row = $sth->fetchrow_hashref())
{
	push(@routes, "route $row->{addr}/$row->{subnet} next-hop $hop");
}

print $cgi->header(-type => 'text/json', -charset => 'utf-8');

print encode_json(\@routes);
