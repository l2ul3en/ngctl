#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        parser.py
# Purpose:     Definir el analizador de comandos y enrutar hacia el procedimiento
#              necesario de acuerdo al nivel de procesamiento requerido
# Author:      Personal
#
# Created:     13/09/2020
# Copyright:   (c) Personal 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sys import path, exit as kill
path.append('/data/source/')
import ngctl.acciones.caller as call
import ngctl.config.constantes as cons
import logging,argparse,logging.config
from subprocess import getoutput as geto

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger (__name__)
lista_alarmas = call.cargar_alarmas()
lista_hosts = call.cargar_hosts()
lista_grupos = call.cargar_hostgroups()
lista_commands = call.cargar_commands()
lista_contacts = call.cargar_contacts()
lista_contactgroups = call.cargar_contactgroups()
lista_alarmas.sort()
lista_hosts.sort()
lista_grupos.sort()
lista_commands.sort()
lista_contacts.sort()
lista_contactgroups.sort()

def validar_formato_ip(ip):
    aux = [int(i) for i in ip.split('.')]
    if len(aux) == 4 and 0 <= aux[0] and aux[0] <= 255 and 0 <= aux[1] and aux[1] <= 255 and 0 <= aux[2] and aux[2] <= 255 and 0 <= aux[3] and aux[3] <= 255:
        return ip
    else: 
        raise argparse.ArgumentTypeError(f'{ip} is not a valid IP')

def validar_longitud_sep(sep):
    if len(sep) >= 2:
        raise argparse.ArgumentTypeError(f'{sep!r} must be a 1-character string')
    return sep

def status(name):
    logger.info(f'{name} [alarmas/hosts/grupos/commands/contacts/contactgroup] [\
{call.get_cantidad_alarmas(lista_alarmas)}/{call.get_cantidad_hosts(lista_hosts)}/{len(lista_grupos)}/{len(lista_commands)}/{len(lista_contacts)}/{len(lista_contactgroups)}\
]', extra=cons.EXTRA)

def exec_servicio(args):
    status(exec_servicio.__name__)
    if args.show:
        call.mostrar_alarma(lista_alarmas, args.service_name, args.host)
    elif args.rename != None:
        call.renombrar_servicio(lista_alarmas, args.service_name, args.rename, args.host)
    elif args.delete:
        call.eliminar_alarma(lista_alarmas, args.service_name, args.host)
    elif args.copy != None:
        call.copiar_servicio(lista_alarmas,args.service_name,args.copy, args.host)
    else: alarma.print_usage()
    status(exec_servicio.__name__)

def exec_servicio_atrib(args):
    status(exec_servicio_atrib.__name__)
    if args.delete:
        call.eliminar_atributo(lista_alarmas, args.service_name, args.atributo, args.host)
    elif args.get:
        call.mostrar_atributo(lista_alarmas, args.service_name, args.atributo, args.host)
    elif args.modify != None:
        call.modificar_atributo(lista_alarmas, args.service_name, args.atributo, args.modify, args.host)
    elif args.del_elemento != None:
        call.eliminar_elemento(lista_alarmas, args.service_name, args.atributo, args.del_elemento, args.host)
    elif args.add_elemento != None:
        call.agregar_elemento(lista_alarmas, args.service_name, args.atributo, args.add_elemento, args.host)
    elif args.new != None:
        call.agregar_parametro(lista_alarmas, args.service_name, args.atributo, args.new, args.host)
    else: edit_alarm.print_usage()
    status(exec_servicio_atrib.__name__)

