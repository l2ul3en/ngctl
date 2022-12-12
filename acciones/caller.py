#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Invocar funciones que realicen tareas especificas
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
import ngctl.extras.toolss as tser
import ngctl.extras.toolsh as thos
import ngctl.extras.toolsg as thgr
import ngctl.extras.toolsCommand as tcmd
import ngctl.extras.toolsContact as tcnt
import ngctl.extras.toolsContactGroup as tcgr
import ngctl.extras.toolsTimeperiod as ttpe
import ngctl.clases #necesario para modulo search y export
import logging, logging.config, re, csv, errno
from subprocess import getoutput as geto

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def cargar_alarmas():
    return tser.cargar()

def get_cantidad_alarmas(datos):
    return tser.get_cantidad(datos)

def renombrar_servicio(lalarmas, old, new, host=None):
    modificar_atributo(lalarmas, old, cons.ID_SRV, new, host)
  
def modificar_atributo(lista, key, atributo, new, host=None):
    logger.info('iniciando modificar_atributo', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key, host):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista,key, host)
        if alarma.existe_atributo(atributo):
            alarma.add_valor(atributo, new)
            tser.aplicar_cambios(lista)
        else: 
            if host != None: logger.warning(f'no existe el atributo {atributo} en el host {host}', extra=cons.EXTRA)
            else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo', extra=cons.EXTRA)

def mostrar_alarma(lista, alarma, host=None):
    logger.info('iniciando mostrar_alarma', extra=cons.EXTRA)
    if tser.existe_alarma(lista, alarma, host):
            tser.show_alarma(lista,alarma, host)
            logger.info(f'se visualizo {alarma}', extra=cons.EXTRA)
    else:
            if host != None: logger.warning(f'no se encontro la alarma {alarma} definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
            else: logger.warning(f'no se encontro la alarma {alarma} definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_alarma', extra=cons.EXTRA)

def eliminar_alarma(lista, key, host=None):
    logger.info('iniciando eliminar_alarma', extra=cons.EXTRA)
    if tser.existe_alarma(lista, key, host):
        tser.delete_alarma(lista, key, host)
        tser.aplicar_cambios(lista)
    else:
        if host != None: logger.warning(f'no se encontro la alarma {key} definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'no se encontro la alarma {key} definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_alarma', extra=cons.EXTRA)

def copiar_servicio(lista, key, new, host=None):
    logger.info('iniciando copiar_servicio', extra=cons.EXTRA)
    if tser.existe_alarma(lista, key, host):
        tser.copy_alarma(lista, key, new, host)
        tser.aplicar_cambios(lista)
    else:
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    logger.info('finalizando copiar_servicio', extra=cons.EXTRA)

def eliminar_atributo(lista,key, atributo, host=None):
    logger.info('iniciando eliminar_atributo', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key, host):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista, key, host)
        if alarma.existe_atributo(atributo):
            alarma.del_parametro(atributo)
            tser.aplicar_cambios(lista)
        else:
            if host != None: logger.warning(f'no existe el atributo {atributo} en el host {host}', extra=cons.EXTRA)
            else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo', extra=cons.EXTRA)

def eliminar_elemento(lista, key, atributo, dato, host=None): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key, host):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista, key, host)
        if alarma.existe_atributo(atributo):
            if alarma.existe_elemento(atributo, dato):
                alarma.del_elemento(atributo, dato)
                tser.aplicar_cambios(lista)
            else: logger.warning(f'no existe el elemento {dato}', extra=cons.EXTRA)
        else:
            if host != None: logger.warning(f'no existe el atributo {atributo} en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
            else: logger.warning(f'no existe el atributo {atributo} en la alarma {key}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento', extra=cons.EXTRA)

def agregar_elemento(lista, key, atributo, dato, host=None): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista,key, host)
        if alarma.existe_atributo(atributo):
            if not alarma.existe_elemento(atributo, dato):
                alarma.add_elemento(atributo, dato)
                tser.aplicar_cambios(lista)
            else: 
                if host != None: logger.warning(f'ya existe el elemento {dato} en la alarma {key} del host {host}', extra=cons.EXTRA)
                else: logger.warning(f'ya existe el elemento {dato} en {key}', extra=cons.EXTRA)
        else:
            alarma.add_parametro([atributo, dato])
            if host != None: logger.info(f'se agrego {atributo} {dato} en la alarma {alarma} del host {host}', extra=cons.EXTRA)
            else: logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista)
    logger.info('finalizando agregar_elemento', extra=cons.EXTRA)

def agregar_parametro(lista, key, atributo, valor, host=None):
    logger.info('iniciando agregar_parametro', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key, host):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista, key, host)
        if not alarma.existe_atributo(atributo):
            alarma.add_parametro([atributo,valor])
            if host != None: logger.info(f'se agrego {atributo} {valor} en el host {host}', extra=cons.EXTRA)
            else: logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista)
        else: logger.warning(f'ya existe el atributo {atributo} en {key}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro', extra=cons.EXTRA)

