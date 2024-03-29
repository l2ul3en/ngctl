#!/usr/bin/python3
#------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel de timeperiods.cfg
#------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Timeperiod import Timeperiod
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config,re

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_TPE, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_TPE} {cons.BACK_TPE}')
    c = geto(f'cp -f {cons.TMP_TPE} {cons.DIR}{cons.ORIG_TPE}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_TPE}', \
        extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos Timeperiods.
Lee linea a linea el archivo especificado en constantes.py cargando todo las 
definiciones de timeperiods.
Lista -> [{'tipo',[['atributo',valor1'],...,['atributo','valorN']]}]"""
    lista_timeperiod = []
    timeperiod = Timeperiod()
    regex = re.compile(cons.PATRON)
    with open (cons.DIR + cons.ORIG_TPE,'r') as f:
        for i in f:
            #Se eliminan los comentarios que contienen ';'
            if (';' in i):
                i = i[:i.find(';')]
            i = i.strip() #elimina espacios de extremos
            #No se toman en cuenta vacios o comentarios que inician con '#'
            if i == '' or i.startswith('#'):
                continue
            elif i.startswith('}'):
                timeperiod.add_tipo(regex.sub(r'\1', \
                    timeperiod.get_valor('define')))
                timeperiod.del_parametro('define', log=False)
                timeperiod.ordenar(rev=True)
                if timeperiod.existe_atributo(cons.ID_TPE, log=False):
                    lista_timeperiod.append(timeperiod)
                timeperiod = Timeperiod()
            else:
                timeperiod.add_parametro(i.split(maxsplit=1))
    return lista_timeperiod

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_timeperiod(datos,timeperiod,log=True):
    """Retorna el objeto timeperiod."""
    for i in datos:
        if i.get_name() == timeperiod and i.get_tipo() == cons.OB_TPE:
            if log:
                logger.info(f'se obtuvo el timeperiod {timeperiod}', \
                    extra=cons.EXTRA)
            return (True, i)
    logger.error(f'no se encontro el timeperiod {timeperiod}', \
        extra=cons.EXTRA)
    return (False, None)

def delete_timeperiod(datos,timeperiod):
    """Elimina el timeperiod indicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_name() == timeperiod and \
        datos[i].get_tipo() == cons.OB_TPE:
            del datos[i]
            logger.info(f'se elimino el timeperiod {timeperiod}', \
                extra=cons.EXTRA)
        i += 1

def show_timeperiod(datos,timeperiod):
    """Imprime por pantalla la config del timeperiod indicado."""
    for i in (x for x in datos if x.get_name() == timeperiod and \
    x.get_tipo() == cons.OB_TPE):
        print(i)

def copy_timeperiod(datos,old,new):
    """Realiza la copia del timeperiod old para el timeperiod new."""
    timeperiod = Timeperiod()
    for i in range(len(datos)):
        if datos[i].get_name() == old and datos[i].get_tipo() == cons.OB_TPE:
            timeperiod = copiar(datos[i])
            datos.append(timeperiod)
            datos[-1].add_valor(cons.ID_TPE, new)
            logger.info(f'se copio {old} a {new} en {cons.ORIG_TPE}', \
                extra=cons.EXTRA)

def existe_timeperiod(datos,timeperiod):
    """Verifica si el timeperiod existe."""
    for x in datos:
        if x.get_name() == timeperiod and x.get_tipo() == cons.OB_TPE:
            return True
    return False

if __name__ == '__main__':
    pass