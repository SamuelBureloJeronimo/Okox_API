class Migration_Clientes:
    def Table_Clientes():
        return '''
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int UNIQUE NOT NULL,
  `estado_servicio` int DEFAULT 0 NULL,
  `fecha_contratacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_persona_09478` (`id_persona`),
  CONSTRAINT `FK_persona_09478` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`));
'''