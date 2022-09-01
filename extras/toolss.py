#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel alarma (services.cfg)
#-------------------------------------------------------------------------------
from sys import path, exit as kill
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Alarma import Alarma
#from ngctl.clases.Body import Body
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config,re

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_SRV, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_SRV} {cons.BACK_SRV}')
    c = geto(f'cp -f {cons.TMP_SRV} {cons.DIR}{cons.ORIG_SRV}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_SRV}', extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos Alarma."""
    lista_alarmas = []
    alarma = Alarma()
    regex = re.compile(r'\s+')
    with open (cons.DIR + cons.ORIG_SRV ,'r') as f:
        for i in f:
            i = i.strip()
            if i == '' or i.startswith('#'):
                continue
            elif i.startswith('}'):
                alarma.add_tipo(regex.sub('',alarma.get_valor('define')))
                alarma.del_parametro('define', log=False)
                alarma.ordenar(rev=True)
                lista_alarmas.append(alarma)
                alarma = Alarma()
            else:
                if ',' in i and not i.startswith('check_command'):
                    alarma.add_parametro(_procesar(i,','))
                else: alarma.add_parametro(i.split(maxsplit=1))
    return lista_alarmas

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_alarmas(datos):
    """Devuelve una lista con todos los nombres de hosts."""
    return [x.get_name() for x in datos if x.get_tipo() == 'define host{']

def get_listado_alarmas(datos,host):
    """Devuelve una lista con todos los nombres de las alarmas del host."""
    return [x.get_name() for x in datos if x.get_host() == host and x.get_tipo() == 'define service{']

def get_list_ip_in_alarma(lista,atr,ip,sep):
    """Devuelve un iterable con todos los objetos Alarma que tengan el elemento ip."""
    return filter(lambda x: x.existe_elemento(atr,ip,sep),lista)

def get_frec_host(datos,host):
    """Devuelve el nro de alarmas del host."""
    c = 0
    for i in datos:
        if i.get_host() == host and i.get_tipo() == 'define service{':
            c += 1
    return c

def get_frec_alarma(datos,name,host=None):
    """Devuelve el nro de alarmas del host."""
    c = 0
    if host != None:
        for i in datos:
            if i.get_host() == host and i.get_name() == name and i.get_tipo() == 'define service{':
                c += 1
    else:
        for i in datos:
            if i.get_name() == name and i.get_tipo() == 'define service{':
                c += 1
    return c

def delete_host(datos,host):
    """Elimina las alarmas asociadas al host indicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_host() == host and datos[i].get_tipo() == 'define service{':
            logger.info(f'se elimino la alarma {datos[i].get_name()}', extra=cons.EXTRA)
            del datos[i]
        i += 1

def show_alarma_host(datos,host):
    """Imprime por pantalla las alarmas del host indicado."""
    for i in (x for x in datos if x.get_host() == host and x.get_tipo() == 'define service{'):
        print(i)

def copy_host(datos,old,new,ip, ip_old):
    """Realiza la copia de todas las alarmas del host old hacia el host new."""
    alarma = Alarma()
    for i in range(len(datos)):
        if datos[i].get_host() == old and datos[i].get_tipo() == 'define service{':
            alarma = copiar(datos[i])
            datos.append(alarma)
            datos[-1].add_valor(cons.ID_SRV, datos[-1].get_name().replace(old,new))
            datos[-1].add_valor(cons.ID_HST, new)
            value=''
            lista = datos[-1].get_valor('check_command').split('!')
            b = False
            for k in range(len(lista)):
                if lista[k] == ip_old:
                    lista[k] = ip
                    b = True
            if len(lista) == 1: value = ''.join(lista)
            else: value = '!'.join(lista)
            if b: datos[-1].add_valor('check_command', value)
            logger.info(f'se copio correctamente la alarma {datos[-1].get_name()}', extra=cons.EXTRA)

def copy_alarma(datos,old,new,host=None):
    """Realiza la copia de la alarma old hacia el host new."""
    #copia = Alarma()
    if host != None:
        for i in range(len(datos)):
            if datos[i].get_host() == host and datos[i].get_name() == old and datos[i].get_tipo() == 'define service{':
                copia = copiar(datos[i])
                datos.append(copia)
                name = datos[-1].get_name().replace(datos[-1].get_host(),new)
                datos[-1].add_valor(cons.ID_SRV, name)
                datos[-1].add_valor(cons.ID_HST, new)
                logger.info(f'se copio correctamente {old}/{host} a {name}', extra=cons.EXTRA)
    else:
        for i in range(len(datos)):
            if datos[i].get_name() == old and datos[i].get_tipo() == 'define service{':
                copia = copiar(datos[i])
                datos.append(copia)
                name = datos[-1].get_name().replace(datos[-1].get_host(),new)
                datos[-1].add_valor(cons.ID_SRV, name)
                datos[-1].add_valor(cons.ID_HST, new)
                logger.info(f'se copio correctamente {old} a {name}', extra=cons.EXTRA)

def existe_alarma(datos,name, host=None):
    return get_frec_alarma(datos,name,host) >= 1

def show_alarma(datos,name,host=None):
    """Imprime las alarmas que coinciden con name."""
    if host != None:
        for alarma in (x for x in datos if x.get_host() == host and x.get_name() == name):
            print(alarma)
    else:
        for alarma in (x for x in datos if x.get_name() == name):
            print(alarma)

def get_alarma(datos,name, host=None, log=True):
    """Retorna el objeto Alarma."""
    if host != None:
        for alarma in datos:
            if alarma.get_host() == host and alarma.get_name() == name:
                if log:
                    logger.info(f'se obtuvo la alarma {name} en {host}', extra=cons.EXTRA)
                return alarma
        logger.error(f'no se encontro la alarma {name} en el host {host}, exit..', extra=cons.EXTRA)
    else:
        for alarma in datos:
            if alarma.get_name() == name:
                if log:
                    logger.info(f'se obtuvo la alarma {name}', extra=cons.EXTRA)
                return alarma
        logger.error(f'no se encontro la alarma {name}, exit..', extra=cons.EXTRA)
    kill(254)

def delete_alarma(datos,name,host=None):
    """Elimina las alarma asociadas a name."""
    i = 0
    if host != None:
        while i < len(datos):
            while i < len(datos) and datos[i].get_host() == host and datos[i].get_name() == name and datos[i].get_tipo() == 'define service{':
                del datos[i]
                logger.info(f'se elimino la alarma {name} en {host}', extra=cons.EXTRA)
            i += 1
    else:
        while i < len(datos):
            if datos[i].get_name() == name and datos[i].get_tipo() == 'define service{':
                del datos[i]
                logger.info(f'se elimino la alarma {name}', extra=cons.EXTRA)
                break
            i += 1

def rename_host(datos, host, new):
    for i in range(len(datos)):
        if datos[i].get_host() == host and datos[i].get_tipo() == 'define service{':
            srv = datos[i].get_name().replace(host,new)
            datos[i].add_valor(cons.SRV, srv)
            datos[i].add_valor(cons.HST, new)
            logger.info(f'se renombro {host} a {new} en {cons.ORIG_SRV}', extra=cons.EXTRA)

def get_cantidad(datos):
    """Retorna la cantidad de definiciones de alarma en services.cfg."""
    c = 0
    for i in datos:
        if i.get_tipo() == 'define service{':
            c += 1
    return c

if __name__ == '__main__':
    pass