def exec_hostname(args):
    status(exec_hostname.__name__)
    if args.lista_alarm:
        call.mostrar_listado_servicios(lista_alarmas, lista_hosts, args.host_name)
    elif args.delete:
        call.eliminar_host(lista_alarmas, lista_hosts, lista_grupos, args.host_name)
    elif args.generate:
        call.reporte_host(lista_alarmas, lista_hosts, args.host_name, args.verbose)
    elif args.rename != None:
        call.renombrar_host(lista_alarmas, lista_grupos, lista_hosts, args.host_name, args.rename, args.verbose) 
    elif args.show:
        call.mostrar_host(lista_hosts, args.host_name,)
    elif args.copy != None and args.ip != None:
        call.copiar_host(lista_alarmas, lista_hosts, args.host_name, args.copy, args.ip)
    elif args.groups:
        call.mostrar_listado_hostgroup(lista_hosts, lista_grupos, args.host_name)
    else: host.print_usage()
    status(exec_hostname.__name__)

def exec_hostname_atrib(args):
    status(exec_hostname_atrib.__name__)
    if args.delete:
        call.eliminar_atributo_host(lista_hosts,args.host_name,args.atributo)
    elif args.get:
        call.mostrar_atributo_host(lista_hosts,args.host_name,args.atributo)
    elif args.modify != None:
        call.modificar_atributo_host(lista_hosts,args.host_name,args.atributo,args.modify)
    elif args.del_elemento != None:
        call.eliminar_elemento_host(lista_hosts, args.host_name, args.atributo, args.del_elemento)
    elif args.add_elemento != None:
        call.agregar_elemento_host(lista_hosts, args.host_name, args.atributo, args.add_elemento)
    elif args.new != None:
        call.agregar_parametro_host(lista_hosts, args.host_name, args.atributo, args.new)
    else: edit_host.print_usage()
    status(exec_hostname_atrib.__name__)

def exec_hostgroup(args):
    status(exec_hostgroup.__name__)
    if args.lista_host:
        call.mostrar_listado_hosts(lista_grupos, args.hostgroup_name)
    elif args.delete:
        call.eliminar_hostgroup(lista_grupos, args.hostgroup_name)
    elif args.copy != None:
        call.duplicar_hostgroup(lista_grupos, args.hostgroup_name, args.copy)
    elif args.show:
        call.mostrar_hostgroup(lista_grupos, args.hostgroup_name)
    elif args.rename != None:
        call.renombrar_hostgroup(lista_grupos, args.hostgroup_name, args.rename)
    else: hgroup.print_usage()
    status(exec_hostgroup.__name__)

def exec_hostgroup_atrib(args):
    status(exec_hostgroup_atrib.__name__)
    if args.delete:
        call.eliminar_atributo_grupo(lista_grupos,args.hostgroup_name,args.atributo)
    elif args.get:
        call.mostrar_atributo_grupo(lista_grupos,args.hostgroup_name,args.atributo)
    elif args.modify != None:
        call.modificar_atributo_grupo(lista_grupos,args.hostgroup_name,args.atributo,args.modify)
    elif args.del_elemento != None:
        call.eliminar_elemento_grupo(lista_grupos, args.hostgroup_name, args.atributo, args.del_elemento)
    elif args.add_elemento != None:
        call.agregar_elemento_grupo(lista_grupos, args.hostgroup_name, args.atributo, args.add_elemento)
    elif args.new != None:
        call.agregar_parametro_grupo(lista_grupos, args.hostgroup_name, args.atributo, args.new)
    else: edit_hgroup.print_usage()
    status(exec_hostgroup_atrib.__name__)

def exec_command(args):
    status(exec_command.__name__)
    if args.show:
        call.mostrar_command(lista_commands, args.command_name)
    elif args.delete:
        call.eliminar_command(lista_commands, args.command_name)
    elif args.copy != None:
        call.copiar_command(lista_commands, args.command_name, args.copy)
    elif args.rename != None:
        call.modificar_atributo_command(lista_commands, args.command_name, cons.ID_CMD, args.rename)
    else: cmmd.print_usage()
    status(exec_command.__name__)

