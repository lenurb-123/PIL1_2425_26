-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: ifri_comotorage
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_comptes_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add email address',7,'add_emailaddress'),(26,'Can change email address',7,'change_emailaddress'),(27,'Can delete email address',7,'delete_emailaddress'),(28,'Can view email address',7,'view_emailaddress'),(29,'Can add email confirmation',8,'add_emailconfirmation'),(30,'Can change email confirmation',8,'change_emailconfirmation'),(31,'Can delete email confirmation',8,'delete_emailconfirmation'),(32,'Can view email confirmation',8,'view_emailconfirmation'),(33,'Can add social account',9,'add_socialaccount'),(34,'Can change social account',9,'change_socialaccount'),(35,'Can delete social account',9,'delete_socialaccount'),(36,'Can view social account',9,'view_socialaccount'),(37,'Can add social application',10,'add_socialapp'),(38,'Can change social application',10,'change_socialapp'),(39,'Can delete social application',10,'delete_socialapp'),(40,'Can view social application',10,'view_socialapp'),(41,'Can add social application token',11,'add_socialtoken'),(42,'Can change social application token',11,'change_socialtoken'),(43,'Can delete social application token',11,'delete_socialtoken'),(44,'Can view social application token',11,'view_socialtoken'),(45,'Can add conversation',12,'add_conversation'),(46,'Can change conversation',12,'change_conversation'),(47,'Can delete conversation',12,'delete_conversation'),(48,'Can view conversation',12,'view_conversation'),(49,'Can add newsletter',13,'add_newsletter'),(50,'Can change newsletter',13,'change_newsletter'),(51,'Can delete newsletter',13,'delete_newsletter'),(52,'Can view newsletter',13,'view_newsletter'),(53,'Can add notification',14,'add_notification'),(54,'Can change notification',14,'change_notification'),(55,'Can delete notification',14,'delete_notification'),(56,'Can view notification',14,'view_notification'),(57,'Can add participant',15,'add_participant'),(58,'Can change participant',15,'change_participant'),(59,'Can delete participant',15,'delete_participant'),(60,'Can view participant',15,'view_participant'),(61,'Can add utilisateur',16,'add_utilisateur'),(62,'Can change utilisateur',16,'change_utilisateur'),(63,'Can delete utilisateur',16,'delete_utilisateur'),(64,'Can view utilisateur',16,'view_utilisateur'),(65,'Can add chat message',17,'add_chatmessage'),(66,'Can change chat message',17,'change_chatmessage'),(67,'Can delete chat message',17,'delete_chatmessage'),(68,'Can view chat message',17,'view_chatmessage'),(69,'Can add message',18,'add_message'),(70,'Can change message',18,'change_message'),(71,'Can delete message',18,'delete_message'),(72,'Can view message',18,'view_message'),(73,'Can add trajet',19,'add_trajet'),(74,'Can change trajet',19,'change_trajet'),(75,'Can delete trajet',19,'delete_trajet'),(76,'Can view trajet',19,'view_trajet'),(77,'Can add position utilisateur',20,'add_positionutilisateur'),(78,'Can change position utilisateur',20,'change_positionutilisateur'),(79,'Can delete position utilisateur',20,'delete_positionutilisateur'),(80,'Can view position utilisateur',20,'view_positionutilisateur'),(81,'Can add reservation',21,'add_reservation'),(82,'Can change reservation',21,'change_reservation'),(83,'Can delete reservation',21,'delete_reservation'),(84,'Can view reservation',21,'view_reservation'),(85,'Can add avis',22,'add_avis'),(86,'Can change avis',22,'change_avis'),(87,'Can delete avis',22,'delete_avis'),(88,'Can view avis',22,'view_avis'),(89,'Can add trajet passage',23,'add_trajetpassage'),(90,'Can change trajet passage',23,'change_trajetpassage'),(91,'Can delete trajet passage',23,'delete_trajetpassage'),(92,'Can view trajet passage',23,'view_trajetpassage'),(93,'Can add trajet taxi',24,'add_trajettaxi'),(94,'Can change trajet taxi',24,'change_trajettaxi'),(95,'Can delete trajet taxi',24,'delete_trajettaxi'),(96,'Can view trajet taxi',24,'view_trajettaxi'),(97,'Can add appel',25,'add_appel'),(98,'Can change appel',25,'change_appel'),(99,'Can delete appel',25,'delete_appel'),(100,'Can view appel',25,'view_appel'),(101,'Can add discussion',26,'add_discussion'),(102,'Can change discussion',26,'change_discussion'),(103,'Can delete discussion',26,'delete_discussion'),(104,'Can view discussion',26,'view_discussion'),(105,'Can add action discussion',27,'add_actiondiscussion'),(106,'Can change action discussion',27,'change_actiondiscussion'),(107,'Can delete action discussion',27,'delete_actiondiscussion'),(108,'Can view action discussion',27,'view_actiondiscussion'),(109,'Can add message',28,'add_message'),(110,'Can change message',28,'change_message'),(111,'Can delete message',28,'delete_message'),(112,'Can view message',28,'view_message'),(113,'Can add parametres discussion',29,'add_parametresdiscussion'),(114,'Can change parametres discussion',29,'change_parametresdiscussion'),(115,'Can delete parametres discussion',29,'delete_parametresdiscussion'),(116,'Can view parametres discussion',29,'view_parametresdiscussion'),(117,'Can add statut lecture message',30,'add_statutlecturemessage'),(118,'Can change statut lecture message',30,'change_statutlecturemessage'),(119,'Can delete statut lecture message',30,'delete_statutlecturemessage'),(120,'Can view statut lecture message',30,'view_statutlecturemessage'),(121,'Can add TOTP device',31,'add_totpdevice'),(122,'Can change TOTP device',31,'change_totpdevice'),(123,'Can delete TOTP device',31,'delete_totpdevice'),(124,'Can view TOTP device',31,'view_totpdevice');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_chatmessage`
--

