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


-- Volcando estructura de base de datos para u839116441_sgirap
CREATE DATABASE IF NOT EXISTS `u839116441_sgirap` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `u839116441_sgirap`;

-- Volcando estructura para tabla u839116441_sgirap.avisos
CREATE TABLE IF NOT EXISTS `avisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_admin` int NOT NULL DEFAULT '0',
  `motivo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hora_f` datetime NOT NULL,
  `hora_i` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Admin_198437` (`id_admin`) USING BTREE,
  CONSTRAINT `FK_Admin_198437` FOREIGN KEY (`id_admin`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `estado_servicio` int DEFAULT '0',
  `fecha_contratacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_persona` (`id_persona`) USING BTREE,
  KEY `FK_persona_09478` (`id_persona`) USING BTREE,
  CONSTRAINT `FK_persona_09478` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.colonias
CREATE TABLE IF NOT EXISTS `colonias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `ciudad` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `municipio` int DEFAULT NULL,
  `asentamiento` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `codigo_postal` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_municipio` (`municipio`) USING BTREE,
  KEY `index_nombre` (`nombre`) USING BTREE,
  KEY `index_asentamiento` (`asentamiento`) USING BTREE,
  KEY `index_codigo_postal` (`codigo_postal`) USING BTREE,
  KEY `index_ciudad` (`ciudad`) USING BTREE,
  CONSTRAINT `fk_municipio` FOREIGN KEY (`municipio`) REFERENCES `municipios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1607710190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.dispositivos
CREATE TABLE IF NOT EXISTS `dispositivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `Wifi_MacAddress` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_cliente` (`id_cliente`),
  KEY `FK_cliente_904897` (`id_cliente`),
  CONSTRAINT `FK_cliente_904897` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.estados
CREATE TABLE IF NOT EXISTS `estados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `pais` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_pais` (`pais`) USING BTREE,
  CONSTRAINT `fk_pais` FOREIGN KEY (`pais`) REFERENCES `paises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.mantenimientos
CREATE TABLE IF NOT EXISTS `mantenimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `tiempo_respuesta` time DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `id_colonia` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Colonia_7897` (`id_colonia`) USING BTREE,
  CONSTRAINT `FK_Colonia_7897` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.municipios
CREATE TABLE IF NOT EXISTS `municipios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `estado` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_estado` (`estado`) USING BTREE,
  CONSTRAINT `fk_estado` FOREIGN KEY (`estado`) REFERENCES `estados` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32059 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.pagos
CREATE TABLE IF NOT EXISTS `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `monto_pago` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_clientes_1456` (`id_cliente`),
  CONSTRAINT `FK_clientes_1456` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.paises
CREATE TABLE IF NOT EXISTS `paises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.personas
CREATE TABLE IF NOT EXISTS `personas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `app` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `apm` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fech_nac` date NOT NULL,
  `sex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `id_colonia` int DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `id_colonia` (`id_colonia`),
  CONSTRAINT `FK_colonia_8402` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.presion
CREATE TABLE IF NOT EXISTS `presion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `presion` float NOT NULL,
  `id_cliente` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_2782` (`id_cliente`),
  CONSTRAINT `FK_cliente_278` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=432 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.reportes
CREATE TABLE IF NOT EXISTS `reportes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `mensaje` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `fecha_subida` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_8345678` (`id_cliente`),
  CONSTRAINT `FK_cliente_8345678` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.suspensiones
CREATE TABLE IF NOT EXISTS `suspensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(120) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `duracion_dias` int DEFAULT '1',
  `id_cliente` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_Cliente_89892` (`id_cliente`),
  CONSTRAINT `FK_Cliente_89892` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla u839116441_sgirap.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `rol` int NOT NULL DEFAULT '0',
  `token` varchar(350) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `last_session` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_persona` (`id_persona`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `token` (`token`),
  KEY `FK_persona_15654` (`id_persona`),
  CONSTRAINT `FK_persona_15654` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
