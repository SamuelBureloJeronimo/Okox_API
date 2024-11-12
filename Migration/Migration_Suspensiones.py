class Migration_Suspensiones:
    def Table_Suspensiones():
        return '''
CREATE TABLE IF NOT EXISTS `suspensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(120) DEFAULT NULL,
  `duracion_dias` int DEFAULT 1,
  `id_cliente` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_Cliente_89892` (`id_cliente`),
  CONSTRAINT `FK_Cliente_89892` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
'''