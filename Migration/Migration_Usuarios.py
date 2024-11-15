class Migration_Usuarios:
    def Table_Usuarios():
        return '''
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL UNIQUE,
  `username` varchar(50) NOT NULL DEFAULT '0' UNIQUE,
  `password` varchar(50) NOT NULL DEFAULT '0',
  `rol` int NOT NULL DEFAULT '0',
  `token` varchar(350) UNIQUE,
  `last_session` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_persona_15654` (`id_persona`),
  CONSTRAINT `FK_persona_15654` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
'''