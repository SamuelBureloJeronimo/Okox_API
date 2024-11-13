class Migration_Reportes:
    def Table_Reportes():
        return '''
CREATE TABLE IF NOT EXISTS `reportes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `mensaje` varchar(50) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `fecha_subida` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_8345678` (`id_cliente`),
  CONSTRAINT `FK_cliente_8345678` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
'''