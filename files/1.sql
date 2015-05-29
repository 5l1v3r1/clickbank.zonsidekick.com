SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `settings`;
CREATE TABLE IF NOT EXISTS `settings` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `value` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

INSERT INTO `settings` (`id`, `key`, `value`) VALUES(1, 'username', 'admin');
INSERT INTO `settings` (`id`, `key`, `value`) VALUES(2, 'password', '$2a$04$4xbJB1kfqs/B9tqzQRD1suugGSY877LkWwmx9EEm4emq6LMliWyny');

DROP TABLE IF EXISTS `customers`;
CREATE TABLE IF NOT EXISTS `customers` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `password` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `address` TEXT COLLATE utf8_unicode_ci NOT NULL,
    `phone_number` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `status` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    INDEX `password` (`password`),
    INDEX `name` (`name`),
    INDEX `phone_number` (`phone_number`),
    INDEX `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `customer_id` INT(11) UNSIGNED NOT NULL,
    `receipt` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `type` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `role` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `affiliate` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `currency` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `language` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `payment_method` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `tracking_codes` TEXT COLLATE utf8_unicode_ci NOT NULL,
    `vendor_variables` TEXT COLLATE utf8_unicode_ci NOT NULL,
    `vendor` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `amounts_account` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_order` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_shipping` DECIMAL(20,2) UNSIGNED NOT NULL,
    `amounts_tax` DECIMAL(20,2) UNSIGNED NOT NULL,
    `timestamp` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `orders_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `receipt` (`receipt`),
    INDEX `type` (`type`),
    INDEX `role` (`role`),
    INDEX `affiliate` (`affiliate`),
    INDEX `currency` (`currency`),
    INDEX `language` (`language`),
    INDEX `payment_method` (`payment_method`),
    INDEX `vendor` (`vendor`),
    INDEX `amounts_account` (`amounts_account`),
    INDEX `amounts_order` (`amounts_order`),
    INDEX `amounts_shipping` (`amounts_shipping`),
    INDEX `amounts_tax` (`amounts_tax`),
    INDEX `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `orders_products`;
CREATE TABLE IF NOT EXISTS `orders_products` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` INT(11) UNSIGNED NOT NULL,
    `item_number` INT(11) UNSIGNED NOT NULL,
    `title` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `url` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `recurring` BOOLEAN NOT NULL,
    `shippable` BOOLEAN NOT NULL,
    `amount` DECIMAL(20,2) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `orders_products_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY `order_id_item_number` (`order_id`, `item_number`),
    INDEX `order_id` (`order_id`),
    INDEX `item_number` (`item_number`),
    INDEX `title` (`title`),
    INDEX `url` (`url`),
    INDEX `recurring` (`recurring`),
    INDEX `shippable` (`shippable`),
    INDEX `amount` (`amount`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

SET FOREIGN_KEY_CHECKS = 1;
