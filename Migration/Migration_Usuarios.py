class Migration_Usuarios:
    def Table_Usuarios():
        return '''
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL,
  `id_persona` int NOT NULL,
  `username` varchar(50) NOT NULL DEFAULT '0',
  `password` varchar(50) NOT NULL DEFAULT '0',
  `token` varchar(250) DEFAULT '0',
  `last_session` datetime,
  KEY `FK_persona_15654` (`id_persona`),
  CONSTRAINT `FK_persona_15654` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
'''