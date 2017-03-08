	-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'logistics_stop'
-- This is the table that will hold each stop along the way for a route
-- ---

DROP TABLE IF EXISTS `logistics_stop`;
		
CREATE TABLE `logistics_stop` (
  `id` VARCHAR(200) NOT NULL DEFAULT 'NULL' COMMENT 'This is a combination of the routeMain and routeStop ids',
  `route_id` VARCHAR(200) NULL DEFAULT NULL,
  `route_start_date` DATE NULL,
  `route_end_date` DATE NULL,
  `misc_expenses` INTEGER NULL DEFAULT NULL,
  `total_miles` INTEGER NULL DEFAULT NULL,
  `operator_name` VARCHAR(300) NULL DEFAULT NULL,
  `operator_pay` INTEGER NULL DEFAULT NULL,
  `customer_name` VARCHAR(300) NULL DEFAULT NULL,
  `ship_to` VARCHAR(300) NULL DEFAULT NULL,
  `customer_zip` INTEGER NULL DEFAULT NULL,
  `miles_from_company` INTEGER NULL DEFAULT NULL,
  `customer_cost` DECIMAL(10,5) NULL DEFAULT NULL,
  `percent_load` DECIMAL(10,5) NULL DEFAULT NULL,
  `pallets` INTEGER NULL DEFAULT NULL,
  `carts` INTEGER NULL DEFAULT NULL,
  `percent_of_total` DECIMAL(10,5) NULL DEFAULT NULL COMMENT 'This should be the miles from company divided by the total m',
  `stop_miles` DECIMAL(10,5) NULL DEFAULT NULL,
  `stop_operator_pay` DECIMAL(10,5) NULL DEFAULT NULL,
  `stop_misc` DECIMAL(10,5) NULL DEFAULT NULL,
  `percent_freight` DECIMAL(10,5) NULL DEFAULT NULL,
  `cost_per_mile` DECIMAL(10,5) NULL DEFAULT NULL,
  `revenue_per_mile` DECIMAL(10,5) NULL DEFAULT NULL,
  `invoice_num` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT 'This is the table that will hold each stop along the way for';

-- ---
-- Foreign Keys 
-- ---


-- ---
-- Table Properties
-- ---

-- ALTER TABLE `logistics_stop` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `logistics_stop` (`id`,`route_start_date`,`route_end_date`,`hotel_expenses`,`fuel_expenses`,`fuel_gallons`,`total_miles`,`total_hours`,`operator_name`,`operator_pay`,`customer_name`,`ship_to`,`customer_zip`,`miles_from_company`,`customer_cost`,`percent_load`,`pallets`,`carts`,`returned_carts`,`percent_of_total`,`stop_miles`,`stop_hours`,`stop_fuel_gallons`,`stop_operator_pay`,`stop_hotel`,`stop_fuel`,`percent_freight`,`fuel_rate`,`cost_per_mile`,`revenue_per_mile`) VALUES
-- ('','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');

