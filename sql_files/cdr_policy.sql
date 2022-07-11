CREATE DATABASE  IF NOT EXISTS `cdr` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `cdr`;

--
-- Table structure for table `policy`
--

DROP TABLE IF EXISTS `policy`;
CREATE TABLE `policy` (
  `id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Details` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `policy` WRITE;
/*!40000 ALTER TABLE `policy` DISABLE KEYS */;
INSERT INTO `policy` VALUES (1,'Very Strict ','Block any suspicius email and send an alert.'),(2,'Strict','Remove any URLs and attachments.'),(3,'strict filtering','Filtering any URLs and known problematic file types Attachments.'),(4,'Blocklist filtering','Filtering URLs for known blacklist sites and known problematic file types.'),(5,'Alert policy','Add an alert on any possible threat'),(6,'None','Not filtering at all.');
/*!40000 ALTER TABLE `policy` ENABLE KEYS */;
UNLOCK TABLES;