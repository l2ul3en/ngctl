#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel de hosts.cfg 
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Host import Host
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config,re

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_HST, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_HST} {cons.BACK_HST}')
    c = geto(f'cp -f {cons.TMP_HST} {cons.DIR}{cons.ORIG_HST}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_HST}', extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos Host.

Lee linea a linea el archivo especificado en constantes.py cargando todo las definiciones de hosts.
Lista     ->  [['host_name',['atributo valor1',...,'atributo valorN']]]"""
    lista_hosts = []
    host = Host()
    regex = re.compile(r'\s+')
    with open (cons.DIR + cons.ORIG_HST,'r') as f:
        for i in f:
            #Se eliminan los comentarios que empiezan por '#' o ';'
            if ('#' in i):
                i = i[:i.find('#')]
            if (';' in i):
                i = i[:i.find(';')]
            i = i.strip()
            if i == '':
                continue
            elif i.startswith('}'):
                host.add_tipo(regex.sub('',host.get_valor('define')))
                host.del_parametro('define',log=False)
                host.ordenar(rev=True)
                lista_hosts.append(host)
                host = Host()
            else:
                if ',' in i:
                    host.add_parametro(_procesar(i,','))
                else: host.add_parametro(i.split(maxsplit=1))
    return lista_hosts

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_host(datos,host, log=True):
    """Retorna el objeto Host."""
    for i in datos:
        if i.get_name() == host and i.get_tipo() == 'define host{':
            if log:
                logger.info(f'se obtuvo el host {host}', extra=cons.EXTRA)
            return i
    logger.error(f'no se encontro el host {host}, exit..', extra=cons.EXTRA)
    raise SystemExit(2)

def get_parametro_in_host(datos, atributo, name):
    """Devuelve un iterable con todos los objetos host a los que pertenece name."""
    return filter(lambda x: x.existe_elemento(atributo, name), datos)

def delete_host(datos,host):
    """Elimina las alarmas asociadas al host inidicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_name() == host and datos[i].get_tipo() == 'define host{':
            del datos[i]
            logger.info(f'se elimino el host {host}', extra=cons.EXTRA)
        i += 1

def show_host(datos,host):
    """Imprime por pantalla la config del host indicado."""
    for i in (x for x in datos if x.get_name() == host and x.get_tipo() == 'define host{'):
        print(i)

def copy_host(datos,old,new,ip=None):
    """Realiza la copia de todas las alarmas del host old hacia el host new."""
    host = Host()
    for i in range(len(datos)):
        if datos[i].get_name() == old and datos[i].get_tipo() == 'define host{':
            host = copiar(datos[i])
            datos.append(host)
            datos[-1].add_valor(cons.ID_HST, new)
            datos[-1].add_valor('alias',new)
            if ip != None:
                datos[-1].add_valor('address',ip)
            logger.info(f'se copio {old} a {new} en {cons.ORIG_HST}', extra=cons.EXTRA)

def existe_host(datos,host):
    """Verifica si el host existe"""
    for x in datos:
        if x.get_name() == host and x.get_tipo() == 'define host{':
            return True
    return False

def rename_host(datos, host, new):
    for i in range(len(datos)):
        if datos[i].get_name() == host and datos[i].get_tipo() == 'define host{':
            datos[i].add_valor(cons.ID_HST, new)
            datos[i].add_valor('alias',new)
            logger.info(f'se actualizo el nombre de {host} a {new} en {cons.ORIG_HST}', extra=cons.EXTRA)

def get_cantidad(datos):
    """Retorna la cantidad de definiciones host en Hosts.cfg."""
    c = 0
    for i in datos:
        if i.get_tipo() == 'define host{':
            c += 1
    return c

if __name__ == '__main__':
    pass
