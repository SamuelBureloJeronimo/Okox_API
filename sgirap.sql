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
CREATE DATABASE IF NOT EXISTS `u839116441_sgirap` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `u839116441_sgirap`;

-- Volcando estructura para tabla u839116441_sgirap.administradores
CREATE TABLE IF NOT EXISTS `administradores` (
  `id` int NOT NULL,
  `fech_alta` date NOT NULL,
  `estado` int DEFAULT '0',
  `id_persona` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Persona_97473` (`id_persona`),
  CONSTRAINT `FK_Persona_97473` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.administradores: ~0 rows (aproximadamente)
DELETE FROM `administradores`;

-- Volcando estructura para tabla u839116441_sgirap.avisos
CREATE TABLE IF NOT EXISTS `avisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_admin` int NOT NULL DEFAULT '0',
  `motivo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hora_f` datetime NOT NULL,
  `hora_i` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Admin_198437` (`id_admin`) USING BTREE,
  CONSTRAINT `FK_Admin_198437` FOREIGN KEY (`id_admin`) REFERENCES `administradores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.avisos: ~0 rows (aproximadamente)
DELETE FROM `avisos`;

-- Volcando estructura para tabla u839116441_sgirap.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `id_dispositivo` int DEFAULT NULL,
  `estado_servicio` varchar(20) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_persona_09478` (`id_persona`),
  KEY `FK_dispositivo_56745` (`id_dispositivo`),
  CONSTRAINT `FK_dispositivo_56745` FOREIGN KEY (`id_dispositivo`) REFERENCES `dispositivos` (`id`),
  CONSTRAINT `FK_persona_09478` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.clientes: ~0 rows (aproximadamente)
DELETE FROM `clientes`;
INSERT INTO `clientes` (`id`, `id_persona`, `id_dispositivo`, `estado_servicio`, `fecha_contratacion`) VALUES
	(10, 11, NULL, '0', '2024-11-09'),
	(11, 12, NULL, '0', '2024-11-09'),
	(12, 13, NULL, '0', '2024-11-09'),
	(13, 14, NULL, '0', '2024-11-09'),
	(14, 15, NULL, '0', '2024-11-09'),
	(15, 16, NULL, '0', '2024-11-09'),
	(16, 17, NULL, '0', '2024-11-09');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.colonias: ~0 rows (aproximadamente)
DELETE FROM `colonias`;
INSERT INTO `colonias` (`id`, `nombre`, `ciudad`, `municipio`, `asentamiento`, `codigo_postal`) VALUES
	(1, 'Josefa ortiz de Dominguez', 'Macuspana', 1, 'La josefa', 86709);

-- Volcando estructura para tabla u839116441_sgirap.dispositivos
CREATE TABLE IF NOT EXISTS `dispositivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Wifi_MacAddress` varchar(18) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.dispositivos: ~0 rows (aproximadamente)
DELETE FROM `dispositivos`;
INSERT INTO `dispositivos` (`id`, `Wifi_MacAddress`) VALUES
	(1, 'B0:A7:32:14:C0:8C');

-- Volcando estructura para tabla u839116441_sgirap.estados
CREATE TABLE IF NOT EXISTS `estados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `pais` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_pais` (`pais`) USING BTREE,
  CONSTRAINT `fk_pais` FOREIGN KEY (`pais`) REFERENCES `paises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.estados: ~0 rows (aproximadamente)
DELETE FROM `estados`;
INSERT INTO `estados` (`id`, `nombre`, `pais`) VALUES
	(1, 'Tabasco', 1);

-- Volcando estructura para tabla u839116441_sgirap.mantenimientos
CREATE TABLE IF NOT EXISTS `mantenimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` text,
  `tiempo_respuesta` time DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `id_colonia` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Colonia_7897` (`id_colonia`) USING BTREE,
  CONSTRAINT `FK_Colonia_7897` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.mantenimientos: ~0 rows (aproximadamente)
DELETE FROM `mantenimientos`;

-- Volcando estructura para tabla u839116441_sgirap.municipios
CREATE TABLE IF NOT EXISTS `municipios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `estado` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_estado` (`estado`) USING BTREE,
  CONSTRAINT `fk_estado` FOREIGN KEY (`estado`) REFERENCES `estados` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.municipios: ~0 rows (aproximadamente)
DELETE FROM `municipios`;
INSERT INTO `municipios` (`id`, `nombre`, `estado`) VALUES
	(1, 'Macuspana', 1);

-- Volcando estructura para tabla u839116441_sgirap.pagos
CREATE TABLE IF NOT EXISTS `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `monto_pago` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_clientes_1456` (`id_cliente`),
  CONSTRAINT `FK_clientes_1456` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.pagos: ~0 rows (aproximadamente)
DELETE FROM `pagos`;

-- Volcando estructura para tabla u839116441_sgirap.paises
CREATE TABLE IF NOT EXISTS `paises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.paises: ~0 rows (aproximadamente)
DELETE FROM `paises`;
INSERT INTO `paises` (`id`, `nombre`) VALUES
	(1, 'México');

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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.personas: ~0 rows (aproximadamente)
DELETE FROM `personas`;
INSERT INTO `personas` (`id`, `nombre`, `app`, `apm`, `fech_nac`, `sex`, `id_colonia`) VALUES
	(11, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(12, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(13, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(14, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(15, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(16, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1),
	(17, 'Samuel', 'Burelos', 'Jerónimo', '2003-08-06', 'Masculino', 1);

-- Volcando estructura para tabla u839116441_sgirap.presion
CREATE TABLE IF NOT EXISTS `presion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `presion` float NOT NULL,
  `id_cliente` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_2782` (`id_cliente`),
  CONSTRAINT `FK_cliente_278` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=426 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla u839116441_sgirap.presion: ~0 rows (aproximadamente)
DELETE FROM `presion`;

-- Volcando estructura para tabla u839116441_sgirap.reportes
CREATE TABLE IF NOT EXISTS `reportes` (
  `id` int NOT NULL,
  `id_cliente` int NOT NULL,
  `mensaje` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_cliente_8345678` (`id_cliente`),
  CONSTRAINT `FK_cliente_8345678` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla u839116441_sgirap.reportes: ~0 rows (aproximadamente)
DELETE FROM `reportes`;

-- Volcando estructura para tabla u839116441_sgirap.suspensiones
CREATE TABLE IF NOT EXISTS `suspensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `motivo_suspension` varchar(120) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `duracion_suspension` time DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Cliente_89892` (`id_cliente`),
  CONSTRAINT `FK_Cliente_89892` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla u839116441_sgirap.suspensiones: ~0 rows (aproximadamente)
DELETE FROM `suspensiones`;

-- Volcando estructura para tabla u839116441_sgirap.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `username` varchar(50) NOT NULL DEFAULT '0',
  `password` varchar(50) NOT NULL DEFAULT '0',
  `rol` int DEFAULT '0',
  `token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `last_session` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_persona_15654` (`id_persona`),
  CONSTRAINT `FK_persona_15654` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla u839116441_sgirap.usuarios: ~0 rows (aproximadamente)
DELETE FROM `usuarios`;
INSERT INTO `usuarios` (`id`, `id_persona`, `username`, `password`, `rol`, `token`, `last_session`) VALUES
	(1, 11, '$[y_Samuel', '$~VVU\'tE', 0, '', NULL),
	(2, 12, 'OjR_Samuel', 'EE(Q}:@+', 0, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTIwNzMwOCwianRpIjoiYzMwOWNkNTQtNjRhMi00NTM4LTkyNDUtYzEyNWRiMTc1ZDZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ik9qUl9TYW11ZWwiLCJuYmYiOjE3MzEyMDczMDgsImNzcmYiOiJjYTg1YmFjYy03ODNmLTRiYzgtOTE1Mi0xYWY1NjQ5ODlmMDEiLCJleHAiOjE3MzEyMDkxMDgsInJvbGUiOjB9.pBzTXxus3kAzba1qKmufaXmrZiUlx-t4FEv_fZNLtL0', '2024-11-09 20:55:08'),
	(3, 13, 'NcGw_Samuel', '(*Xk|^<P', 0, '', NULL),
	(4, 14, 'OqOY_Samuel', '6NUWcjFG', 0, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTIwNzIzNiwianRpIjoiYjE5MTRmNTItMGEwNC00ZTY4LTk3MzctODhhZTYzZDgwMmM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ik9xT1lfU2FtdWVsIiwibmJmIjoxNzMxMjA3MjM2LCJjc3JmIjoiMGM1MTUzYTEtMWQwNC00ZGI1LWFkZjEtZDQ1YjM5ZGIyZGM1IiwiZXhwIjoxNzMxMjA5MDM2LCJyb2xlIjowfQ.XK81AJjDGVFKGO-wADFCbGaYXf-p2RoESlGrVFU1cMw', '2024-11-09 20:53:56'),
	(5, 15, 'rhZF_Samuel', 'NDOF7Wmc', 0, NULL, NULL),
	(6, 16, '93Qe_Samuel', 'kZL2Vzmh', 3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTIwNzI3NCwianRpIjoiOWQyNjM3ZGQtNzIwZS00YzQzLWIxMDQtZjI3ODRjYjJmNjMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkzUWVfU2FtdWVsIiwibmJmIjoxNzMxMjA3Mjc0LCJjc3JmIjoiOTY4NzMzZWUtMGI4OS00ZWMyLWI5MmYtZDg3NmZjYTJmNDllIiwiZXhwIjoxNzMxMjA5MDc0LCJyb2xlIjozfQ._I--rdpcotEQ0K1MoNxrHfTMoTR49MQ-j_Z1df-dkzM', '2024-11-09 20:54:34'),
	(7, 17, 'wfdd_Samuel', 'TrnQDuCT', 0, NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
