CREATE DATABASE  IF NOT EXISTS `cdr` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `cdr`;

-- Table structure for table `mailbox`
--

DROP TABLE IF EXISTS `mailbox`;
CREATE TABLE `mailbox` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(45) NOT NULL,
  `LastName` varchar(45) NOT NULL,
  `MailBoxName` varchar(45) NOT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `Role` varchar(45) DEFAULT NULL,
  `PolicyID` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`ID`),
  KEY `id_idx` (`PolicyID`),
  KEY `policyNum_idx` (`PolicyID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