def exec_command_atrib(args):
    status(exec_command_atrib.__name__)
    if args.delete:
        call.eliminar_atributo_command(lista_commands, args.command_name, args.atributo)
    elif args.get:
        call.mostrar_atributo_command(lista_commands, args.command_name, args.atributo)
    elif args.modify != None:
        call.modificar_atributo_command(lista_commands, args.command_name, args.atributo, args.modify)
    elif args.del_elemento != None:
        call.eliminar_elemento_command(lista_commands, args.command_name, args.atributo, args.del_elemento)
    elif args.add_elemento != None:
        call.agregar_elemento_command(lista_commands, args.command_name, args.atributo, args.add_elemento)
    elif args.new != None:
        call.agregar_parametro_command(lista_commands, args.command_name, args.atributo, args.new)
    else: edit_cmd.print_usage()
    status(exec_command_atrib.__name__)

def exec_contactgroup(args):
    status(exec_contactgroup.__name__)
    if args.show:
        call.mostrar_contactgroup(lista_contactgroups, args.contactgroup_name)
    elif args.delete:
        call.eliminar_contactgroup(lista_contactgroups, args.contactgroup_name)
    elif args.copy != None:
        call.copiar_contactgroup(lista_contactgroups, args.contactgroup_name, args.copy)
    elif args.rename != None:
        call.modificar_atributo_contactgroup(lista_contactgroups, args.contactgroup_name, cons.ID_CGR, args.rename)
    else: cgrp.print_usage()
    status(exec_contactgroup.__name__)

def exec_contactgroup_atrib(args):
    status(exec_contactgroup_atrib.__name__)
    if args.delete:
        call.eliminar_atributo_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo)
    elif args.get:
        call.mostrar_atributo_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo)
    elif args.modify != None:
        call.modificar_atributo_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo, args.modify)
    elif args.del_elemento != None:
        call.eliminar_elemento_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo, args.del_elemento)
    elif args.add_elemento != None:
        call.agregar_elemento_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo, args.add_elemento)
    elif args.new != None:
        call.agregar_parametro_contactgroup(lista_contactgroups, args.contactgroup_name, args.atributo, args.new)
    else: edit_cgr.print_usage()
    status(exec_contactgroup_atrib.__name__)

def exec_contact(args):
    status(exec_contact.__name__)
    if args.show:
        call.mostrar_contact(lista_contacts, args.contact_name)
    elif args.delete:
        call.eliminar_contact(lista_contacts, args.contact_name)
    elif args.copy != None:
        call.copiar_contact(lista_contacts, args.contact_name, args.copy)
    elif args.rename != None:
        call.modificar_atributo_contact(lista_contacts, args.contact_name, cons.ID_CNT, args.rename)
    else: cnts.print_usage()
    status(exec_contact.__name__)

def exec_contact_atrib(args):
    status(exec_contact_atrib.__name__)
    if args.delete:
        call.eliminar_atributo_contact(lista_contacts, args.contact_name, args.atributo)
    elif args.get:
        call.mostrar_atributo_contact(lista_contacts, args.contact_name, args.atributo)
    elif args.modify != None:
        call.modificar_atributo_contact(lista_contacts, args.contact_name, args.atributo, args.modify)
    elif args.del_elemento != None:
        call.eliminar_elemento_contact(lista_contacts, args.contact_name, args.atributo, args.del_elemento)
    elif args.add_elemento != None:
        call.agregar_elemento_contact(lista_contacts, args.contact_name, args.atributo, args.add_elemento)
    elif args.new != None:
        call.agregar_parametro_contact(lista_contacts, args.contact_name, args.atributo, args.new)
    else: edit_cnt.print_usage()
    status(exec_contact_atrib.__name__)