DROP TABLE IF EXISTS `comptes_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_chatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `sender_id` bigint NOT NULL,
  `conversation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comptes_chatmessage_sender_id_b00af400_fk_comptes_utilisateur_id` (`sender_id`),
  KEY `comptes_chatmessage_conversation_id_31b45057_fk_comptes_c` (`conversation_id`),
  CONSTRAINT `comptes_chatmessage_conversation_id_31b45057_fk_comptes_c` FOREIGN KEY (`conversation_id`) REFERENCES `comptes_conversation` (`id`),
  CONSTRAINT `comptes_chatmessage_sender_id_b00af400_fk_comptes_utilisateur_id` FOREIGN KEY (`sender_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_chatmessage`
--

LOCK TABLES `comptes_chatmessage` WRITE;
/*!40000 ALTER TABLE `comptes_chatmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_conversation`
--

DROP TABLE IF EXISTS `comptes_conversation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_conversation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_conversation`
--

LOCK TABLES `comptes_conversation` WRITE;
/*!40000 ALTER TABLE `comptes_conversation` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_conversation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_message`
--

DROP TABLE IF EXISTS `comptes_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `contenu` longtext NOT NULL,
  `date_envoie` datetime(6) NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `fichier` varchar(100) DEFAULT NULL,
  `destinataire_id` bigint NOT NULL,
  `discussion_id` bigint NOT NULL,
  `expediteur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comptes_message_destinataire_id_b360cd33_fk_comptes_u` (`destinataire_id`),
  KEY `comptes_message_discussion_id_9e5b1936_fk_discussio` (`discussion_id`),
  KEY `comptes_message_expediteur_id_e716f416_fk_comptes_utilisateur_id` (`expediteur_id`),
  CONSTRAINT `comptes_message_destinataire_id_b360cd33_fk_comptes_u` FOREIGN KEY (`destinataire_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `comptes_message_discussion_id_9e5b1936_fk_discussio` FOREIGN KEY (`discussion_id`) REFERENCES `discussions_discussion` (`id`),
  CONSTRAINT `comptes_message_expediteur_id_e716f416_fk_comptes_utilisateur_id` FOREIGN KEY (`expediteur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_message`
--

LOCK TABLES `comptes_message` WRITE;
/*!40000 ALTER TABLE `comptes_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_newsletter`
--

DROP TABLE IF EXISTS `comptes_newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_newsletter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_newsletter`
--

LOCK TABLES `comptes_newsletter` WRITE;
/*!40000 ALTER TABLE `comptes_newsletter` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_newsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_notification`
--

DROP TABLE IF EXISTS `comptes_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `lien` varchar(200) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comptes_notification_user_id_70629245_fk_comptes_utilisateur_id` (`user_id`),
  CONSTRAINT `comptes_notification_user_id_70629245_fk_comptes_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_notification`
--

LOCK TABLES `comptes_notification` WRITE;
/*!40000 ALTER TABLE `comptes_notification` DISABLE KEYS */;
INSERT INTO `comptes_notification` VALUES (1,'trajet','Nouveau passager !','Un passager cherche un trajet de Cotonou à IFRI UAC Bénin à 12:23',0,'2025-06-18 22:17:05.285762','/trajets/details/1/',3);
/*!40000 ALTER TABLE `comptes_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_participant`
--

DROP TABLE IF EXISTS `comptes_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_participant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `conversation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comptes_participant_conversation_id_user_id_50089807_uniq` (`conversation_id`,`user_id`),
  KEY `comptes_participant_user_id_2d51feac_fk_comptes_utilisateur_id` (`user_id`),
  CONSTRAINT `comptes_participant_conversation_id_f0ead319_fk_comptes_c` FOREIGN KEY (`conversation_id`) REFERENCES `comptes_conversation` (`id`),
  CONSTRAINT `comptes_participant_user_id_2d51feac_fk_comptes_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_participant`
--

LOCK TABLES `comptes_participant` WRITE;
/*!40000 ALTER TABLE `comptes_participant` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_utilisateur`
--

DROP TABLE IF EXISTS `comptes_utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_utilisateur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `vehicule` varchar(100) DEFAULT NULL,
  `immatriculation` varchar(20) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `adresse` varchar(200) DEFAULT NULL,
  `ville` varchar(100) DEFAULT NULL,
  `departement` varchar(100) DEFAULT NULL,
  `photo_profil` varchar(100) DEFAULT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `derniere_connexion` datetime(6) DEFAULT NULL,
  `est_verifie` tinyint(1) NOT NULL,
  `est_actif` tinyint(1) NOT NULL,
  `est_bloque` tinyint(1) NOT NULL,
  `date_blocage` datetime(6) DEFAULT NULL,
  `raison_blocage` longtext,
  `date_derniere_modification` datetime(6) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `adresse_depart_habituelle` varchar(100) NOT NULL,
  `heure_depart_habituelle` time(6) DEFAULT NULL,
  `heure_arrivee_habituelle` time(6) DEFAULT NULL,
  `marque_vehicule` varchar(100) NOT NULL,
  `modele_vehicule` varchar(100) NOT NULL,
  `places_disponibles` int unsigned DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `deux_facteurs_active` tinyint(1) NOT NULL,
  `deux_facteurs_code` varchar(6) DEFAULT NULL,
  `deux_facteurs_code_expiration` datetime(6) DEFAULT NULL,
  `two_factor_enabled` tinyint(1) NOT NULL,
  `totp_secret` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `comptes_utilisateur_chk_1` CHECK ((`places_disponibles` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_utilisateur`
--

LOCK TABLES `comptes_utilisateur` WRITE;
/*!40000 ALTER TABLE `comptes_utilisateur` DISABLE KEYS */;
INSERT INTO `comptes_utilisateur` VALUES (1,'pbkdf2_sha256$1000000$sCjxp1vtToHfHg2w2czpB8$1RtYCA4ei1qRdJBeUmkO4pejHnMCR49DKLd6/+hqgOA=',NULL,1,'admin@gmail.com','ADMIN','ADMIN',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','2025-06-18 22:07:08.011748',NULL,0,1,0,NULL,NULL,'2025-06-18 22:07:07.250284','passager','',NULL,NULL,'','',NULL,1,1,0,NULL,NULL,0,NULL),(2,'pbkdf2_sha256$1000000$ZR8nUaNvyE0a74qZk34OCL$ygoMY9cLA2TOW2FViinCCv67PjzGdSYCq3kpfDIvFQI=','2025-06-18 22:16:04.412732',0,'kpogbemebrunel@gmail.com','Ks','Brunel','23212312',NULL,NULL,NULL,NULL,NULL,NULL,'','2025-06-18 22:10:30.392119',NULL,0,1,0,NULL,NULL,'2025-06-18 22:10:28.619859','passager','',NULL,NULL,'','',NULL,1,0,0,NULL,NULL,0,NULL),(3,'pbkdf2_sha256$1000000$uWWMGZzUYiCmknK8XgplfW$5iIZuBUQX29loG9fBGo2pTgyZCfDhh+1CIF3UWMuNOI=','2025-06-18 22:13:03.361716',0,'felix@gmail.com','TOVIGNAN','Félix','23232323',NULL,'AB-123-DA',NULL,NULL,NULL,NULL,'','2025-06-18 22:11:38.801996',NULL,0,1,0,NULL,NULL,'2025-06-18 22:11:37.161675','conducteur','',NULL,NULL,'','',NULL,1,0,0,NULL,NULL,0,NULL),(4,'pbkdf2_sha256$1000000$2SZ8BdPcYQXJ5jS8SpEd6b$Jr79u69XCzWYoPNAFzVITNpqHKXdmpESdCkOWfjm3C8=',NULL,0,'ulrich@gmail.com','BM','Ulrich','21212121',NULL,NULL,NULL,NULL,NULL,NULL,'','2025-06-18 22:12:35.907281',NULL,0,1,0,NULL,NULL,'2025-06-18 22:12:34.200706','passager','',NULL,NULL,'','',NULL,1,0,0,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `comptes_utilisateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_utilisateur_groups`
--

DROP TABLE IF EXISTS `comptes_utilisateur_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_utilisateur_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comptes_utilisateur_groups_utilisateur_id_group_id_f6703be7_uniq` (`utilisateur_id`,`group_id`),
  KEY `comptes_utilisateur_groups_group_id_40550a17_fk_auth_group_id` (`group_id`),
  CONSTRAINT `comptes_utilisateur__utilisateur_id_2c4242fe_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `comptes_utilisateur_groups_group_id_40550a17_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_utilisateur_groups`
--

LOCK TABLES `comptes_utilisateur_groups` WRITE;
/*!40000 ALTER TABLE `comptes_utilisateur_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_utilisateur_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes_utilisateur_user_permissions`
--

DROP TABLE IF EXISTS `comptes_utilisateur_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes_utilisateur_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comptes_utilisateur_user_utilisateur_id_permissio_6ccc9f1d_uniq` (`utilisateur_id`,`permission_id`),
  KEY `comptes_utilisateur__permission_id_6de48079_fk_auth_perm` (`permission_id`),
  CONSTRAINT `comptes_utilisateur__permission_id_6de48079_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `comptes_utilisateur__utilisateur_id_edaf0051_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes_utilisateur_user_permissions`
--

LOCK TABLES `comptes_utilisateur_user_permissions` WRITE;
/*!40000 ALTER TABLE `comptes_utilisateur_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes_utilisateur_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_actiondiscussion`
--

DROP TABLE IF EXISTS `discussions_actiondiscussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_actiondiscussion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_action` varchar(30) NOT NULL,
  `details` json DEFAULT NULL,
  `date_action` datetime(6) NOT NULL,
  `utilisateur_id` bigint NOT NULL,
  `discussion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussions_actiondi_utilisateur_id_0567eff3_fk_comptes_u` (`utilisateur_id`),
  KEY `discussions_actiondi_discussion_id_2ae81938_fk_discussio` (`discussion_id`),
  CONSTRAINT `discussions_actiondi_discussion_id_2ae81938_fk_discussio` FOREIGN KEY (`discussion_id`) REFERENCES `discussions_discussion` (`id`),
  CONSTRAINT `discussions_actiondi_utilisateur_id_0567eff3_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_actiondiscussion`
--

LOCK TABLES `discussions_actiondiscussion` WRITE;
/*!40000 ALTER TABLE `discussions_actiondiscussion` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussions_actiondiscussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_appel`
--

DROP TABLE IF EXISTS `discussions_appel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_appel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_debut` datetime(6) NOT NULL,
  `date_fin` datetime(6) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `emetteur_id` bigint NOT NULL,
  `recepteur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussions_appel_emetteur_id_7210dd07_fk_comptes_utilisateur_id` (`emetteur_id`),
  KEY `discussions_appel_recepteur_id_34e58ab1_fk_comptes_u` (`recepteur_id`),
  CONSTRAINT `discussions_appel_emetteur_id_7210dd07_fk_comptes_utilisateur_id` FOREIGN KEY (`emetteur_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `discussions_appel_recepteur_id_34e58ab1_fk_comptes_u` FOREIGN KEY (`recepteur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_appel`
--

LOCK TABLES `discussions_appel` WRITE;
/*!40000 ALTER TABLE `discussions_appel` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussions_appel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_discussion`
--

DROP TABLE IF EXISTS `discussions_discussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_discussion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `type` varchar(10) NOT NULL,
  `confidentialite` varchar(10) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `statut` varchar(20) NOT NULL,
  `createur_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `discussions_discussi_createur_id_e2b7d680_fk_comptes_u` (`createur_id`),
  CONSTRAINT `discussions_discussi_createur_id_e2b7d680_fk_comptes_u` FOREIGN KEY (`createur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_discussion`
--

LOCK TABLES `discussions_discussion` WRITE;
/*!40000 ALTER TABLE `discussions_discussion` DISABLE KEYS */;
INSERT INTO `discussions_discussion` VALUES (1,'','privee','public','','','2025-06-18 22:13:46.112363','2025-06-18 22:14:02.023618','active',NULL),(2,'','privee','public','','','2025-06-18 22:14:06.270518','2025-06-18 22:16:41.574679','active',NULL),(3,'','privee','public','','','2025-06-18 22:14:22.269550','2025-06-18 22:14:28.773371','active',NULL),(4,'','groupe','public','','','2025-06-18 22:14:42.984661','2025-06-18 22:16:30.746239','active',NULL),(5,'Groupe','groupe','public','','','2025-06-18 22:15:04.098034','2025-06-18 22:16:21.762119','active',NULL);
/*!40000 ALTER TABLE `discussions_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_discussion_participants`
--

DROP TABLE IF EXISTS `discussions_discussion_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_discussion_participants` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `discussion_id` bigint NOT NULL,
  `utilisateur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discussions_discussion_p_discussion_id_utilisateu_95641379_uniq` (`discussion_id`,`utilisateur_id`),
  KEY `discussions_discussi_utilisateur_id_26c58744_fk_comptes_u` (`utilisateur_id`),
  CONSTRAINT `discussions_discussi_discussion_id_7ccd675f_fk_discussio` FOREIGN KEY (`discussion_id`) REFERENCES `discussions_discussion` (`id`),
  CONSTRAINT `discussions_discussi_utilisateur_id_26c58744_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_discussion_participants`
--

LOCK TABLES `discussions_discussion_participants` WRITE;
/*!40000 ALTER TABLE `discussions_discussion_participants` DISABLE KEYS */;
INSERT INTO `discussions_discussion_participants` VALUES (1,1,1),(2,1,3),(3,2,2),(4,2,3),(5,3,3),(6,3,4),(7,4,1),(8,4,2),(9,4,3),(10,5,1),(11,5,2),(12,5,3),(13,5,4);
/*!40000 ALTER TABLE `discussions_discussion_participants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_message`
--

DROP TABLE IF EXISTS `discussions_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `contenu` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `media` varchar(100) DEFAULT NULL,
  `media_type` varchar(10) DEFAULT NULL,
  `date_envoi` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `supprime` tinyint(1) NOT NULL,
  `destinataire_id` bigint DEFAULT NULL,
  `discussion_id` bigint NOT NULL,
  `expediteur_id` bigint NOT NULL,
  `message_parent_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `discussions_message_destinataire_id_0d62f1b9_fk_comptes_u` (`destinataire_id`),
  KEY `discussions_message_discussion_id_398a2411_fk_discussio` (`discussion_id`),
  KEY `discussions_message_expediteur_id_3c5d5a52_fk_comptes_u` (`expediteur_id`),
  KEY `discussions_message_message_parent_id_a361265d_fk_discussio` (`message_parent_id`),
  CONSTRAINT `discussions_message_destinataire_id_0d62f1b9_fk_comptes_u` FOREIGN KEY (`destinataire_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `discussions_message_discussion_id_398a2411_fk_discussio` FOREIGN KEY (`discussion_id`) REFERENCES `discussions_discussion` (`id`),
  CONSTRAINT `discussions_message_expediteur_id_3c5d5a52_fk_comptes_u` FOREIGN KEY (`expediteur_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `discussions_message_message_parent_id_a361265d_fk_discussio` FOREIGN KEY (`message_parent_id`) REFERENCES `discussions_message` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_message`
--

LOCK TABLES `discussions_message` WRITE;
/*!40000 ALTER TABLE `discussions_message` DISABLE KEYS */;
INSERT INTO `discussions_message` VALUES (1,'Bonjour l-admin','text','',NULL,'2025-06-18 22:13:55.800611','2025-06-18 22:13:55.800635',0,0,NULL,1,3,NULL),(2,'','media','messages/1/Al Ahsa, Saudi Arabia (ID-13544).jpg','image','2025-06-18 22:14:02.019032','2025-06-18 22:14:02.019056',0,0,NULL,1,3,NULL),(3,'Salut toi comment vas tu','text','',NULL,'2025-06-18 22:14:19.076233','2025-06-18 22:14:19.076258',0,0,NULL,2,3,NULL),(4,'Salut','text','',NULL,'2025-06-18 22:14:28.768427','2025-06-18 22:14:28.768445',0,0,NULL,3,3,NULL),(5,'SALut','text','',NULL,'2025-06-18 22:14:49.843504','2025-06-18 22:14:49.843522',0,0,NULL,4,3,NULL),(6,'SA','text','',NULL,'2025-06-18 22:15:08.144339','2025-06-18 22:15:08.144353',0,0,NULL,5,3,NULL),(7,'Salut ici','text','',NULL,'2025-06-18 22:15:12.995992','2025-06-18 22:15:12.996018',0,0,NULL,5,3,NULL),(8,'OUI bonjour comment allez vous','text','',NULL,'2025-06-18 22:16:21.756713','2025-06-18 22:16:21.756746',0,0,NULL,5,2,NULL),(9,'Salut chef','text','',NULL,'2025-06-18 22:16:30.742353','2025-06-18 22:16:30.742384',0,0,NULL,4,2,NULL),(10,'Tout va bien','text','',NULL,'2025-06-18 22:16:41.570687','2025-06-18 22:16:41.570711',0,0,NULL,2,2,NULL);
/*!40000 ALTER TABLE `discussions_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_parametresdiscussion`
--

DROP TABLE IF EXISTS `discussions_parametresdiscussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_parametresdiscussion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notifications` tinyint(1) NOT NULL,
  `epingle` tinyint(1) NOT NULL,
  `archive` tinyint(1) NOT NULL,
  `couleur` varchar(7) DEFAULT NULL,
  `discussion_id` bigint NOT NULL,
  `utilisateur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discussions_parametresdi_utilisateur_id_discussio_a42c6385_uniq` (`utilisateur_id`,`discussion_id`),
  KEY `discussions_parametr_discussion_id_b7580d7e_fk_discussio` (`discussion_id`),
  CONSTRAINT `discussions_parametr_discussion_id_b7580d7e_fk_discussio` FOREIGN KEY (`discussion_id`) REFERENCES `discussions_discussion` (`id`),
  CONSTRAINT `discussions_parametr_utilisateur_id_0e9bf4f6_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_parametresdiscussion`
--

LOCK TABLES `discussions_parametresdiscussion` WRITE;
/*!40000 ALTER TABLE `discussions_parametresdiscussion` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussions_parametresdiscussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussions_statutlecturemessage`
--

DROP TABLE IF EXISTS `discussions_statutlecturemessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discussions_statutlecturemessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lu` tinyint(1) NOT NULL,
  `date_lecture` datetime(6) DEFAULT NULL,
  `message_id` bigint NOT NULL,
  `utilisateur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discussions_statutlectur_message_id_utilisateur_i_34b301cf_uniq` (`message_id`,`utilisateur_id`),
  KEY `discussions_statutle_utilisateur_id_76513c1a_fk_comptes_u` (`utilisateur_id`),
  CONSTRAINT `discussions_statutle_message_id_90c465a3_fk_discussio` FOREIGN KEY (`message_id`) REFERENCES `discussions_message` (`id`),
  CONSTRAINT `discussions_statutle_utilisateur_id_76513c1a_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussions_statutlecturemessage`
--

LOCK TABLES `discussions_statutlecturemessage` WRITE;
/*!40000 ALTER TABLE `discussions_statutlecturemessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussions_statutlecturemessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_comptes_utilisateur_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_comptes_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'account','emailaddress'),(8,'account','emailconfirmation'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(17,'comptes','chatmessage'),(12,'comptes','conversation'),(18,'comptes','message'),(13,'comptes','newsletter'),(14,'comptes','notification'),(15,'comptes','participant'),(16,'comptes','utilisateur'),(4,'contenttypes','contenttype'),(27,'discussions','actiondiscussion'),(25,'discussions','appel'),(26,'discussions','discussion'),(28,'discussions','message'),(29,'discussions','parametresdiscussion'),(30,'discussions','statutlecturemessage'),(31,'otp_totp','totpdevice'),(5,'sessions','session'),(6,'sites','site'),(9,'socialaccount','socialaccount'),(10,'socialaccount','socialapp'),(11,'socialaccount','socialtoken'),(22,'trajets','avis'),(20,'trajets','positionutilisateur'),(21,'trajets','reservation'),(19,'trajets','trajet'),(23,'trajets','trajetpassage'),(24,'trajets','trajettaxi');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-18 22:03:46.603186'),(2,'contenttypes','0002_remove_content_type_name','2025-06-18 22:03:46.719106'),(3,'auth','0001_initial','2025-06-18 22:03:47.023191'),(4,'auth','0002_alter_permission_name_max_length','2025-06-18 22:03:47.095298'),(5,'auth','0003_alter_user_email_max_length','2025-06-18 22:03:47.101590'),(6,'auth','0004_alter_user_username_opts','2025-06-18 22:03:47.108252'),(7,'auth','0005_alter_user_last_login_null','2025-06-18 22:03:47.115269'),(8,'auth','0006_require_contenttypes_0002','2025-06-18 22:03:47.119031'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-18 22:03:47.126471'),(10,'auth','0008_alter_user_username_max_length','2025-06-18 22:03:47.134031'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-18 22:03:47.139958'),(12,'auth','0010_alter_group_name_max_length','2025-06-18 22:03:47.157155'),(13,'auth','0011_update_proxy_permissions','2025-06-18 22:03:47.165061'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-18 22:03:47.173610'),(15,'comptes','0001_initial','2025-06-18 22:03:47.975359'),(16,'account','0001_initial','2025-06-18 22:03:48.198574'),(17,'account','0002_email_max_length','2025-06-18 22:03:48.225874'),(18,'account','0003_alter_emailaddress_create_unique_verified_email','2025-06-18 22:03:48.266717'),(19,'account','0004_alter_emailaddress_drop_unique_email','2025-06-18 22:03:48.314420'),(20,'account','0005_emailaddress_idx_upper_email','2025-06-18 22:03:48.347022'),(21,'account','0006_emailaddress_lower','2025-06-18 22:03:48.372134'),(22,'account','0007_emailaddress_idx_email','2025-06-18 22:03:48.430954'),(23,'account','0008_emailaddress_unique_primary_email_fixup','2025-06-18 22:03:48.450677'),(24,'account','0009_emailaddress_unique_primary_email','2025-06-18 22:03:48.462746'),(25,'admin','0001_initial','2025-06-18 22:03:48.631637'),(26,'admin','0002_logentry_remove_auto_add','2025-06-18 22:03:48.643850'),(27,'admin','0003_logentry_add_action_flag_choices','2025-06-18 22:03:48.657759'),(28,'discussions','0001_initial','2025-06-18 22:03:49.904338'),(29,'comptes','0002_initial','2025-06-18 22:03:50.359518'),(30,'otp_totp','0001_initial','2025-06-18 22:03:50.490202'),(31,'otp_totp','0002_auto_20190420_0723','2025-06-18 22:03:50.680637'),(32,'otp_totp','0003_add_timestamps','2025-06-18 22:03:50.787299'),(33,'sessions','0001_initial','2025-06-18 22:03:50.885806'),(34,'sites','0001_initial','2025-06-18 22:03:50.912579'),(35,'sites','0002_alter_domain_unique','2025-06-18 22:03:50.935510'),(36,'socialaccount','0001_initial','2025-06-18 22:03:51.442466'),(37,'socialaccount','0002_token_max_lengths','2025-06-18 22:03:51.512762'),(38,'socialaccount','0003_extra_data_default_dict','2025-06-18 22:03:51.538612'),(39,'socialaccount','0004_app_provider_id_settings','2025-06-18 22:03:51.719910'),(40,'socialaccount','0005_socialtoken_nullable_app','2025-06-18 22:03:51.897752'),(41,'socialaccount','0006_alter_socialaccount_extra_data','2025-06-18 22:03:51.990354'),(42,'trajets','0001_initial','2025-06-18 22:03:52.749804');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3pb9g8x07fvopuzo1zdrrkjtmx2m0l2o','.eJxVjMsOwiAQRf-FtSFA5dEu3fsNZIAZixpoSptojP-uTbrQ7T3nnhfzsC6jXxvOPic2MMUOv1uAeMOygXSFcqk81rLMOfBN4Ttt_FwT3k-7-xcYoY3fN2FwvTN9lMqQ6EgQOYsGkiZHMZEKIliCzigidFEKoa086mjBaIO93KINW8u1eHxMeX6yQbw_vIQ_uQ:1uS14e:RaR4LA2dxN_pai15sB-o5DzixRtJ4sw7LlWFTXyA1ok','2025-07-18 22:16:04.419669');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `otp_totp_totpdevice`
--

DROP TABLE IF EXISTS `otp_totp_totpdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `otp_totp_totpdevice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `key` varchar(80) NOT NULL,
  `step` smallint unsigned NOT NULL,
  `t0` bigint NOT NULL,
  `digits` smallint unsigned NOT NULL,
  `tolerance` smallint unsigned NOT NULL,
  `drift` smallint NOT NULL,
  `last_t` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `throttling_failure_count` int unsigned NOT NULL,
  `throttling_failure_timestamp` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `last_used_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `otp_totp_totpdevice_user_id_0fb18292_fk_comptes_utilisateur_id` (`user_id`),
  CONSTRAINT `otp_totp_totpdevice_user_id_0fb18292_fk_comptes_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `otp_totp_totpdevice_chk_1` CHECK ((`step` >= 0)),
  CONSTRAINT `otp_totp_totpdevice_chk_2` CHECK ((`digits` >= 0)),
  CONSTRAINT `otp_totp_totpdevice_chk_3` CHECK ((`tolerance` >= 0)),
  CONSTRAINT `otp_totp_totpdevice_chk_4` CHECK ((`throttling_failure_count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `otp_totp_totpdevice`
--

LOCK TABLES `otp_totp_totpdevice` WRITE;
/*!40000 ALTER TABLE `otp_totp_totpdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `otp_totp_totpdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_social_user_id_8146e70c_fk_comptes_u` (`user_id`),
  CONSTRAINT `socialaccount_social_user_id_8146e70c_fk_comptes_u` FOREIGN KEY (`user_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_avis`
--

DROP TABLE IF EXISTS `trajets_avis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_avis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `note` int NOT NULL,
  `commentaire` longtext NOT NULL,
  `auteur_id` bigint NOT NULL,
  `destinataire_id` bigint NOT NULL,
  `trajet_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trajets_avis_auteur_id_74248d74_fk_comptes_utilisateur_id` (`auteur_id`),
  KEY `trajets_avis_destinataire_id_87487a49_fk_comptes_utilisateur_id` (`destinataire_id`),
  KEY `trajets_avis_trajet_id_99830976_fk_trajets_trajet_id` (`trajet_id`),
  CONSTRAINT `trajets_avis_auteur_id_74248d74_fk_comptes_utilisateur_id` FOREIGN KEY (`auteur_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `trajets_avis_destinataire_id_87487a49_fk_comptes_utilisateur_id` FOREIGN KEY (`destinataire_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `trajets_avis_trajet_id_99830976_fk_trajets_trajet_id` FOREIGN KEY (`trajet_id`) REFERENCES `trajets_trajet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_avis`
--

LOCK TABLES `trajets_avis` WRITE;
/*!40000 ALTER TABLE `trajets_avis` DISABLE KEYS */;
/*!40000 ALTER TABLE `trajets_avis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_positionutilisateur`
--

DROP TABLE IF EXISTS `trajets_positionutilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_positionutilisateur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `utilisateur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `trajets_positionutil_utilisateur_id_1501d71d_fk_comptes_u` FOREIGN KEY (`utilisateur_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_positionutilisateur`
--

LOCK TABLES `trajets_positionutilisateur` WRITE;
/*!40000 ALTER TABLE `trajets_positionutilisateur` DISABLE KEYS */;
/*!40000 ALTER TABLE `trajets_positionutilisateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_reservation`
--

DROP TABLE IF EXISTS `trajets_reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_reservation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `passager_nom` varchar(100) NOT NULL,
  `passager_prenom` varchar(100) NOT NULL,
  `depart` varchar(255) NOT NULL,
  `arrivee` varchar(255) NOT NULL,
  `heure_depart` datetime(6) NOT NULL,
  `heure_arrivee` datetime(6) NOT NULL,
  `places_reservees` int unsigned NOT NULL,
  `date_reservation` datetime(6) NOT NULL,
  `created_le` datetime(6) NOT NULL,
  `trajet_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trajets_reservation_trajet_id_1d4330ee_fk_trajets_trajet_id` (`trajet_id`),
  CONSTRAINT `trajets_reservation_trajet_id_1d4330ee_fk_trajets_trajet_id` FOREIGN KEY (`trajet_id`) REFERENCES `trajets_trajet` (`id`),
  CONSTRAINT `trajets_reservation_chk_1` CHECK ((`places_reservees` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_reservation`
--

LOCK TABLES `trajets_reservation` WRITE;
/*!40000 ALTER TABLE `trajets_reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `trajets_reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_trajet`
--

DROP TABLE IF EXISTS `trajets_trajet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_trajet` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `conducteur_nom` varchar(100) NOT NULL,
  `conducteur_prenom` varchar(100) NOT NULL,
  `depart` varchar(255) NOT NULL,
  `arrivee` varchar(255) NOT NULL,
  `heure_depart` datetime(6) NOT NULL,
  `heure_arrivee` datetime(6) NOT NULL,
  `places_disponibles` int unsigned NOT NULL,
  `tarif` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `trajets_trajet_chk_1` CHECK ((`places_disponibles` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_trajet`
--

LOCK TABLES `trajets_trajet` WRITE;
/*!40000 ALTER TABLE `trajets_trajet` DISABLE KEYS */;
/*!40000 ALTER TABLE `trajets_trajet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_trajetpassage`
--

DROP TABLE IF EXISTS `trajets_trajetpassage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_trajetpassage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lieu_depart` varchar(255) NOT NULL,
  `lieu_arrivee` varchar(255) NOT NULL,
  `heure_souhaitee` time(6) DEFAULT NULL,
  `jours_semaine` varchar(50) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `statut` varchar(20) NOT NULL,
  `tarif` decimal(8,2) NOT NULL,
  `passager_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trajets_trajetpassag_passager_id_15e2f813_fk_comptes_u` (`passager_id`),
  CONSTRAINT `trajets_trajetpassag_passager_id_15e2f813_fk_comptes_u` FOREIGN KEY (`passager_id`) REFERENCES `comptes_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_trajetpassage`
--

LOCK TABLES `trajets_trajetpassage` WRITE;
/*!40000 ALTER TABLE `trajets_trajetpassage` DISABLE KEYS */;
INSERT INTO `trajets_trajetpassage` VALUES (1,'Cotonou','IFRI UAC Bénin','12:23:00.000000','Lun,Mar','2025-06-18 22:17:05.275761','proposé',0.00,2);
/*!40000 ALTER TABLE `trajets_trajetpassage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trajets_trajettaxi`
--

DROP TABLE IF EXISTS `trajets_trajettaxi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_trajettaxi` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lieu_depart` varchar(255) NOT NULL,
  `lieu_arrivee` varchar(255) NOT NULL,
  `heure_depart` time(6) DEFAULT NULL,
  `jours_semaine` varchar(50) NOT NULL,
  `places_disponibles` int unsigned NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `statut` varchar(20) NOT NULL,
  `tarif` decimal(8,2) NOT NULL,
  `conducteur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trajets_trajettaxi_conducteur_id_891a37c6_fk_comptes_u` (`conducteur_id`),
  CONSTRAINT `trajets_trajettaxi_conducteur_id_891a37c6_fk_comptes_u` FOREIGN KEY (`conducteur_id`) REFERENCES `comptes_utilisateur` (`id`),
  CONSTRAINT `trajets_trajettaxi_chk_1` CHECK ((`places_disponibles` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trajets_trajettaxi`
--

LOCK TABLES `trajets_trajettaxi` WRITE;
/*!40000 ALTER TABLE `trajets_trajettaxi` DISABLE KEYS */;
INSERT INTO `trajets_trajettaxi` VALUES (1,'Cotonou','IFRI UAC Bénin',NULL,'Lun,Mar,Mer',1,'2025-06-18 22:13:35.751079','proposé',0.00,3);
/*!40000 ALTER TABLE `trajets_trajettaxi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 23:22:31
