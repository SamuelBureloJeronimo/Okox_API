class Migration_Personas:
    def Table_Personas():
        return '''
            CREATE TABLE IF NOT EXISTS `personas` (
            `id` int NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
            `app` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
            `apm` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
            `fech_nac` date NOT NULL,
            `sex` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
            `id_colonia` int DEFAULT '0',
            PRIMARY KEY (`id`) USING BTREE,
            KEY `id_colonia` (`id_colonia`),
            CONSTRAINT `FK_colonia_8402` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`));
            '''