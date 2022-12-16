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
#import ngctl.clases #necesario para modulo search y export
import logging, logging.config, re
from subprocess import getstatusoutput as ejec
from subprocess import getoutput as geto

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def _existe_config(ip,archivo):
    cmd = f"grep -w '{ip}' {archivo}";
    out, exitcode = ejec(cmd)
    if (exitcode != 0):
        return (False,out);
    print(out[0])
    return (True,out)

def get_array_value(ip, oid, patron):
    """Devuelve un array en el cual los elementos coinciden con el patron;
    Si inverso es true devuelve los elementos del arrary que no coinciden con patron."""
    line, exitcode = _existe_config(ip,cons.FILE_SNMPV3)
    if (exitcode != 0):
        print(f"no se encontro config snmpv3 para {ip}")
        line, exitcode = _existe_config(ip,cons.FILE_SNMPV2)
        if (exitcode != 0):
            print(f"3::UNK - no se encontro config snmp para {ip}")
            exit(3);
        else:
            print(line)
            ipaddress,version,comunidad = line.split('|');
            cmd = f"snmpwalk -v {version} -c {comunidad} {ipaddress} {oid} -On";
            line, exitcode = ejec(cmd)
    else:
        print(line)
        ipaddress,user,passAuth,passEncr,authPro,privPro,secuLev = line.split('|');
        cmd = f"snmpwalk -v3 -u {user} -A {passAuth} -X {passEncr} \
            -a {authPro} -x {privPro} -l {secuLev} {ipaddress} {oid} -On";
        line, exitcode = ejec(cmd);
    regexp = re.compile(rf'{patron}', re.MULTILINE)
    return regexp.findall(line)

### Generate

def generar_alarmas_basicas(lista_hosts, lista_alarmas, lista_conctacts, \
lista_contactgroups, hostname, ip, contact, *contactgroup):
    logger.info('iniciando generar_alarmas_basicas', extra=cons.EXTRA)
    if (not tcnt.existe_contact(lista_conctacts,contact)):
        logger.warning(f'el contact {contact} no esta definido en {cons.ORIG_CNT}', extra=cons.EXTRA)
    elif (thos.existe_host(lista_hosts, hostname)):
        logger.warning(f'el host {hostname} ya esta definido en {cons.ORIG_HST}', extra=cons.EXTRA)
    else:
        array = get_array_value(ip,'oid','.*= STRING: "(?!/(dev|sys|proc|run)(/.*)?"$)(.*)"$' )
        discos = [x[2] for x in array]
        #reemplazar argumentos
        hd=''
        for i in discos:
            hd = cons.MODELO['HD'].replace("ARG1", i)
            hd = hd.replace("HOST", hostname)
        cpu = cons.MODELO['CPU'].replace("HOST", hostname)
        ram = cons.MODELO['RAM'].replace("HOST", hostname)
        ping = cons.MODELO['PING'].replace("HOST", hostname)

        config_host = cons.MODELO['HOST'].replace("ARG1", hostname)
        config_host = config_host.replace("IPADD", ip)
        config_host = config_host.replace("CNTCT", contact)
        #Guardar cambios
        with open(cons.TMP_SRV, 'a') as f:
            for i in lista_alarmas:
                print(i,file=f,flush=True)
            f.write(ping)
            f.write(cpu)
            f.write(ram)
            f.write(hd)
        geto(f'cp -f {cons.DIR}{cons.ORIG_SRV} {cons.BACK_SRV}')
        geto(f'cp -f {cons.TMP_SRV} {cons.DIR}{cons.ORIG_SRV}')
        logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_SRV}', extra=cons.EXTRA)
        with open(cons.TMP_HST, 'a') as f:
            for i in lista_hosts:
                print(i,file=f,flush=True)
            f.write(config_host)
        geto(f'cp -f {cons.DIR}{cons.ORIG_HST} {cons.BACK_HST}')
        geto(f'cp -f {cons.TMP_HST} {cons.DIR}{cons.ORIG_HST}')
        logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_HST}', extra=cons.EXTRA)

        for i in contactgroup: 
            if (not tcgr.existe_contact_group(lista_contactgroups, i)):
                logger.warning(f'el contactgroup {i} no esta definido en {cons.ORIG_CGR}', extra=cons.EXTRA)
            else:
                call.agregar_elemento_host(lista_hosts, hostname, 'contact_groups', i)
        logger.info('finalizando generar_alarmas_basicas', extra=cons.EXTRA)

if __name__ == '__main__':
    cad = '''1.21.1.1.2154.1 = STRING: "/"
1.21.1.1.2154.2 = STRING: "/home"
1.21.1.1.2154.3 = STRING: "/var"
1.21.1.1.2154.4 = STRING: "/proc"
1.21.1.1.2154.5 = STRING: "/dev/sdm"
1.21.1.1.2154.7 = STRING: "/run"
1.21.1.1.2154.3 = STRING: "/opt"'''
    regexp = re.compile(r'.*= STRING: "(?!/(dev|sys|proc|run)(/.*)?"$)(.*)"$', re.MULTILINE)
    coin = regexp.findall(cad)
    print(cad)
    print(coin)
    discos = [x[2] for x in coin]
    print(discos)
    host = "CAMBIADO"
    for i in discos:
        hd = cons.MODELO['HD'].replace("ARG1", i)
        hd = hd.replace("HOST", host)
        print(hd)