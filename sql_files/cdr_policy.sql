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
