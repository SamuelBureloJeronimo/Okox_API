class Migration_Colonias:
    def Table_Colonias():
        return '''
  CREATE TABLE `colonias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `ciudad` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `municipio` int(6) DEFAULT NULL,
  `asentamiento` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `codigo_postal` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_municipio` (`municipio`) USING BTREE,
  KEY `index_nombre` (`nombre`) USING BTREE,
  KEY `index_asentamiento` (`asentamiento`) USING BTREE,
  KEY `index_codigo_postal` (`codigo_postal`) USING BTREE,
  KEY `index_ciudad` (`ciudad`) USING BTREE,
  CONSTRAINT `fk_municipio` FOREIGN KEY (`municipio`) REFERENCES `municipios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1607710190 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

            '''