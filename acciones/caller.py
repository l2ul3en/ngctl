#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        caller.py
# Purpose:     Invocar funciones que realicen tareas especificas
#
# Author:      Personal
#
# Created:     13/09/2020
# Copyright:   (c) Personal 2020
# Licence:     <your licence>
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
import ngctl.clases.Alarma #necesario para exportar
import ngctl.clases.Host
import ngctl.clases.Hostgroup
import logging, logging.config, re, csv
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
        for i in tser.get_listado_alarmas(lalarmas,host):
            print(i)
            c += 1
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
            i.rename_elemento('members', host, new)
            frec += 1
        logger.info(f'se modifico {frec} grupos en {cons.ORIG_HGR}', extra=cons.EXTRA)
        if frec > 0:
            thgr.aplicar_cambios(lhostgroups)
        frec = tser.get_frec_host(lalarmas, host)
        if frec > 0:
            tser.rename_host(lalarmas, host, new)
            tser.aplicar_cambios(lalarmas)
        logger.info(f'se modifico {frec} alarmas en {cons.ORIG_SRV}', extra=cons.EXTRA)
        if verbose and frec > 0:
            tser.mostrar_host(lalarmas, new)
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
        for i in thgr.get_listado_hosts(lhostgroups,grupo):
            c = 0
            for j in i.split(','):
                print(j)
                c += 1
            logger.info(f'se visualizo {c} hosts asociados al grupo {grupo}', extra=cons.EXTRA)
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

##Other

def search_regexp(lista, regex):
    logger.info('iniciando search_regexp', extra=cons.EXTRA)
    filtro = re.compile(fr'{regex}')
    out = [x.get_name() for x in lista if filtro.search(x.get_name())]
    logger.info(f'se encontraron {len(out)} coincidencias para el patron {filtro.pattern!r}', extra=cons.EXTRA)
    for i in out:
        print(i)
    logger.info('finalizando search_regexp', extra=cons.EXTRA)

def buscar_ip_host(lista, ip):
    logger.info('iniciando buscar_ip_host', extra=cons.EXTRA)
    c = 0
    for i in thos.get_list_ip_in_host(lista,'address',ip):
        print(i.get_name())
        c += 1
    logger.info(f'se encontraron {c} coincidencias para la IP {ip}', extra=cons.EXTRA)
    logger.info('finalizando buscar_ip_host', extra=cons.EXTRA)

def buscar_ip_alarma(lista, ip):
    logger.info('iniciando buscar_ip_alarma', extra=cons.EXTRA)
    c = 0
    for i in tser.get_list_ip_in_alarma(lista,'check_command',ip,'!'):
        print(i.get_name())
        c += 1
    logger.info(f'se encontraron {c} coincidencias para la IP {ip}', extra=cons.EXTRA)
    logger.info('finalizando buscar_ip_alarma', extra=cons.EXTRA)

#export
def generar_reporte(lista, file_in, file_out, separador_out=',', *atributos):
    logger.info('iniciando generar_reporte', extra=cons.EXTRA)
    writer = csv.DictWriter(file_out, fieldnames=atributos, delimiter=separador_out)
    writer.writeheader()
    for i in file_in:
        i = i.strip()
        if i != '':
            if isinstance(lista[0], ngctl.clases.Host.Host):
                obj = thos.get_host(lista, i, log=False)
            elif isinstance(lista[0], ngctl.clases.Alarma.Alarma):
                obj = tser.get_alarma(lista, i, log=False)
            else:
                obj = thgr.get_hostgroup(lista, i, log=False)
            data_row = {}
            for atributo in atributos:
                if obj.existe_atributo(atributo, log=False):
                    data_row[atributo] = obj.get_valor(atributo)
            writer.writerow(data_row)
            del data_row
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

def eliminar_command(lista_commands, command):
    logger.info('iniciando eliminar_command', extra=cons.EXTRA)
    if tcmd.existe_command(lista_commands, command):
        tcmd.delete_command(lista_commands, command)
        tcmd.aplicar_cambios(lista_commands)
    else: logger.warning(f'el command {command} no esta definido en {cons.ORIG_CMD}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_command', extra=cons.EXTRA)

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

def eliminar_contact(lista_contacts, contact):
    logger.info('iniciando eliminar_contact', extra=cons.EXTRA)
    if tcnt.existe_contact(lista_contacts, contact):
        tcnt.delete_contact(lista_contacts, contact)
        tcnt.aplicar_cambios(lista_contacts)
    else: logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_contact', extra=cons.EXTRA)

def copiar_contact(lista_contacts, contact, new):
    logger.info('iniciando copiar_contact', extra=cons.EXTRA)
    if tcnt.existe_contact(lista_contacts, contact):
        if not tcnt.existe_contact(lista_contacts, new):
            tcnt.copy_contact(lista_contacts, contact, new)
            tcnt.aplicar_cambios(lista_contacts)
        else: logger.warning(f'el contact {new} ya existe en {cons.ORIG_CNT}', extra=cons.EXTRA)
    else: logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    logger.info('finalizando copiar_contact', extra=cons.EXTRA)

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

def eliminar_contactgroup(lista_contactgroups, contactgroup):
    logger.info('iniciando eliminar_contactgroup', extra=cons.EXTRA)
    if tcgr.existe_contactgroup(lista_contactgroups, contactgroup):
        tcgr.delete_contactgroup(lista_contactgroups, contactgroup)
        tcgr.aplicar_cambios(lista_contactgroups)
    else: logger.warning(f'el contactgroup {contactgroup} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
    logger.info('finalizando eliminar_contactgroup', extra=cons.EXTRA)

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

if __name__ == '__main__':

    l = cargar_hostgroups()
    mostrar_listado_hostgroup(l,'NVR_PARAGU')
