class Migration_Estados:
    def Table_Estados():
        return '''
CREATE TABLE `estados` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `pais` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_pais` (`pais`) USING BTREE,
  CONSTRAINT `fk_pais` FOREIGN KEY (`pais`) REFERENCES `paises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            '''