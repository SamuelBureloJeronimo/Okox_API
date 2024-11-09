class Migration_Estados:
    def Table_Estados():
        return '''
            CREATE TABLE IF NOT EXISTS `estados` (
            `id` int NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
            `pais` int NOT NULL DEFAULT '0',
            PRIMARY KEY (`id`),
            KEY `index_pais` (`pais`) USING BTREE,
            CONSTRAINT `fk_pais` FOREIGN KEY (`pais`) REFERENCES `paises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE);
            '''