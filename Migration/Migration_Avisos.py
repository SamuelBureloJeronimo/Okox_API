class Migration_Avisos:
    def Table_Avisos():
        return '''
CREATE TABLE IF NOT EXISTS `avisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_admin` int NOT NULL DEFAULT '0',
  `motivo` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `hora_f` datetime NOT NULL,
  `hora_i` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Admin_198437` (`id_admin`) USING BTREE,
  CONSTRAINT `FK_Admin_198437` FOREIGN KEY (`id_admin`) REFERENCES `administradores` (`id`));
'''