class Migration_Paises:
    def Table_Paises():
        return '''
            CREATE TABLE `paises` (
            `id` int(3) NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            '''