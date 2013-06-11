DROP TABLE IF EXISTS `route`;
CREATE TABLE `route` (
  `route_id` int(11) NOT NULL AUTO_INCREMENT,
  `start_epoch` int(11) NOT NULL,
  `end_epoch` int(11) NOT NULL,
  `version` enum('4','6') NOT NULL,
  `addr` varchar(45) NOT NULL,
  `subnet` int(3) NOT NULL,
  PRIMARY KEY (`route_id`),
  UNIQUE KEY `start_epoch` (`start_epoch`,`end_epoch`,`version`,`addr`,`subnet`),
  KEY `start_epoch_2` (`start_epoch`,`end_epoch`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
