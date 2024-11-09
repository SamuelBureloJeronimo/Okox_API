class Migration_Pagos:
    def Table_Pagos():
        return '''
CREATE TABLE IF NOT EXISTS `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `monto_pago` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_clientes_1456` (`id_cliente`),
  CONSTRAINT `FK_clientes_1456` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`));
'''