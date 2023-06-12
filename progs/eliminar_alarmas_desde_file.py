import sys
sys.path.append('/data/source/')
import ngctl.config.constantes as cons
import ngctl.extras.toolss as tser
import logging,logging.config


archivo = sys.argv[1]

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

lista_alarmas = tser.cargar()
lista_alarmas.sort()
cantidad_antes = len(lista_alarmas)
with open(archivo, 'r') as lista_eliminar:
    for alarma in lista_eliminar:
        tser.delete_alarma(lista_alarmas, alarma)
tser.aplicar_cambios(lista_alarmas)
logger.info(f'Se eliminaron {cantidad_antes - len(lista_alarmas)} \
            alarmas de {cantidad_antes} - actual: {len(lista_alarmas)}', \
                extra=cons.EXTRA)