def exec_other(args):
    status(exec_other.__name__)
    if args.buscar != None:
        if args.buscar == 'alarma':
            call.search_regexp(lista_alarmas, args.regex)
        elif args.buscar == 'host':
            call.search_regexp(lista_hosts, args.regex)
        else: call.search_regexp(lista_grupos, args.regex)
    elif args.ip != None:
        try:
            args.regex = validar_formato_ip(args.regex)
        except:
            print(f'{args.regex!r} is not a valid IP')
            kill(254)
        if args.ip == 'host':
            call.buscar_ip_host(lista_hosts, args.regex)
        else:
            call.buscar_ip_alarma(lista_alarmas, args.regex)
    else: other.print_usage()
    status(exec_other.__name__)

def exec_export(args):
    status(exec_export.__name__)
    if args.tipo == 'alarma':
        lista = lista_alarmas
    elif args.tipo == 'host':
        lista = lista_hosts
    else:
        lista = lista_grupos

    if args.columns != None:
        call.generar_reporte(lista, args.Input, args.Output, args.delimiter, *args.columns)
    elif args.columns == None:
        #generar la lista de atributos unicos
        lista_unicos = list()
        for obj in lista:
            for  atributo in obj.get_atributos():
                lista_unicos.append(atributo)
        lista_unicos = list(set(lista_unicos))
        lista_unicos.sort()
        call.generar_reporte(lista, args.Input, args.Output, args.delimiter, *lista_unicos)
    else:
        export.print_usage()
    status(exec_export.__name__)

