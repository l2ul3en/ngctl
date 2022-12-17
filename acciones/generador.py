#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Invocar funciones que generan alarmas
#-------------------------------------------------------------------------------
import sys
sys.path.append('../../')
import ngctl.config.constantes as cons
import ngctl.extras.toolss as tser
import ngctl.extras.toolsh as thos
#import ngctl.extras.toolsg as thgr
#import ngctl.extras.toolsCommand as tcmd
import ngctl.extras.toolsContact as tcnt
import ngctl.extras.toolsContactGroup as tcgr
import ngctl.acciones.caller as call
#import ngctl.extras.toolsTimeperiod as ttpe
from ngctl.clases.Alarma import Alarma
from ngctl.clases.Host import Host
import logging, logging.config, re
from subprocess import getstatusoutput as ejec
from subprocess import getoutput as geto

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def _existe_config(ip,archivo):
    cmd = f"grep -w '{ip}' {archivo}";
    exitcode, out = ejec(cmd)
    if (exitcode != 0):
        return (False,out);
    print(out)
    return (True,out)

def get_array_value(ip, oid, patron):
    """Devuelve un array en el cual los elementos coinciden con el patron;
    Si inverso es true devuelve los elementos del arrary que no coinciden con patron."""
    exitcode, line = _existe_config(ip,cons.FILE_SNMPV3)
    if (not exitcode):
        print(f"no se encontro config snmpv3 para {ip}")
        exitcode, line = _existe_config(ip,cons.FILE_SNMPV2)
        if (not exitcode):
            print(f"3::UNK - no se encontro config snmp para {ip}")
            exit(3);
        else:
            print(line)
            ipaddress,version,comunidad = line.split('|');
            cmd = f"snmpwalk -v {version} -c {comunidad} {ipaddress} {oid} -On";
            exitcode, line = ejec(cmd)
    else:
        print(line)
        ipaddress,user,passAuth,passEncr,authPro,privPro,secuLev = line.split('|');
        cmd = f"snmpwalk -v3 -u {user} -A {passAuth} -X {passEncr} \
            -a {authPro} -x {privPro} -l {secuLev} {ipaddress} {oid} -On";
        exitcode, line = ejec(cmd);
    regexp = re.compile(rf'{patron}', re.MULTILINE)
    return regexp.findall(line)

def _add_alarmas(lista_alarmas, host, servicio, comando):
    alarma = Alarma()
    alarma.add_tipo('service{')
    alarma.add_parametro(['use','DEFAULT'])
    alarma.add_parametro(['service_description',f'{host}_{servicio}'])
    alarma.add_parametro(['host_name',host])
    alarma.add_parametro(['check_period','24x7'])
    alarma.add_parametro(['normal_check_interval','10'])
    alarma.add_parametro(['notification_interval','30'])
    alarma.add_parametro(['retry_check_interval','10'])
    alarma.add_parametro(['notification_options','c,r,w'])
    alarma.add_parametro(['check_command', comando])
    lista_alarmas.append(alarma)
    logger.info(f'Se agrego la alarma {host}_{servicio} en {cons.ORIG_SRV}', extra=cons.EXTRA)

def _add_host(lista_hosts, lista_contactgroups, host, ip, contact, contactgroup):
    hostname = Host()
    hostname.add_tipo('host{')
    hostname.add_parametro(['use','DEFAULT'])
    hostname.add_parametro(['host_name',host])
    hostname.add_parametro(['address',ip])
    hostname.add_parametro(['contacts',contact])
    hostname.add_parametro(['notification_period','24x7'])
    for i in contactgroup:
        if (not tcgr.existe_contactgroup(lista_contactgroups, i)):
            logger.warning(f'el contactgroup {i} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
        else:
            if (hostname.existe_atributo('contact_groups', log=False)):
                hostname.add_elemento('contact_groups',i)
            else:
                hostname.add_parametro(['contact_groups',i])
                logger.info(f'se agrego {i} al atributo contact_groups', extra=cons.EXTRA)
    lista_hosts.append(hostname)
    logger.info(f'Se agrego el host {host} en {cons.ORIG_HST}', extra=cons.EXTRA)
    thos.aplicar_cambios(lista_hosts)

### Generate

def generar_alarmas_basicas(lista_hosts, lista_alarmas, lista_conctacts, \
lista_contactgroups, hostname, ip, contact, *contactgroup):
    logger.info('iniciando generar_alarmas_basicas', extra=cons.EXTRA)
    if (not tcnt.existe_contact(lista_conctacts,contact)):
        logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    elif (thos.existe_host(lista_hosts, hostname)):
        logger.warning(f'el host {hostname} ya esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        array = get_array_value(ip,'HOST-RESOURCES-MIB::hrFSMountPoint','.*= STRING: "(?!/(dev|sys|proc|run)(/.*)?"$)(.*)"$' )
        discos = [x[2] for x in array]
        _add_host(lista_hosts, lista_contactgroups,  hostname, ip, contact, contactgroup)
        _add_alarmas(lista_alarmas, hostname, 'PING', 'check-host-alive')
        _add_alarmas(lista_alarmas, hostname, 'CPU', 'ch_snmp_cpu_linux')
        _add_alarmas(lista_alarmas, hostname, 'RAM', 'ch_snmp_ram_linux')
        for hd in discos:
            _add_alarmas(lista_alarmas, hostname, f'HD_{hd}', f'ch_snmp_hd_linux!{hd}')
        tser.aplicar_cambios(lista_alarmas)
    logger.info('finalizando generar_alarmas_basicas', extra=cons.EXTRA)

if __name__ == '__main__':
    pass