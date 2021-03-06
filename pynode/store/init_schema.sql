CREATE DATABASE IF NOT EXISTS pynode;

USE pynode;

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- explanation: https://stackoverflow.com/questions/6265891/sql-syntax-what-is-this
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pynode`
--

-- --------------------------------------------------------

--
-- Table structure for table `edge`
--

CREATE TABLE IF NOT EXISTS `edge` (
  `from_node_id` bigint(36) unsigned NOT NULL,
  `to_node_id` bigint(36) unsigned NOT NULL,
  `type` bigint(36) unsigned NOT NULL,
  `seq` bigint(36) unsigned NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`from_node_id`,`to_node_id`,`type`),
  KEY `from_type_seq` (`from_node_id`,`type`,`seq`),
  KEY `to_node_id` (`to_node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `node`
--

CREATE TABLE IF NOT EXISTS `node` (
  `id` bigint(36) unsigned NOT NULL AUTO_INCREMENT,
  `type` bigint(36) unsigned NOT NULL,
  `data` text COLLATE utf8_unicode_ci NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `type_updated` (`type`,`updated`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1000000;

-- --------------------------------------------------------

--
-- Table structure for table `node_data`
--

CREATE TABLE IF NOT EXISTS `node_data` (
  `node_id` bigint(36) unsigned NOT NULL,
  `type` bigint(36) unsigned NOT NULL,
  `data` text COLLATE utf8_unicode_ci NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`node_id`,`type`),
  KEY `type_data` (`type`,`data`(128)),
  KEY `type_updated` (`type`,`updated`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Constraints for dumped tables
-- TODO savil: remove these constraints. We don't want FOREIGN KEY in the DB.
-- When we want to shard these FOREIGN KEYs will prevent us from doing so.
--

--
-- Constraints for table `edge`
--
ALTER TABLE `edge`
  ADD CONSTRAINT `edge_ibfk_2` FOREIGN KEY (`to_node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `edge_ibfk_1` FOREIGN KEY (`from_node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `node_data`
--
ALTER TABLE `node_data`
  ADD CONSTRAINT `node_data_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
