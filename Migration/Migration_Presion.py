class Migration_Presion:
    def Table_Presion():
        return '''
CREATE TABLE IF NOT EXISTS `presion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `presion` float NOT NULL,
  `id_cliente` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_2782` (`id_cliente`),
  CONSTRAINT `FK_cliente_278` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=423 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
'''