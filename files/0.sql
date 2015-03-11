SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `settings`;
CREATE TABLE IF NOT EXISTS `settings` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `value` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE IF NOT EXISTS `customers` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `first_name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `last_name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `full_name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `address` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    INDEX `first_name` (`first_name`),
    INDEX `last_name` (`last_name`),
    INDEX `full_name` (`full_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `type` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `role` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `vendor` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `version` INT(11) UNSIGNED NOT NULL,
    `attempts` INT(11) UNSIGNED NOT NULL,
    `currency` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `language` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `payment_method` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `amounts_account` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_order` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_shipping` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_tax` DECIMAL(20,2) UNSIGNED NOT NULL,
    `receipt` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `timestamp` DATETIME NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `orders_products`;
CREATE TABLE IF NOT EXISTS `orders_products` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` INT(11) UNSIGNED NOT NULL,
    `title` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `amount` DECIMAL(20,2) UNSIGNED NOT NULL,
    `item_number` INT(11) UNSIGNED NOT NULL,
    `recurring` BOOLEAN NOT NULL,
    `shippable` BOOLEAN NOT NULL,
    `url` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `orders_products_order_id`
        FOREIGN KEY (`order_id`)
        REFERENCES `orders` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE KEY `order_id_item_number` (`order_id`, `item_number`),
    INDEX `order_id` (`order_id`),
    INDEX `title` (`title`),
    INDEX `amount` (`amount`),
    INDEX `item_number` (`item_number`),
    INDEX `recurring` (`recurring`),
    INDEX `shippable` (`shippable`),
    INDEX `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

SET FOREIGN_KEY_CHECKS = 1;
