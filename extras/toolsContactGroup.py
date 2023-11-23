#!/usr/bin/python3
#------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel de contactgroups.cfg 
#------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.ContactGroup import ContactGroup
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config,re

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_CGR, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_CGR} {cons.BACK_CGR}')
    c = geto(f'cp -f {cons.TMP_CGR} {cons.DIR}{cons.ORIG_CGR}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_CGR}', extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos ContactGroups.
Lee linea a linea el archivo especificado en constantes.py cargando todo las 
definiciones de contactgroups.
Lista -> [{'tipo',[['atributo', 'valor1'],...,['atributo', 'valorN']}]."""
    lista_contactgroup = []
    contactgroup = ContactGroup()
    regex = re.compile(cons.PATRON)
    with open (cons.DIR + cons.ORIG_CGR,'r') as f:
        for i in f:
            #Se eliminan los comentarios que contienen ';'
            if (';' in i):
                i = i[:i.find(';')]
            i = i.strip() #elimina espacios de extremos
            #No se toman en cuenta vacios o comentarios que inician con '#'
            if i == '' or i.startswith('#'):
                continue
            elif i.startswith('}'):
                contactgroup.add_tipo(regex.sub(r'\1',\
                    contactgroup.get_valor('define')))
                contactgroup.del_parametro('define', log=False)
                contactgroup.ordenar()
                if contactgroup.existe_atributo(cons.ID_CGR,log=False):
                    lista_contactgroup.append(contactgroup)
                contactgroup = ContactGroup()
            else:
                if ',' in i:
                    contactgroup.add_parametro(_procesar(i,','))
                else: contactgroup.add_parametro(i.split(maxsplit=1))
    return lista_contactgroup

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_parametro_in_contactgroup(datos,atributo, name):
    """Devuelve un iterable con todos los objetos contactgroup a los que 
    pertenece name."""
    return filter(lambda x: x.existe_elemento(atributo, name) and \
    x.get_tipo() == cons.OB_CGR, datos)

def get_contactgroup(datos,contactgroup,log=True):
    """Retorna el objeto contactgroup."""
    for i in datos:
        if i.get_name() == contactgroup and i.get_tipo() == cons.OB_CGR:
            if log:
                logger.info(f'se obtuvo el contactgroup {contactgroup}', \
                    extra=cons.EXTRA)
            return (True, i)
    logger.error(f'no se encontro el contactgroup {contactgroup}', \
        extra=cons.EXTRA)
    return (False, None)

def delete_contactgroup(datos,contactgroup):
    """Elimina el contactgroup indicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_name() == contactgroup and \
        datos[i].get_tipo() == cons.OB_CGR:
            del datos[i]
            logger.info(f'se elimino el contactgroup {contactgroup}', \
                extra=cons.EXTRA)
        i += 1

def show_contactgroup(datos,contactgroup):
    """Imprime por pantalla la config del contactgroup indicado."""
    for i in (x for x in datos if x.get_name() == contactgroup and \
    x.get_tipo() == cons.OB_CGR):
        print(i)

def copy_contactgroup(datos,old,new):
    """Realiza la copia del contactgroup old para el contactgroup new."""
    contactgroup = ContactGroup()
    for i in range(len(datos)):
        if datos[i].get_name() == old and datos[i].get_tipo() == cons.OB_CGR:
            contactgroup = copiar(datos[i])
            datos.append(contactgroup)
            datos[-1].add_valor(cons.ID_CGR,new)
            logger.info(f'se copio {old} a {new} en {cons.ORIG_CGR}', \
                extra=cons.EXTRA)

def existe_contactgroup(datos,contactgroup):
    """Verifica si el contactgroup existe."""
    for x in datos:
        if x.get_name() == contactgroup and x.get_tipo() == cons.OB_CGR:
            return True
    return False


if __name__ == '__main__':
    pass