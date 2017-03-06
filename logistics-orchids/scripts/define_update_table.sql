-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'last_update'
-- This table tracks when the last time a table was updated
-- ---

DROP TABLE IF EXISTS `last_update`;
		
CREATE TABLE `last_update` (
  `id` INTEGER AUTO_INCREMENT,
  `item_name` VARCHAR(50) DEFAULT 'basic',
  `item_first_load` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `item_last_load` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) COMMENT 'This table tracks when the last time a table was updated';

-- ---
-- Foreign Keys 
-- ---


-- ---
-- Table Properties
-- ---

-- ALTER TABLE `last_update` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `last_update` (`id`,`item_name`,`item_first_load`,`item_last_load`) VALUES
-- ('','','','');

INSERT INTO last_update (item_name) VALUES ('logistics_app');