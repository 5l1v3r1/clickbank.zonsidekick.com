SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `clickbank_settings`;
CREATE TABLE IF NOT EXISTS `clickbank_settings` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `value` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

INSERT INTO `clickbank_settings` (`id`, `key`, `value`) VALUES(1, 'username', 'admin');
INSERT INTO `clickbank_settings` (`id`, `key`, `value`) VALUES(2, 'password', '$2a$04$4xbJB1kfqs/B9tqzQRD1suugGSY877LkWwmx9EEm4emq6LMliWyny');

DROP TABLE IF EXISTS `clickbank_orders`;
CREATE TABLE IF NOT EXISTS `clickbank_orders` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `customer_id` BIGINT(20) UNSIGNED NOT NULL,
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
    INDEX `customer_id` (`customer_id`),
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

DROP TABLE IF EXISTS `clickbank_orders_products`;
CREATE TABLE IF NOT EXISTS `clickbank_orders_products` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` INT(11) UNSIGNED NOT NULL,
    `item_number` INT(11) UNSIGNED NOT NULL,
    `title` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `url` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `recurring` BOOLEAN NOT NULL,
    `shippable` BOOLEAN NOT NULL,
    `amount` DECIMAL(20,2) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `clickbank_orders_products_order_id` FOREIGN KEY (`order_id`) REFERENCES `clickbank_orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
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
