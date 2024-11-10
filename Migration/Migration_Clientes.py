class Migration_Clientes:
    def Table_Clientes():
        return '''
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `id_dispositivo` int,
  `estado_servicio` int DEFAULT 0 NULL,
  `fecha_contratacion` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_persona_09478` (`id_persona`),
  KEY `FK_dispositivo_56745` (`id_dispositivo`),
  CONSTRAINT `FK_dispositivo_56745` FOREIGN KEY (`id_dispositivo`) REFERENCES `dispositivos` (`id`),
  CONSTRAINT `FK_persona_09478` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`));
'''