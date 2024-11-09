class Migration_Paises:
    def Table_Paises():
        return '''
            CREATE TABLE IF NOT EXISTS `paises` (
            `id` int NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
            PRIMARY KEY (`id`));
            '''