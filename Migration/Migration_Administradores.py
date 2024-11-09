class Migration_Administradores:
    def Table_Administradores():
        return '''
CREATE TABLE IF NOT EXISTS `administradores` (
  `id` int NOT NULL,
  `fech_alta` date NOT NULL,
  `estado` int DEFAULT 0,
  `id_persona` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Persona_97473` (`id_persona`),
  CONSTRAINT `FK_Persona_97473` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`));
'''