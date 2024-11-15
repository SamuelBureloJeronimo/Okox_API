class Migration_Municipios:
    def Table_Municipios():
        return '''
            CREATE TABLE `municipios` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `estado` int(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `index_estado` (`estado`) USING BTREE,
  CONSTRAINT `fk_estado` FOREIGN KEY (`estado`) REFERENCES `estados` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32059 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            '''