--
-- Create model Apartment
--
CREATE TABLE `main_apartment` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ad_date` date NOT NULL,
    `token` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `district` varchar(255) NOT NULL,
    `title` longtext NOT NULL,
    `description` longtext NOT NULL,
    `floor_number` integer NOT NULL,
    `total_floors` integer NOT NULL,
    `msquare` integer NOT NULL,
    `total_price` bigint NOT NULL,
    `price_per_msquare` bigint NOT NULL,
    `production_year` integer NOT NULL,
    `rooms` integer NOT NULL,
    `elevator` bool NOT NULL,
    `parking` bool NOT NULL,
    `storeroom` bool NOT NULL
    );
--
-- Create model Land
--
CREATE TABLE `main_land` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ad_date` date NOT NULL,
    `token` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `district` varchar(255) NOT NULL,
    `title` longtext NOT NULL,
    `description` longtext NOT NULL,
    `land_msquare` integer NOT NULL,
    `total_price` bigint NOT NULL,
    `price_per_msquare` bigint NOT NULL
    );
--
-- Create model Villa
--
CREATE TABLE `main_villa` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ad_date` date NOT NULL,
    `token` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `district` varchar(255) NOT NULL,
    `title` longtext NOT NULL,
    `description` longtext NOT NULL,
    `land_msquare` integer NOT NULL,
    `msquare` integer NOT NULL,
    `total_price` bigint NOT NULL,
    `price_per_msquare` bigint NOT NULL,
    `production_year` integer NOT NULL,
    `rooms` integer NOT NULL,
    `storeroom` bool NOT NULL,
    `parking` bool NOT NULL, 
    `balcony` bool NOT NULL
    );