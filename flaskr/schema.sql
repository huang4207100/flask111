DROP TABLE IF EXISTS `order`;

DROP TABLE IF EXISTS comment;

DROP TABLE IF EXISTS item;

DROP TABLE IF EXISTS user;


CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `password_UNIQUE` (`password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'item name',
  `picture` varchar(45) DEFAULT 'item name',
  `price` int NOT NULL,
  `describe` varchar(45) DEFAULT 'item name',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(45) NOT NULL,
  `item_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id_idx` (`item_id`),
  CONSTRAINT `item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `user_id` int NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `idcard_name` varchar(45) DEFAULT NULL,
  `idcard_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id_idx` (`item_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `item_id_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `user_id_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('car111','1.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('banana car','2.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('big car','3.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('small car','4.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('hug car','5.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('yellow car','6.jpg','50333333','the car hope you buy with money');

INSERT INTO `db`.`item` (`name`,`picture`,`price`,`describe`) VALUES ('red car','7.jpg','50333333','the car hope you buy with money');




