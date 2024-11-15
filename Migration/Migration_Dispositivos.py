class Migration_Dispositivos:
    def Table_Dispositivos():
        return '''
CREATE TABLE IF NOT EXISTS `dispositivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int UNIQUE NOT NULL,
  `Wifi_MacAddress` varchar(18) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_cliente_904897` (`id_cliente`),
  CONSTRAINT `FK_cliente_904897` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`));
'''