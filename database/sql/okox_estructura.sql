-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para okox_pruebas
CREATE DATABASE IF NOT EXISTS `okox_pruebas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `okox_pruebas`;

-- Volcando estructura para tabla okox_pruebas.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `rfc` varchar(13) NOT NULL,
  `id_umbral` int NOT NULL,
  `id_company` int NOT NULL,
  `estado_servicio` int NOT NULL,
  `fecha_contratacion` datetime NOT NULL,
  PRIMARY KEY (`rfc`),
  UNIQUE KEY `rfc` (`rfc`),
  KEY `id_umbral` (`id_umbral`),
  KEY `id_company` (`id_company`) USING BTREE,
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`),
  CONSTRAINT `clientes_ibfk_2` FOREIGN KEY (`id_umbral`) REFERENCES `umbral_clientes` (`id`),
  CONSTRAINT `clientes_ibfk_3` FOREIGN KEY (`id_company`) REFERENCES `company` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.colonias
CREATE TABLE IF NOT EXISTS `colonias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `municipio` int DEFAULT NULL,
  `asentamiento` varchar(100) DEFAULT NULL,
  `codigo_postal` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `municipio` (`municipio`),
  CONSTRAINT `colonias_ibfk_1` FOREIGN KEY (`municipio`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1607710190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.company
CREATE TABLE IF NOT EXISTS `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc` varchar(13) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` text,
  `facebook` varchar(150) DEFAULT NULL,
  `linkedIn` varchar(150) DEFAULT NULL,
  `link_x` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rfc` (`rfc`),
  CONSTRAINT `company_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.dispositivos
CREATE TABLE IF NOT EXISTS `dispositivos` (
  `Wifi_MacAddress` varchar(17) NOT NULL,
  `rfc` varchar(13) NOT NULL,
  `valvula` tinyint(1) DEFAULT NULL,
  `last_connection` datetime DEFAULT NULL,
  PRIMARY KEY (`Wifi_MacAddress`),
  UNIQUE KEY `Wifi_MacAddress` (`Wifi_MacAddress`),
  KEY `rfc` (`rfc`),
  CONSTRAINT `dispositivos_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `clientes` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.estados
CREATE TABLE IF NOT EXISTS `estados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `pais` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pais` (`pais`),
  CONSTRAINT `estados_ibfk_1` FOREIGN KEY (`pais`) REFERENCES `paises` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.mantenimientos
CREATE TABLE IF NOT EXISTS `mantenimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(80) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `fecha` datetime NOT NULL,
  `colonia_afectada` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `colonia_afectada` (`colonia_afectada`),
  CONSTRAINT `mantenimientos_ibfk_1` FOREIGN KEY (`colonia_afectada`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.motivo_suspensiones
CREATE TABLE IF NOT EXISTS `motivo_suspensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.municipios
CREATE TABLE IF NOT EXISTS `municipios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `estado` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estado` (`estado`),
  CONSTRAINT `municipios_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32059 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.notificaciones
CREATE TABLE IF NOT EXISTS `notificaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc` varchar(13) DEFAULT NULL,
  `asunto` varchar(80) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `tipo` varchar(80) NOT NULL,
  `fecha_envio` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rfc` (`rfc`),
  CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `clientes` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.pagos
CREATE TABLE IF NOT EXISTS `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc` varchar(13) NOT NULL,
  `comprobante` mediumblob NOT NULL,
  `monto` float NOT NULL,
  `fecha_pago` datetime NOT NULL,
  `fecha_subida` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rfc` (`rfc`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `clientes` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.paises
CREATE TABLE IF NOT EXISTS `paises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.personas
CREATE TABLE IF NOT EXISTS `personas` (
  `rfc` varchar(13) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `app` varchar(100) NOT NULL,
  `apm` varchar(100) NOT NULL,
  `fech_nac` date NOT NULL,
  `sex` varchar(1) NOT NULL,
  `id_colonia` int NOT NULL,
  PRIMARY KEY (`rfc`),
  KEY `id_colonia` (`id_colonia`),
  CONSTRAINT `personas_ibfk_1` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.reportes_fugas
CREATE TABLE IF NOT EXISTS `reportes_fugas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc` varchar(13) NOT NULL,
  `foto` mediumblob NOT NULL,
  `mensaje` varchar(500) NOT NULL,
  `atendido` tinyint(1) NOT NULL,
  `id_colonia` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rfc` (`rfc`),
  KEY `id_colonia` (`id_colonia`),
  CONSTRAINT `reportes_fugas_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `clientes` (`rfc`),
  CONSTRAINT `reportes_fugas_ibfk_2` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.sensores_log
CREATE TABLE IF NOT EXISTS `sensores_log` (
  `fecha` datetime NOT NULL,
  `Wifi_MacAddress` varchar(17) NOT NULL,
  `presion` double NOT NULL DEFAULT '0',
  `caudal` double NOT NULL DEFAULT '0',
  `litros_consumidos` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`fecha`),
  KEY `Wifi_MacAddress` (`Wifi_MacAddress`),
  CONSTRAINT `sensores_log_ibfk_1` FOREIGN KEY (`Wifi_MacAddress`) REFERENCES `dispositivos` (`Wifi_MacAddress`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.suspensiones
CREATE TABLE IF NOT EXISTS `suspensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc` varchar(13) NOT NULL,
  `motivo_id` int NOT NULL,
  `duracion_suspension` datetime NOT NULL,
  `fecha` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rfc` (`rfc`),
  KEY `motivo_id` (`motivo_id`),
  CONSTRAINT `suspensiones_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `clientes` (`rfc`),
  CONSTRAINT `suspensiones_ibfk_2` FOREIGN KEY (`motivo_id`) REFERENCES `motivo_suspensiones` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.umbral_clientes
CREATE TABLE IF NOT EXISTS `umbral_clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `min_L` float NOT NULL,
  `max_L` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla okox_pruebas.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `rfc` varchar(13) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `rol` int DEFAULT NULL COMMENT '# 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador, 4 = Compañia',
  `last_session` datetime DEFAULT NULL,
  PRIMARY KEY (`rfc`),
  UNIQUE KEY `rfc` (`rfc`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
