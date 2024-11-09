class Migration_Mantenimientos:
    def Table_Mantenimientos():
        return '''
CREATE TABLE IF NOT EXISTS `mantenimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` text DEFAULT NULL,
  `tiempo_respuesta` time DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `id_colonia` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Colonia_7897` (`id_colonia`) USING BTREE,
  CONSTRAINT `FK_Colonia_7897` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`));
'''