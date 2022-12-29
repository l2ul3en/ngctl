#!/usr/bin/python3
from subprocess import getoutput as geto
from sys import path
path.append('../../')

#usuario que ejecuta la app
EXTRA = {'user' : geto('whoami')}

#archivo de log de la app
LOG = '/var/log/nagios/nagiosctl.log'

#archivo de configuracion del logger de python
LOG_CONF = '/data/source/ngctl/config/logging.conf'

#archivo de credenciales SNMP
FILE_SNMPV3 = '/usr/local/nagios/homemade/snmp_v3_server.txt'
FILE_SNMPV2 = '/usr/local/nagios/homemade/snmp_v2_server.txt'

#comands alarmas basicas
CMND_PING = 'check-host-alive'
CMND_CPU_LINUX = 'ch_snmp_cpu_linux'
CMND_RAM_LINUX = 'ch_snmp_ram_linux'
CMND_HD_LINUX = 'ch_snmp_hd_linux'

#directorios de trabajo de la app
DIR = '/data/objects/'  #path completo a los archivos (.cfg) de configuracion de nagios
DIR_BK = '/data/backup/'  #path completo donde se guardaran los archivos de respaldo luego de un cambio (solo se guarda el ultimo cambio)
DIR_TMP = '/data/cache/'  #path completo donde se guardaran los archivos temporales

#si se procesaran nuevos archivos de configuracion se deben agregar 4 nuevas constantes para su funcionamiento
#1. Archivos de objetos de configuracion nagios
ORIG_SRV = 'services.cfg'
ORIG_HST = 'hosts.cfg'
ORIG_HGR = 'hostgroups.cfg'
ORIG_CMD = 'commands.cfg'
ORIG_CNT = 'contacts.cfg'
ORIG_CGR = 'contactgroups.cfg'
ORIG_TPE = 'timeperiods.cfg'

#2. Archivos de respaldo de configuracion nagios
BACK_SRV = f'{DIR_BK}{ORIG_SRV}.bk'
BACK_HST = f'{DIR_BK}{ORIG_HST}.bk'
BACK_HGR = f'{DIR_BK}{ORIG_HGR}.bk'
BACK_CMD = f'{DIR_BK}{ORIG_CMD}.bk'
BACK_CNT = f'{DIR_BK}{ORIG_CNT}.bk'
BACK_CGR = f'{DIR_BK}{ORIG_CGR}.bk'
BACK_TPE = f'{DIR_BK}{ORIG_TPE}.bk'

#3. Archivo temporal para escribir los cambios
TMP_SRV = f'{DIR_TMP}{ORIG_SRV}.tmp'
TMP_HST = f'{DIR_TMP}{ORIG_HST}.tmp'
TMP_HGR = f'{DIR_TMP}{ORIG_HGR}.tmp'
TMP_CMD = f'{DIR_TMP}{ORIG_CMD}.tmp'
TMP_CNT = f'{DIR_TMP}{ORIG_CNT}.tmp'
TMP_CGR = f'{DIR_TMP}{ORIG_CGR}.tmp'
TMP_TPE = f'{DIR_TMP}{ORIG_TPE}.tmp'

#4. Atributo identificador de objetos nagios
ID_SRV = 'service_description'
ID_HST = 'host_name'
ID_HGR = 'hostgroup_name'
ID_CMD = 'command_name'
ID_CNT = 'contact_name'
ID_CGR = 'contactgroup_name'
ID_TPE = 'timeperiod_name'

if __name__ == '__main__':
	pass
