DROP TABLE IF EXISTS `Sessions`;
CREATE TABLE `Sessions` (
    `session_id` VARCHAR(128) UNIQUE NOT NULL,
    `atime` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    `data` TEXT
);

DROP TABLE IF EXISTS `Users`;
CREATE TABLE `Users`
(
    `username` VARCHAR(20),
    `password` VARCHAR(20),
    PRIMARY KEY(`username`)
);

DROP TABLE IF EXISTS `AuthorizedAPs`;
CREATE TABLE `AuthorizedAPs`
(
    `bssid` CHAR(17),
    `ssid` VARCHAR(30),
    `channel` TINYINT,
    `vendor` VARCHAR(20),
    `location` VARCHAR(30),
    `route` VARCHAR(30), 
    PRIMARY KEY(`bssid`)
);

DROP TABLE IF EXISTS `APsFeatures`;
CREATE TABLE `APsFeatures`
(
    `bssid` CHAR(17),
    `ssid` VARCHAR(30),
    `channel` TINYINT,
    `vendor` VARCHAR(20),
    `location` VARCHAR(30),
    `security` VARCHAR(20),
    `signal` SMALLINT,
    `noise` SMALLINT,
    `route` VARCHAR(30),
    PRIMARY KEY(`bssid`)
);

DROP TABLE IF EXISTS `APsCredit`;
CREATE TABLE `APsCredit`
(
    `bssid` CHAR(17),
    `credit` TINYINT,
    PRIMARY KEY(`bssid`)
);

DROP TABLE IF EXISTS `APsRTTEvals`;
CREATE TABLE `APsRTTEvals`
(
    `bssid` CHAR(17),
    `rtt_probelist` VARCHAR(500),
    `RTT_dnslist` VARCHAR(500),
    `mean_probe` NUMERIC(5,5),
    `mean_dns` NUMERIC(5,5),
    `dev_probe` NUMERIC(5,5),
    `dev_dns` NUMERIC(5,5),
    `rtt_eval` NUMERIC(5,5),
    PRIMARY KEY(`bssid`)
)