def create_command():
    global parser
    parser = argparse.ArgumentParser(description='nagiosctl es usado para procesar objetos de configuracion nagios de manera modular.')
    subparsers = parser.add_subparsers()

    #An export subcommand
    global export
    export = subparsers.add_parser('export', aliases='e', help='Exportar a salida personalizada')
    export.add_argument('tipo', choices=['alarma','host','grupo'],help='exporta las definiciones de acuerdo al criterio seleccionado')
    export.add_argument('-c', '--columns', nargs='+',help='lista de atributos a exportar en file-out; nombres de columna')
    export.add_argument('-I', '--Input', metavar='file-in',type=argparse.FileType('r'), default='-', help='ruta al archivo de entrada de datos, sin encabezado; por defecto stdin')
    export.add_argument('-O', '--Output', metavar='file-out',type=argparse.FileType('w'), default='-', help='ruta al archivo de salida; por defecto stdout')
    export.add_argument('-d', '--delimiter', default=',', type=validar_longitud_sep, help='separador de columnas en archivo de salida; por defecto ,')
    export.set_defaults(func=exec_export)

    #A other subcommand
    global other
    other = subparsers.add_parser('search', aliases='b', help='Busqueda con expresiones regulares extendidas')
    other.add_argument('regex',help='expresion regular')
    grp_ot = other.add_mutually_exclusive_group()
    grp_ot.add_argument('-b','--buscar',choices=['alarma','host','grupo'],help='busqueda de acuerdo al criterio seleccionado')
    grp_ot.add_argument('-i','--ip', choices=['alarma','host'], help='busqueda de IP de acuerdo al criterio seleccionado')
    other.set_defaults(func=exec_other)

    #A hostgroup subcommand
    global hgroup 
    hgroup = subparsers.add_parser('group', aliases='g', help='Procesamiento a nivel de hostgroup')
    hgroup.add_argument(cons.ID_HGR, action='store',help='nombre de grupo')
    group_hgr = hgroup.add_mutually_exclusive_group()
    group_hgr.add_argument('-c','--copy',metavar=f'NEW_{cons.ID_HGR.upper()}',action='store',help=f'copia {cons.ID_HGR} para NEW_{cons.ID_HGR.upper()}')
    group_hgr.add_argument('-d', '--delete', action='store_true',default=False,help=f'elimina {cons.ID_HGR}')
    group_hgr.add_argument('-l','--list',action='store_true',default=False,dest='lista_host',help=f'muestra una lista de hosts asociados a {cons.ID_HGR}')
    group_hgr.add_argument('-r', '--rename',metavar=f'NEW_{cons.ID_HGR.upper()}', action='store',help=f'cambia {cons.ID_HGR} con NEW_{cons.ID_HGR.upper()}')
    group_hgr.add_argument('-s', '--show', action='store_true',default=False,help=f'muestra la configuracion de {cons.ID_HGR}')
    hgroup.set_defaults(func=exec_hostgroup)

    #An edit hostgroup subcomand
    sub_hgroup = hgroup.add_subparsers()
    global edit_hgroup
    edit_hgroup = sub_hgroup.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_hgroup.add_argument('atributo',help=f'nombre del atributo de {cons.ID_HGR}')
    group_edit_hgroup = edit_hgroup.add_mutually_exclusive_group()
    group_edit_hgroup.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade a ELEMENTO en atributo; si no existe el ATRIBUTO lo agrega')
    group_edit_hgroup.add_argument('-d', '--delete', action='store_true',default=False,help='elimina atributo')
    group_edit_hgroup.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_hgroup.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a atributo')
    group_edit_hgroup.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a atributo')
    group_edit_hgroup.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en atributo')
    edit_hgroup.set_defaults(func=exec_hostgroup_atrib)

    # A service subcommand
    global alarma
    alarma = subparsers.add_parser('service', aliases='s', help='Procesamiento a nivel de servicio')
    alarma.add_argument(cons.ID_SRV,help='nombre de alarma')
    group_alarma = alarma.add_mutually_exclusive_group()
    group_opc = alarma.add_mutually_exclusive_group()
    group_alarma.add_argument('-c','--copy',metavar='NEW_HOST',help='copia service_name para NEW_HOST')
    group_alarma.add_argument('-d', '--delete', action='store_true',default=False,help=f'elimina {cons.ID_SRV}')
    group_alarma.add_argument('-r', '--rename',metavar=f'NEW_{cons.ID_SRV.upper()}',help=f'cambia {cons.ID_SRV} con NEW_{cons.ID_SRV.upper()}')
    group_alarma.add_argument('-s', '--show', action='store_true',default=False,help=f'muestra la configuracion de {cons.ID_SRV}')
    group_opc.add_argument('--host',help='especifica HOST para una busqueda mas precisa')
    alarma.set_defaults(func=exec_servicio)

    #An edit service subcomand
    sub_service = alarma.add_subparsers()
    global edit_alarm
    edit_alarm = sub_service.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_alarm.add_argument('atributo',help=f'nombre del atributo de {cons.ID_SRV}')
    group_edit_alarm = edit_alarm.add_mutually_exclusive_group()
    group_edit_alarm.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade a ELEMENTO en ATRIBUTO; si no existe el ATRIBUTO lo agrega')
    group_edit_alarm.add_argument('-d', '--delete',action='store_true',default=False,help='elimina ATRIBUTO')
    group_edit_alarm.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_alarm.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a ATRIBUTO')
    group_edit_alarm.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a ATRIBUTO ')
    group_edit_alarm.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en ATRIBUTO')
    edit_alarm.set_defaults(func=exec_servicio_atrib)

    # A hostname subcommand
    global host
    host = subparsers.add_parser('hostname', aliases='h', help='Procesamiento a nivel de host')
    host.add_argument(cons.ID_HST, action='store',help='nombre de host')
    group_opc = host.add_mutually_exclusive_group()
    group_host = host.add_mutually_exclusive_group()
    group_opc.add_argument('-l','--list',action='store_true',default=False,dest='lista_alarm',help=f'muestra una lista de alarmas asociadas a {cons.ID_HST}')
    group_host.add_argument('-c','--copy',metavar=f'NEW_{cons.ID_HST.upper()}',action='store',help=f'copia las alarmas de {cons.ID_HST} para NEW_{cons.ID_HST.upper()}')
    group_host.add_argument('-d','--delete',action='store_true',default=False,help=f'elimina {cons.ID_HST} y alarmas; desvincula de grupos')
    group_host.add_argument('-g', '--generate',action='store_true',default=False,help=f'genera breve reporte # de alarmas de {cons.ID_HST}')
    group_host.add_argument('-G', '--groups',action='store_true',default=False,help=f'muestra los grupos asociados a {cons.ID_HST}')
    group_host.add_argument('-r', '--rename',metavar=f'NEW_{cons.ID_HST.upper()}', action='store',help=f'cambia {cons.ID_HST} con NEW_{cons.ID_HST.upper()}; actualiza grupos y alarmas')
    group_host.add_argument('-s', '--show', action='store_true',default=False,help=f'muestra la configuracion de {cons.ID_HST}')
    group_opc.add_argument('--ip',type=validar_formato_ip,help='especifica la nueva IP; trabaja con -c/--copy')
    group_opc.add_argument('-v', '--verbose', action='store_true',default=False,help='informe detallado')
    host.set_defaults(func=exec_hostname)

    #An edit host subcomand
    sub_host = host.add_subparsers()
    global edit_host
    edit_host = sub_host.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_host.add_argument('atributo',help=f'nombre del atributo de {cons.ID_HST}')
    group_edit_host = edit_host.add_mutually_exclusive_group()
    group_edit_host.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade ELEMENTO en ATRIBUTO; si no existe el ATRIBUTO lo agrega')
    group_edit_host.add_argument('-d', '--delete', action='store_true',default=False,help='elimina ATRIBUTO VALOR')
    group_edit_host.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_host.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a ATRIBUTO')
    group_edit_host.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a ATRIBUTO ' )
    group_edit_host.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en ATRIBUTO')
    edit_host.set_defaults(func=exec_hostname_atrib)

    #A command subcommand
    global cmmd 
    cmmd = subparsers.add_parser('command', aliases='x', help='Procesamiento a nivel de command')
    cmmd.add_argument(cons.ID_CMD, action='store', help='nombre de command')
    group_cmd = cmmd.add_mutually_exclusive_group()
    group_cmd.add_argument('-c','--copy', metavar=f'NEW_{cons.ID_CMD.upper()}', action='store', help=f'copia {cons.ID_CMD} para NEW_{cons.ID_CMD.upper()}')
    group_cmd.add_argument('-d', '--delete', action='store_true', default=False, help=f'elimina {cons.ID_CMD}')
    group_cmd.add_argument('-r', '--rename', metavar=f'NEW_{cons.ID_CMD.upper()}', action='store', help=f'cambia {cons.ID_CMD} con NEW_{cons.ID_CMD.upper()}')
    group_cmd.add_argument('-s', '--show', action='store_true', default=False, help=f'muestra la configuracion de {cons.ID_CMD}')
    cmmd.set_defaults(func=exec_command)

    #An edit command subcomand
    sub_cmmd = cmmd.add_subparsers()
    global edit_cmd
    edit_cmd = sub_cmmd.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_cmd.add_argument('atributo',help=f'nombre del atributo {cons.ID_CMD}')
    group_edit_cmd = edit_cmd.add_mutually_exclusive_group()
    group_edit_cmd.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade a ELEMENTO en atributo; si no existe el ATRIBUTO lo agrega')
    group_edit_cmd.add_argument('-d', '--delete', action='store_true',default=False,help='elimina atributo')
    group_edit_cmd.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_cmd.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a atributo')
    group_edit_cmd.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a atributo')
    group_edit_cmd.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en atributo')
    edit_cmd.set_defaults(func=exec_command_atrib)

    #A contact subcommand
    global cnts 
    cnts = subparsers.add_parser('contact', aliases='c', help='Procesamiento a nivel de contact')
    cnts.add_argument(cons.ID_CNT, action='store', help='usuario')
    group_cnt = cnts.add_mutually_exclusive_group()
    group_cnt.add_argument('-c','--copy', metavar=f'NEW_{cons.ID_CNT.upper()}', action='store', help=f'copia {cons.ID_CNT} para NEW_{cons.ID_CNT.upper()}')
    group_cnt.add_argument('-d', '--delete', action='store_true', default=False, help=f'elimina {cons.ID_CNT}')
    group_cnt.add_argument('-r', '--rename', metavar=f'NEW_{cons.ID_CNT.upper()}', action='store', help=f'cambia {cons.ID_CNT} con NEW_{cons.ID_CNT.upper()}')
    group_cnt.add_argument('-s', '--show', action='store_true', default=False, help=f'muestra la configuracion de {cons.ID_CNT}')
    cnts.set_defaults(func=exec_contact)

    #An edit contact subcomand
    sub_cnts = cnts.add_subparsers()
    global edit_cnt
    edit_cnt = sub_cnts.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_cnt.add_argument('atributo',help=f'nombre del atributo {cons.ID_CNT}')
    group_edit_cnt = edit_cnt.add_mutually_exclusive_group()
    group_edit_cnt.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade a ELEMENTO en atributo; si no existe el ATRIBUTO lo agrega')
    group_edit_cnt.add_argument('-d', '--delete', action='store_true',default=False,help='elimina atributo')
    group_edit_cnt.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_cnt.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a atributo')
    group_edit_cnt.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a atributo')
    group_edit_cnt.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en atributo')
    edit_cnt.set_defaults(func=exec_contact_atrib)

    #A contactgroup subcommand
    global cgrp 
    cgrp = subparsers.add_parser('contactgroup', aliases='C', help='Procesamiento a nivel de contactgroup')
    cgrp.add_argument(cons.ID_CGR, action='store', help='nombre de contactgroup')
    group_cgr = cgrp.add_mutually_exclusive_group()
    group_cgr.add_argument('-c','--copy', metavar=f'NEW_{cons.ID_CGR.upper()}', action='store', help=f'copia {cons.ID_CGR} para NEW_{cons.ID_CGR.upper()}')
    group_cgr.add_argument('-d', '--delete', action='store_true', default=False, help=f'elimina {cons.ID_CGR}')
    group_cgr.add_argument('-r', '--rename', metavar=f'NEW_{cons.ID_CGR.upper()}', action='store', help=f'cambia {cons.ID_CGR} con NEW_{cons.ID_CGR.upper()}')
    group_cgr.add_argument('-s', '--show', action='store_true', default=False, help=f'muestra la configuracion de {cons.ID_CGR}')
    cgrp.set_defaults(func=exec_contactgroup)

    #An edit contactgroup subcomand
    sub_cgrp = cgrp.add_subparsers()
    global edit_cgr
    edit_cgr = sub_cgrp.add_parser('edit', aliases='e', help='Procesamiento a nivel de atributo')
    edit_cgr.add_argument('atributo',help=f'nombre del atributo {cons.ID_CGR}')
    group_edit_cgr = edit_cgr.add_mutually_exclusive_group()
    group_edit_cgr.add_argument('-a','--add-elemento',dest='add_elemento',metavar='ELEMENTO',help='añade a ELEMENTO en atributo; si no existe el ATRIBUTO lo agrega')
    group_edit_cgr.add_argument('-d', '--delete', action='store_true',default=False,help='elimina atributo')
    group_edit_cgr.add_argument('-g', '--get', action='store_true',default=False,help='muestra el VALOR del ATRIBUTO')
    group_edit_cgr.add_argument('-m','--modify',metavar='VALOR',help='asigna VALOR a atributo')
    group_edit_cgr.add_argument('-n','--new',metavar='VALOR',help='agrega VALOR a atributo')
    group_edit_cgr.add_argument('-x','--delete-elemento',metavar='ELEMENTO',dest='del_elemento',help='elimina a ELEMENTO en atributo')
    edit_cgr.set_defaults(func=exec_contactgroup_atrib)

    args = parser.parse_args()
    #print(args)
    args.func(args)

if __name__ == '__main__':
    create_command()