def mostrar_atributo(lista, key, atributo, host=None):
    logger.info('iniciando mostrar_atributo', extra=cons.EXTRA)
    if not tser.existe_alarma(lista, key):
        if host != None: logger.warning(f'la alarma {key} no esta definida en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        else: logger.warning(f'la alarma {key} no esta definida en {cons.ORIG_SRV}', extra=cons.EXTRA)
    else:
        alarma = tser.get_alarma(lista, key, host)
        if alarma.existe_atributo(atributo):
            print(alarma.get_valor(atributo))
        else: 
            if host != None: logger.warning(f'no existe el atributo {atributo} en el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
            logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_host', extra=cons.EXTRA)

#Metodos de HOST

def cargar_hosts():
    return thos.cargar()

def mostrar_listado_servicios(lalarmas, lhosts, host):
    logger.info('iniciando mostrar_listado_servicios', extra=cons.EXTRA)
    if thos.existe_host(lhosts,host):
        c = 0
        try:
            for i in tser.get_listado_alarmas(lalarmas,host):
                print(i)
                c += 1
        except IOError as e:
            if e.errno == errno.EPIPE: pass
        logger.info(f'se visualizo {c} alarmas asociadas al host {host}', extra=cons.EXTRA) 
    else:
        logger.warning(f'{host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_listado_servicios', extra=cons.EXTRA)

def reporte_host(lalarmas, lhosts, host, verbose):
    logger.info('iniciando reporte_host', extra=cons.EXTRA)
    if thos.existe_host(lhosts, host):
        frec = tser.get_frec_host(lalarmas, host)
        if verbose:
            tser.show_alarma_host(lalarmas, host)
        logger.info(f'se tiene {frec} alarmas configuradas para el host {host} en {cons.ORIG_SRV}', extra=cons.EXTRA)
        print(f'se tiene {frec} alarmas configuradas para el host {host} en {cons.ORIG_SRV}')
    else: logger.warning(f'no existe definicion de {host} en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando reporte_host', extra=cons.EXTRA)

def renombrar_host(lalarmas, lhostgroups, lhosts, host, new, verbose):
    logger.info('iniciando renombrar_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, host):
        logger.warning(f'no existe definicion de {host} en {cons.ORIG_HST}', extra=cons.EXTRA)
    elif thos.existe_host(lhosts, new):
        logger.warning(f'el host {new} ya existe en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        frec = 0
        for i in thgr.get_list_host_in_group(lhostgroups,host):
            i.rename_elemento('members', host, new, log=False)
            frec += 1
        if frec > 0:
            logger.info(f'se modifico {frec} grupos en {cons.ORIG_HGR}', extra=cons.EXTRA)
            thgr.aplicar_cambios(lhostgroups)
        frec = tser.get_frec_host(lalarmas, host)
        if frec > 0:
            tser.rename_host(lalarmas, host, new)
            tser.aplicar_cambios(lalarmas)
        if frec > 0:
            logger.info(f'se modifico {frec} alarmas en {cons.ORIG_SRV}', extra=cons.EXTRA)
            if verbose: tser.show_alarma_host(lalarmas, new)
        thos.rename_host(lhosts, host, new)
        thos.aplicar_cambios(lhosts)
    logger.info('finalizando renombrar_host', extra=cons.EXTRA)

def copiar_host(lalarmas, lhosts, host, new, ip):
    logger.info('iniciando copiar_host', extra=cons.EXTRA)
    if thos.existe_host(lhosts, host):
        if not thos.existe_host(lhosts, new):
            hostname = thos.get_host(lhosts,host)
            ip_old = hostname.get_valor('address')
            if ip == ip_old:
                logger.info(f'la IP {ip} anterior y nueva son iguales', extra=cons.EXTRA)
            tser.copy_host(lalarmas, host, new,ip, ip_old)
            thos.copy_host(lhosts, host, new,ip)
            tser.aplicar_cambios(lalarmas)
            thos.aplicar_cambios(lhosts)
        else: logger.warning(f'el host {new} ya existe en {cons.ORIG_HST}, proceder a adicionar manualmente', extra=cons.EXTRA)
    else: logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando copiar_host', extra=cons.EXTRA)

def eliminar_host(lalarmas, lhosts, lgrupos, host):
    logger.info('iniciando eliminar_host', extra=cons.EXTRA)
    if thos.existe_host(lhosts, host):
        frec = tser.get_frec_host(lalarmas,host)
        if frec > 0:
            tser.delete_host(lalarmas, host)
            tser.aplicar_cambios(lalarmas)
        thos.delete_host(lhosts, host)
        thos.aplicar_cambios(lhosts)
        b = False
        for i in thgr.get_list_host_in_group(lgrupos,host):
            i.del_elemento('members',host)
            logger.info(f'se elimino el host {host} del grupo {i.get_name()}', extra=cons.EXTRA)
            b = True
        if b: thgr.aplicar_cambios(lgrupos)
    else: logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_host', extra=cons.EXTRA)

def mostrar_host(lista, host):
    logger.info('iniciando mostrar_host', extra=cons.EXTRA)
    if thos.existe_host(lista, host):
        thos.show_host(lista,host)
        logger.info(f'se visualizo {host}', extra=cons.EXTRA)
    else: logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_host', extra=cons.EXTRA)

def mostrar_listado_hostgroup(lhost, lhostgroups, host):
    logger.info('iniciando mostrar_listado_hostgroup', extra=cons.EXTRA)
    if thos.existe_host(lhost, host):
        c = 0
        for i in thgr.get_list_host_in_group(lhostgroups,host):
            print (i.get_name())
            c += 1
        logger.info(f'se visualizo {c} grupos asociados al host {host}', extra=cons.EXTRA)
    else: logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_listado_hostgroup', extra=cons.EXTRA)

def eliminar_atributo_host(lhosts,host, atributo):
    logger.info('iniciando eliminar_atributo_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, host):
        logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts, host)
        if hostname.existe_atributo(atributo):
            hostname.del_parametro(atributo)
            thos.aplicar_cambios(lhosts)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_host', extra=cons.EXTRA)

def modificar_atributo_host(lhosts, key, atributo, new):
    logger.info('iniciando modificar_atributo_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, key):
        logger.warning(f'el host {key} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts,key)
        if hostname.existe_atributo(atributo):
            hostname.add_valor(atributo, new)
            thos.aplicar_cambios(lhosts)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_host', extra=cons.EXTRA)

def agregar_parametro_host(lhosts, key, atributo, valor):
    logger.info('iniciando agregar_parametro_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, key):
        logger.warning(f'el host {key} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts,key)
        if not hostname.existe_atributo(atributo):
            hostname.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            thos.aplicar_cambios(lhosts)
        else: logger.warning(f'ya existe el atributo {atributo} en {key}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_host', extra=cons.EXTRA)

def eliminar_elemento_host(lhosts, key, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, key):
        logger.warning(f'el host {key} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts, key)
        if hostname.existe_atributo(atributo):
            if hostname.existe_elemento(atributo, dato):
                hostname.del_elemento(atributo, dato)
                thos.aplicar_cambios(lhosts)
            else: logger.warning(f'no existe el elemento {dato} en {key}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {key}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_host', extra=cons.EXTRA)

def agregar_elemento_host(lhosts, key, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, key):
        logger.warning(f'el host {key} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts,key)
        if hostname.existe_atributo(atributo):
            if not hostname.existe_elemento(atributo, dato):
                hostname.add_elemento(atributo, dato)
                thos.aplicar_cambios(lhosts)
            else: logger.warning(f'ya existe el elemento {dato} en {key}', extra=cons.EXTRA)
        else:
            hostname.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            thos.aplicar_cambios(lhosts)
    logger.info('finalizando agregar_elemento_host', extra=cons.EXTRA)

def mostrar_atributo_host(lhosts, host, atributo):
    logger.info('iniciando mostrar_atributo_host', extra=cons.EXTRA)
    if not thos.existe_host(lhosts, host):
        logger.warning(f'el host {host} no esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        hostname = thos.get_host(lhosts, host)
        if hostname.existe_atributo(atributo):
            print(hostname.get_valor(atributo))
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_host', extra=cons.EXTRA)

#Metodos para Hostgroups

def cargar_hostgroups():
    return thgr.cargar()

def get_cantidad_hosts(datos):
    return thos.get_cantidad(datos)

def duplicar_hostgroup(lhostgroups, grupo, new):
    logger.info('iniciando duplicar_hostgroup', extra=cons.EXTRA)
    if thgr.existe_hostgroup(lhostgroups, grupo):
        if not thgr.existe_hostgroup(lhostgroups, new):
            thgr.copy_hostgroup(lhostgroups, grupo, new)
            thgr.aplicar_cambios(lhostgroups)
        else: logger.warning(f'el hostgroup {new} ya existe en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else: logger.warning(f'el hostgroup {grupo} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    logger.info('finalizando duplicar_hostgroup', extra=cons.EXTRA)

def mostrar_hostgroup(lista, grupo):
    logger.info('iniciando mostrar_hostgroup', extra=cons.EXTRA)
    if thgr.existe_hostgroup(lista, grupo):
        thgr.show_hostgroup(lista,grupo)
        logger.info(f'se visualizo {grupo}', extra=cons.EXTRA)
    else: logger.warning(f'no se encontro el hostgroup {grupo} definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_hostgroup', extra=cons.EXTRA)

def eliminar_hostgroup(lhostgroups, grupo):
    logger.info('iniciando eliminar_hostgroup', extra=cons.EXTRA)
    if thgr.existe_hostgroup(lhostgroups, grupo):
        thgr.delete_hostgroup(lhostgroups, grupo)
        thgr.aplicar_cambios(lhostgroups)
    else: logger.warning(f'el grupo {grupo} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_hostgroup', extra=cons.EXTRA)

def renombrar_hostgroup(lhostgroups, grupo, new):
    modificar_atributo_grupo(lhostgroups, grupo, cons.ID_HGR, new)

def mostrar_listado_hosts(lhostgroups, grupo):
    logger.info('iniciando mostrar_listado_hosts', extra=cons.EXTRA)
    hostgroup = thgr.get_hostgroup(lhostgroups,grupo)
    if hostgroup.existe_atributo('members'):
        try:
            for i in thgr.get_listado_hosts(lhostgroups,grupo):
                c = 0
                for j in i.split(','):
                    print(j)
                    c += 1
                logger.info(f'se visualizo {c} hosts asociados al grupo {grupo}', extra=cons.EXTRA)
        except IOError as e:
            if e.errno == errno.EPIPE: pass
    else: logger.warning(f'no existe el atributo members en el grupo {hostgroup.get_name()}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_listado_hosts', extra=cons.EXTRA)

def eliminar_atributo_grupo(lhostgroups,hostgroup, atributo):
    logger.info('iniciando eliminar_atributo_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, hostgroup):
        logger.warning(f'el grupo {hostgroup} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups, hostgroup)
        if grupo.existe_atributo(atributo):
            grupo.del_parametro(atributo)
            thgr.aplicar_cambios(lhostgroups)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_grupo', extra=cons.EXTRA)

def agregar_parametro_grupo(lhostgroups, key, atributo, valor):
    logger.info('iniciando agregar_parametro_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, key):
        logger.warning(f'el grupo {key} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups,key)
        if not grupo.existe_atributo(atributo):
            grupo.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            thgr.aplicar_cambios(lhostgroups)
        else: logger.warning(f'ya existe el atributo {atributo} en {key}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_grupo', extra=cons.EXTRA)

def modificar_atributo_grupo(lhostgroups, key, atributo, new):
    logger.info('iniciando modificar_atributo_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, key):
        logger.warning(f'el grupo {key} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups,key)
        if grupo.existe_atributo(atributo):
            grupo.add_valor(atributo,new)
            thgr.aplicar_cambios(lhostgroups)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_grupo', extra=cons.EXTRA)

def agregar_elemento_grupo(lhostgroups, key, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, key):
        logger.warning(f'el grupo {key} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups,key)
        if grupo.existe_atributo(atributo):
            if not grupo.existe_elemento(atributo, dato):
                grupo.add_elemento(atributo, dato)
                thgr.aplicar_cambios(lhostgroups)
            else: logger.warning(f'ya existe el elemento {dato} en {key}', extra=cons.EXTRA)
        else:
            grupo.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            thgr.aplicar_cambios(lhostgroups)
    logger.info('finalizando agregar_elemento_grupo', extra=cons.EXTRA)

def eliminar_elemento_grupo(lhostgroups, key, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, key):
        logger.warning(f'el grupo {key} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups, key)
        if grupo.existe_atributo(atributo):
            if grupo.existe_elemento(atributo, dato):
                grupo.del_elemento(atributo, dato)
                thgr.aplicar_cambios(lhostgroups)
            else: logger.warning(f'no existe el elemento {dato} en {key}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {key}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_grupo', extra=cons.EXTRA)

def mostrar_atributo_grupo(lhostgroups, key, atributo):
    logger.info('iniciando mostrar_atributo_grupo', extra=cons.EXTRA)
    if not thgr.existe_hostgroup(lhostgroups, key):
        logger.warning(f'el grupo {key} no esta definido en {cons.ORIG_HGR}', extra=cons.EXTRA)
    else:
        grupo = thgr.get_hostgroup(lhostgroups, key)
        if grupo.existe_atributo(atributo):
            print(grupo.get_valor(atributo))
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_grupo', extra=cons.EXTRA)

##search

def _get_id_objeto(obj):
    if isinstance(obj, ngctl.clases.Host.Host):
        return cons.ID_HST
    elif isinstance(obj, ngctl.clases.Alarma.Alarma):
        return cons.ID_SRV
    elif isinstance(obj, ngctl.clases.Hostgroup.Hostgroup):
        return cons.ID_HGR
    elif isinstance(obj, ngctl.clases.Command.Command):
        return cons.ID_CMD
    elif isinstance(obj, ngctl.clases.Contact.Contact):
        return cons.ID_CNT
    elif isinstance(obj, ngctl.clases.ContactGroup.ContactGroup):
        return cons.ID_CGR
    else:
        return cons.ID_TPE
    
def search_atributo(lista, regex, atributo=None, show_name=False):
    logger.info('iniciando search_atributo', extra=cons.EXTRA)
    filtro = re.compile(fr'{regex}')
    if atributo == None: aux = _get_id_objeto(lista[0])
    else: aux = atributo
    out = [ x for x in lista if filtro.search(str(x.get_valor(aux))) ]
    logger.info(f'se encontraron {len(out)} coincidencias para el patron {filtro.pattern!r} en {aux}', extra=cons.EXTRA)
    try:
        for i in out:
            if show_name: print(i.get_name())
            else: print(i.get_valor(aux))
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass
    logger.info('finalizando search_atributo', extra=cons.EXTRA)

#export

def _get_objeto(lista, name):
    if isinstance(lista[0], ngctl.clases.Host.Host):
        return thos.get_host(lista, name, log=False)
    elif isinstance(lista[0], ngctl.clases.Alarma.Alarma):
        return tser.get_alarma(lista, name, log=False)
    elif isinstance(lista[0], ngctl.clases.Hostgroup.Hostgroup):
        return thgr.get_hostgroup(lista, name, log=False)
    elif isinstance(lista[0], ngctl.clases.Command.Command):
        return tcmd.get_command(lista, name, log=False)
    elif isinstance(lista[0], ngctl.clases.Contact.Contact):
        return tcnt.get_contact(lista, name, log=False)
    elif isinstance(lista[0], ngctl.clases.ContactGroup.ContactGroup):
        return tcgr.get_contactgroup(lista, name, log=False)
    else:
        return ttpe.get_timeperiod(lista, name, log=False)

def generar_reporte(lista, file_in, file_out, separador_out=',', *atributos):
    logger.info('iniciando generar_reporte', extra=cons.EXTRA)
    writer = csv.DictWriter(file_out, fieldnames=atributos, delimiter=separador_out)
    writer.writeheader()
    try:
        for i in file_in:
            i = i.strip()
            if i != '':
                obj = _get_objeto(lista, i)
                data_row = {}
                for atributo in atributos:
                    if obj.existe_atributo(atributo, log=False):
                        data_row[atributo] = obj.get_valor(atributo)
                writer.writerow(data_row)
                del data_row
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass
    logger.info(f'Se exportaron {len(lista)} registros a {getattr(file_out, "name")}', extra=cons.EXTRA)
    logger.info('finalizando generar_reporte', extra=cons.EXTRA)

#Funciones para commands

def cargar_commands():
    return tcmd.cargar()

def mostrar_command(lista, command):
    logger.info('iniciando mostrar_command', extra=cons.EXTRA)
    if tcmd.existe_command(lista, command):
        tcmd.show_command(lista,command)
        logger.info(f'se visualizo {command}', extra=cons.EXTRA)
    else: logger.warning(f'no se encontro el command {command} definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_command', extra=cons.EXTRA)

def eliminar_command(lista_commands, command_name):
    logger.info('iniciando eliminar_command', extra=cons.EXTRA)
    if tcmd.existe_command(lista_commands, command_name):
        tcmd.delete_command(lista_commands, command_name)
        tcmd.aplicar_cambios(lista_commands)
    else: logger.warning(f'el command {command} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_command', extra=cons.EXTRA)

def renombrar_command(lista_alarmas, lista_commands, command_name, new):
    logger.info('iniciando renombrar_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, command_name):
        logger.warning(f'no existe definicion de {command_name} en {cons.ORIG_CMD}', extra=cons.EXTRA)
    elif tcmd.existe_command(lista_commands, new):
        logger.warning(f'el contact {new} ya existe en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'check_command', command_name, sep='!'):
            alarma.rename_elemento('check_command', command_name, new, sep='!', log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} check_command en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        command = tcmd.get_command(lista_commands, command_name)
        command.rename_elemento(cons.ID_CMD, command_name, new, log=False)
        logger.info(f'se renombro {command_name} con {new} en {cons.ORIG_CMD}', extra=cons.EXTRA)
        tcmd.aplicar_cambios(lista_commands)
    logger.info('finalizando renombrar_command', extra=cons.EXTRA)

def copiar_command(lista_commands, command, new):
    logger.info('iniciando copiar_command', extra=cons.EXTRA)
    if tcmd.existe_command(lista_commands, command):
        if not tcmd.existe_command(lista_commands, new):
            tcmd.copy_command(lista_commands, command, new)
            tcmd.aplicar_cambios(lista_commands)
        else: logger.warning(f'el command {new} ya existe en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else: logger.warning(f'el command {command} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    logger.info('finalizando copiar_command', extra=cons.EXTRA)

def modificar_atributo_command(lista_commands, name, atributo, new):
    logger.info('iniciando modificar_atributo_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if command.existe_atributo(atributo):
            command.add_valor(atributo,new)
            tcmd.aplicar_cambios(lista_commands)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_command', extra=cons.EXTRA)

def eliminar_atributo_command(lista_commands, name, atributo):
    logger.info('iniciando eliminar_atributo_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if command.existe_atributo(atributo):
            command.del_parametro(atributo)
            tcmd.aplicar_cambios(lista_commands)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_command', extra=cons.EXTRA)

def mostrar_atributo_command(lista_commands, name, atributo):
    logger.info('iniciando mostrar_atributo_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if command.existe_atributo(atributo):
            print(command.get_valor(atributo))
        else: logger.warning(f'no existe el command {name}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_command', extra=cons.EXTRA)

def eliminar_elemento_command(lista_commands, name, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if command.existe_atributo(atributo):
            if command.existe_elemento(atributo, dato):
                command.del_elemento(atributo, dato)
                tcmd.aplicar_cambios(lista_commands)
            else: logger.warning(f'no existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_command', extra=cons.EXTRA)

def agregar_elemento_command(lista_commands, name, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if command.existe_atributo(atributo):
            if not command.existe_elemento(atributo, dato):
                command.add_elemento(atributo, dato)
                tcmd.aplicar_cambios(lista_commands)
            else: logger.warning(f'ya existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else:
            command.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            tcmd.aplicar_cambios(lista_commands)
    logger.info('finalizando agregar_elemento_command', extra=cons.EXTRA)

def agregar_parametro_command(lista_commands, name, atributo, valor):
    logger.info('iniciando agregar_parametro_command', extra=cons.EXTRA)
    if not tcmd.existe_command(lista_commands, name):
        logger.warning(f'el command {name} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    else:
        command = tcmd.get_command(lista_commands, name)
        if not command.existe_atributo(atributo):
            command.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            tcmd.aplicar_cambios(lista_commands)
        else: logger.warning(f'ya existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_command', extra=cons.EXTRA)

#Funciones para contacts

def cargar_contacts():
    return tcnt.cargar()

def mostrar_contact(lista, contact):
    logger.info('iniciando mostrar_contact', extra=cons.EXTRA)
    if tcnt.existe_contact(lista, contact):
        tcnt.show_contact(lista,contact)
        logger.info(f'se visualizo {contact}', extra=cons.EXTRA)
    else: logger.warning(f'no se encontro el contact {contact} definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_contact', extra=cons.EXTRA)

def eliminar_contact(lista_contactgroups, lista_alarmas, lista_hosts, lista_contacts, contact_name):
    logger.info('iniciando eliminar_contact', extra=cons.EXTRA)
    if tcnt.existe_contact(lista_contacts, contact_name):
        frecuencia = 0
        for contactgroup in tcgr.get_parametro_in_contactgroup(lista_contactgroups, 'members', contact_name):
            contactgroup.del_elemento('members', contact_name, log=False)
            logger.warning(f'se elimino el contact {contact_name} del contactgroup {contactgroup.get_name()}', extra=cons.EXTRA)
            frecuencia += 1
        if frecuencia > 0: tcgr.aplicar_cambios(lista_contactgroups)
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'contacts', contact_name):
            alarma.del_elemento('contacts', contact_name, log=False)
            logger.warning(f'se elimino el contact {contact_name} de la alarma {alarma.get_name()}', extra=cons.EXTRA)
            frecuencia += 1
        if frecuencia > 0: tser.aplicar_cambios(lista_alarmas)
        frecuencia = 0
        for host in thos.get_parametro_in_host(lista_hosts, 'contacts', contact_name):
            host.del_elemento('contacts', contact_name, log=False)
            logger.warning(f'se elimino el contact {contact_name} del host {host.get_name()}', extra=cons.EXTRA)
            frecuencia += 1
        if frecuencia > 0: thos.aplicar_cambios(lista_hosts)
        tcnt.delete_contact(lista_contacts, contact_name)
        tcnt.aplicar_cambios(lista_contacts)
    else: logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)

def renombrar_contact(lista_contactgroups, lista_alarmas, lista_hosts, lista_contacts, contact_name, new):
    logger.info('iniciando renombrar_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, contact_name):
        logger.warning(f'no existe definicion de {contact_name} en {cons.ORIG_CNT}', extra=cons.EXTRA)
    elif tcnt.existe_contact(lista_contacts, new):
        logger.warning(f'el contact {new} ya existe en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        frecuencia = 0
        for contactgroup in tcgr.get_parametro_in_contactgroup(lista_contactgroups, 'members', contact_name):
            contactgroup.rename_elemento('members', contact_name, new, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} contactgroups en {cons.ORIG_CGR}', extra=cons.EXTRA)
            tcgr.aplicar_cambios(lista_contactgroups)
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'contacts', contact_name):
            alarma.rename_elemento('contacts', contact_name, new, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} alarmas en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        frecuencia = 0
        for host in thos.get_parametro_in_host(lista_hosts, 'contacts', contact_name):
            host.rename_elemento('contacts', contact_name, new, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} hosts en {cons.ORIG_HST}', extra=cons.EXTRA)
            thos.aplicar_cambios(lista_hosts)
        contact = tcnt.get_contact(lista_contacts, contact_name)
        contact.rename_elemento(cons.ID_CNT, contact_name, new, log=False)
        logger.info(f'se renombro {contact_name} con {new} en {cons.ORIG_CNT}', extra=cons.EXTRA)
        tcnt.aplicar_cambios(lista_contacts)
    logger.info('finalizando renombrar_contact', extra=cons.EXTRA)

def copiar_contact(lista_contacts, contact, new):
    logger.info('iniciando copiar_contact', extra=cons.EXTRA)
    if tcnt.existe_contact(lista_contacts, contact):
        if not tcnt.existe_contact(lista_contacts, new):
            tcnt.copy_contact(lista_contacts, contact, new)
            tcnt.aplicar_cambios(lista_contacts)
        else: logger.warning(f'el contact {new} ya existe en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else: logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    logger.info('finalizando copiar_contact', extra=cons.EXTRA)

def mostrar_listado_contactgroup(lista_contacts, lista_contactgroups, contact_name):
    logger.info('iniciando mostrar_listado_contactgroup', extra=cons.EXTRA)
    if tcnt.existe_contact(lista_contacts, contact_name):
        frecuencia = 0
        try:
            for contactgroup in tcgr.get_parametro_in_contactgroup(lista_contactgroups, 'members', contact_name):
                print (contactgroup.get_name())
                frecuencia += 1
        except IOError as e:
            if e.errno == errno.EPIPE: pass
        logger.info(f'se visualizo {frecuencia} contactgroups asociados al contact {contact_name}', extra=cons.EXTRA)
    else: logger.warning(f'el contact {contact_name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_listado_contactgroup', extra=cons.EXTRA)

def modificar_atributo_contact(lista_contacts, name, atributo, new):
    logger.info('iniciando modificar_atributo_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if contact.existe_atributo(atributo):
            contact.add_valor(atributo,new)
            tcnt.aplicar_cambios(lista_contacts)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_contact', extra=cons.EXTRA)

def eliminar_atributo_contact(lista_contacts, name, atributo):
    logger.info('iniciando eliminar_atributo_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if contact.existe_atributo(atributo):
            contact.del_parametro(atributo)
            tcnt.aplicar_cambios(lista_contacts)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_contact', extra=cons.EXTRA)

def mostrar_atributo_contact(lista_contacts, name, atributo):
    logger.info('iniciando mostrar_atributo_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if contact.existe_atributo(atributo):
            print(contact.get_valor(atributo))
        else: logger.warning(f'no existe el contact {name}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_contact', extra=cons.EXTRA)

def eliminar_elemento_contact(lista_contacts, name, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if contact.existe_atributo(atributo):
            if contact.existe_elemento(atributo, dato):
                contact.del_elemento(atributo, dato)
                tcnt.aplicar_cambios(lista_contacts)
            else: logger.warning(f'no existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_contact', extra=cons.EXTRA)

def agregar_elemento_contact(lista_contacts, name, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if contact.existe_atributo(atributo):
            if not contact.existe_elemento(atributo, dato):
                contact.add_elemento(atributo, dato)
                tcnt.aplicar_cambios(lista_contacts)
            else: logger.warning(f'ya existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else:
            contact.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            tcnt.aplicar_cambios(lista_contacts)
    logger.info('finalizando agregar_elemento_contact', extra=cons.EXTRA)

def agregar_parametro_contact(lista_contacts, name, atributo, valor):
    logger.info('iniciando agregar_parametro_contact', extra=cons.EXTRA)
    if not tcnt.existe_contact(lista_contacts, name):
        logger.warning(f'el contact {name} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else:
        contact = tcnt.get_contact(lista_contacts, name)
        if not contact.existe_atributo(atributo):
            contact.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            tcnt.aplicar_cambios(lista_contacts)
        else: logger.warning(f'ya existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_contact', extra=cons.EXTRA)

#Funciones para contactgroups

def cargar_contactgroups():
    return tcgr.cargar()

def mostrar_contactgroup(lista, contactgroup):
    logger.info('iniciando mostrar_contactgroup', extra=cons.EXTRA)
    if tcgr.existe_contactgroup(lista, contactgroup):
        tcgr.show_contactgroup(lista,contactgroup)
        logger.info(f'se visualizo {contactgroup}', extra=cons.EXTRA)
    else: logger.warning(f'no se encontro el contactgroup {contactgroup} definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_contactgroup', extra=cons.EXTRA)

def eliminar_contactgroup(lista_hosts, lista_alarmas, lista_contactgroups, contactgroup_name):
    logger.info('iniciando eliminar_contactgroup', extra=cons.EXTRA)
    if tcgr.existe_contactgroup(lista_contactgroups, contactgroup_name):
        frecuencia = 0
        for host in thos.get_parametro_in_host(lista_hosts, 'contact_groups', contactgroup_name):
            host.del_elemento('contact_groups', contactgroup_name, log=False)
            frecuencia += 1
        if frecuencia > 0: 
            logger.warning(f'se elimino {frecuencia} hosts en {cons.ORIG_HST}', extra=cons.EXTRA)
            thos.aplicar_cambios(lista_hosts)
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'contact_groups', contactgroup_name):
            alarma.del_elemento('contact_groups', contactgroup_name, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.warning(f'se elimino {frecuencia} alarmas en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        tcgr.delete_contactgroup(lista_contactgroups, contactgroup_name)
        tcgr.aplicar_cambios(lista_contactgroups)
    else: logger.warning(f'el contactgroup {contactgroup} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_contactgroup', extra=cons.EXTRA)

def renombrar_contactgroup(lista_alarmas, lista_hosts, lista_contactgroups, contactgroup_name, new):
    logger.info('iniciando renombrar_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, contactgroup_name):
        logger.warning(f'no existe definicion de {contactgroup_name} en {cons.ORIG_CGR}', extra=cons.EXTRA)
    elif tcgr.existe_contactgroup(lista_contactgroups, new):
        logger.warning(f'el contactgroup {new} ya existe en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'contact_groups', contactgroup_name):
            alarma.rename_elemento('contact_groups', contactgroup_name, new, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} alarmas en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        frecuencia = 0
        for host in thos.get_parametro_in_host(lista_hosts, 'contact_groups', contactgroup_name):
            host.rename_elemento('contact_groups', contactgroup_name, new, log=False)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} hosts en {cons.ORIG_HST}', extra=cons.EXTRA)
            thos.aplicar_cambios(lista_hosts)
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, contactgroup_name)
        contactgroup.rename_elemento(cons.ID_CGR, contactgroup_name, new, log=False)
        logger.info(f'se renombro {contactgroup_name} con {new} en {cons.ORIG_CGR}', extra=cons.EXTRA)
        tcgr.aplicar_cambios(lista_contactgroups)
    logger.info('finalizando renombrar_contactgroup', extra=cons.EXTRA)

def copiar_contactgroup(lista_contactgroups, contactgroup, new):
    logger.info('iniciando copiar_contactgroup', extra=cons.EXTRA)
    if tcgr.existe_contactgroup(lista_contactgroups, contactgroup):
        if not tcgr.existe_contactgroup(lista_contactgroups, new):
            tcgr.copy_contactgroup(lista_contactgroups, contactgroup, new)
            tcgr.aplicar_cambios(lista_contactgroups)
        else: logger.warning(f'el contactgroup {new} ya existe en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else: logger.warning(f'el contactgroup {contactgroup} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    logger.info('finalizando copiar_contactgroup', extra=cons.EXTRA)

def modificar_atributo_contactgroup(lista_contactgroups, name, atributo, new):
    logger.info('iniciando modificar_atributo_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if contactgroup.existe_atributo(atributo):
            contactgroup.add_valor(atributo,new)
            tcgr.aplicar_cambios(lista_contactgroups)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_contactgroup', extra=cons.EXTRA)

def eliminar_atributo_contactgroup(lista_contactgroups, name, atributo):
    logger.info('iniciando eliminar_atributo_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if contactgroup.existe_atributo(atributo):
            contactgroup.del_parametro(atributo)
            tcgr.aplicar_cambios(lista_contactgroups)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_contactgroup', extra=cons.EXTRA)

def mostrar_atributo_contactgroup(lista_contactgroups, name, atributo):
    logger.info('iniciando mostrar_atributo_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if contactgroup.existe_atributo(atributo):
            print(contactgroup.get_valor(atributo))
        else: logger.warning(f'no existe el contactgroup {name}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_contactgroup', extra=cons.EXTRA)

def eliminar_elemento_contactgroup(lista_contactgroups, name, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if contactgroup.existe_atributo(atributo):
            if contactgroup.existe_elemento(atributo, dato):
                contactgroup.del_elemento(atributo, dato)
                tcgr.aplicar_cambios(lista_contactgroups)
            else: logger.warning(f'no existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_contactgroup', extra=cons.EXTRA)

def agregar_elemento_contactgroup(lista_contactgroups, name, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if contactgroup.existe_atributo(atributo):
            if not contactgroup.existe_elemento(atributo, dato):
                contactgroup.add_elemento(atributo, dato)
                tcgr.aplicar_cambios(lista_contactgroups)
            else: logger.warning(f'ya existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else:
            contactgroup.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            tcgr.aplicar_cambios(lista_contactgroups)
    logger.info('finalizando agregar_elemento_contactgroup', extra=cons.EXTRA)

def agregar_parametro_contactgroup(lista_contactgroups, name, atributo, valor):
    logger.info('iniciando agregar_parametro_contactgroup', extra=cons.EXTRA)
    if not tcgr.existe_contactgroup(lista_contactgroups, name):
        logger.warning(f'el contactgroup {name} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    else:
        contactgroup = tcgr.get_contactgroup(lista_contactgroups, name)
        if not contactgroup.existe_atributo(atributo):
            contactgroup.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            tcgr.aplicar_cambios(lista_contactgroups)
        else: logger.warning(f'ya existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_contactgroup', extra=cons.EXTRA)

#Funciones para timeperiods

def cargar_timeperiods():
    return ttpe.cargar()

def mostrar_timeperiod(lista, timeperiod):
    logger.info('iniciando mostrar_timeperiod', extra=cons.EXTRA)
    if ttpe.existe_timeperiod(lista, timeperiod):
        ttpe.show_timeperiod(lista,timeperiod)
        logger.info(f'se visualizo {timeperiod}', extra=cons.EXTRA)
    else: logger.warning(f'no se encontro el timeperiod {timeperiod} definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_timeperiod', extra=cons.EXTRA)

def eliminar_timeperiod(lista_timeperiods, timeperiod_name):
    logger.info('iniciando eliminar_timeperiod', extra=cons.EXTRA)
    if ttpe.existe_timeperiod(lista_timeperiods, timeperiod_name):
        ttpe.delete_timeperiod(lista_timeperiods, timeperiod_name)
        ttpe.aplicar_cambios(lista_timeperiods)
    else: logger.warning(f'el timeperiod {timeperiod} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_timeperiod', extra=cons.EXTRA)

def renombrar_timeperiod(lista_alarmas, lista_timeperiods, timeperiod_name, new):
    logger.info('iniciando renombrar_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, timeperiod_name):
        logger.warning(f'no existe definicion de {timeperiod_name} en {cons.ORIG_TPE}', extra=cons.EXTRA)
    elif ttpe.existe_timeperiod(lista_timeperiods, new):
        logger.warning(f'el contact {new} ya existe en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'check_period', timeperiod_name):
            alarma.add_valor('check_period', new)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} check_period en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        frecuencia = 0
        for alarma in tser.get_parametro_in_alarma(lista_alarmas, 'notification_period', timeperiod_name):
            alarma.add_valor('notification_period', new)
            frecuencia += 1
        if frecuencia > 0:
            logger.info(f'se renombro {frecuencia} notification_period en {cons.ORIG_SRV}', extra=cons.EXTRA)
            tser.aplicar_cambios(lista_alarmas)
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, timeperiod_name)
        timeperiod.add_valor(cons.ID_TPE, new)
        logger.info(f'se renombro {timeperiod_name} con {new} en {cons.ORIG_TPE}', extra=cons.EXTRA)
        ttpe.aplicar_cambios(lista_timeperiods)
    logger.info('finalizando renombrar_timeperiod', extra=cons.EXTRA)

def copiar_timeperiod(lista_timeperiods, timeperiod, new):
    logger.info('iniciando copiar_timeperiod', extra=cons.EXTRA)
    if ttpe.existe_timeperiod(lista_timeperiods, timeperiod):
        if not ttpe.existe_timeperiod(lista_timeperiods, new):
            ttpe.copy_timeperiod(lista_timeperiods, timeperiod, new)
            ttpe.aplicar_cambios(lista_timeperiods)
        else: logger.warning(f'el timeperiod {new} ya existe en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else: logger.warning(f'el timeperiod {timeperiod} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    logger.info('finalizando copiar_timeperiod', extra=cons.EXTRA)

def modificar_atributo_timeperiod(lista_timeperiods, name, atributo, new):
    logger.info('iniciando modificar_atributo_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if timeperiod.existe_atributo(atributo):
            timeperiod.add_valor(atributo,new)
            ttpe.aplicar_cambios(lista_timeperiods)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando modificar_atributo_timeperiod', extra=cons.EXTRA)

def eliminar_atributo_timeperiod(lista_timeperiods, name, atributo):
    logger.info('iniciando eliminar_atributo_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if timeperiod.existe_atributo(atributo):
            timeperiod.del_parametro(atributo)
            ttpe.aplicar_cambios(lista_timeperiods)
        else: logger.warning(f'no existe el atributo {atributo}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_atributo_timeperiod', extra=cons.EXTRA)

def mostrar_atributo_timeperiod(lista_timeperiods, name, atributo):
    logger.info('iniciando mostrar_atributo_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if timeperiod.existe_atributo(atributo):
            print(timeperiod.get_valor(atributo))
        else: logger.warning(f'no existe el timeperiod {name}', extra=cons.EXTRA)
    logger.info('finalizando mostrar_atributo_timeperiod', extra=cons.EXTRA)

def eliminar_elemento_timeperiod(lista_timeperiods, name, atributo, dato): #solo se puede eliminar un elem a la vez
    logger.info('iniciando eliminar_elemento_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if timeperiod.existe_atributo(atributo):
            if timeperiod.existe_elemento(atributo, dato):
                timeperiod.del_elemento(atributo, dato)
                ttpe.aplicar_cambios(lista_timeperiods)
            else: logger.warning(f'no existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else: logger.warning(f'no existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_elemento_timeperiod', extra=cons.EXTRA)

def agregar_elemento_timeperiod(lista_timeperiods, name, atributo, dato): #puede add varios elems separados x , Ej w,c,r
    logger.info('iniciando agregar_elemento_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if timeperiod.existe_atributo(atributo):
            if not timeperiod.existe_elemento(atributo, dato):
                timeperiod.add_elemento(atributo, dato)
                ttpe.aplicar_cambios(lista_timeperiods)
            else: logger.warning(f'ya existe el elemento {dato} en {name}', extra=cons.EXTRA)
        else:
            timeperiod.add_parametro([atributo, dato])
            logger.info(f'se agrego {atributo} {dato}', extra=cons.EXTRA)
            ttpe.aplicar_cambios(lista_timeperiods)
    logger.info('finalizando agregar_elemento_timeperiod', extra=cons.EXTRA)

def agregar_parametro_timeperiod(lista_timeperiods, name, atributo, valor):
    logger.info('iniciando agregar_parametro_timeperiod', extra=cons.EXTRA)
    if not ttpe.existe_timeperiod(lista_timeperiods, name):
        logger.warning(f'el timeperiod {name} no esta definido en {cons.ORIG_TPE}', extra=cons.EXTRA)
    else:
        timeperiod = ttpe.get_timeperiod(lista_timeperiods, name)
        if not timeperiod.existe_atributo(atributo):
            timeperiod.add_parametro([atributo,valor])
            logger.info(f'se agrego {atributo} {valor}', extra=cons.EXTRA)
            ttpe.aplicar_cambios(lista_timeperiods)
        else: logger.warning(f'ya existe el atributo {atributo} en {name}', extra=cons.EXTRA)
    logger.info('finalizando agregar_parametro_timeperiod', extra=cons.EXTRA)

if __name__ == '__main__':
    pass
