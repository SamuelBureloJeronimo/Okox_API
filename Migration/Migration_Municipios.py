class Migration_Municipios:
    def Table_Municipios():
        return '''
            CREATE TABLE IF NOT EXISTS `municipios` (
            `id` int NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
            `estado` int NOT NULL DEFAULT '0',
            PRIMARY KEY (`id`),
            KEY `index_estado` (`estado`) USING BTREE,
            CONSTRAINT `fk_estado` FOREIGN KEY (`estado`) REFERENCES `estados` (`id`) ON DELETE CASCADE ON UPDATE CASCADE);
            '''