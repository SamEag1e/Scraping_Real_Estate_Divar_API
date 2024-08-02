--
-- Table structure for table `main_apartment`
--

DROP TABLE IF EXISTS `main_apartment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_apartment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ad_date` date NOT NULL,
  `token` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `title` longtext NOT NULL,
  `description` longtext NOT NULL,
  `floor_number` int NOT NULL,
  `total_floors` int NOT NULL,
  `msquare` int NOT NULL,
  `total_price` bigint NOT NULL,
  `price_per_msquare` bigint NOT NULL,
  `production_year` int NOT NULL,
  `rooms` int NOT NULL,
  `elevator` tinyint(1) NOT NULL,
  `parking` tinyint(1) NOT NULL,
  `storeroom` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=856 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `main_land`
--

DROP TABLE IF EXISTS `main_land`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_land` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ad_date` date NOT NULL,
  `token` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `title` longtext NOT NULL,
  `description` longtext NOT NULL,
  `land_msquare` int NOT NULL,
  `total_price` bigint NOT NULL,
  `price_per_msquare` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=712 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `main_villa`
--

DROP TABLE IF EXISTS `main_villa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_villa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ad_date` date NOT NULL,
  `token` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `title` longtext NOT NULL,
  `description` longtext NOT NULL,
  `land_msquare` int NOT NULL,
  `msquare` int NOT NULL,
  `total_price` bigint NOT NULL,
  `price_per_msquare` bigint NOT NULL,
  `production_year` int NOT NULL,
  `rooms` int NOT NULL,
  `storeroom` tinyint(1) NOT NULL,
  `parking` tinyint(1) NOT NULL,
  `balcony` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=703 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;