#!/usr/bin/python3
from subprocess import getoutput as geto
from sys import path
path.append('../../')

EXTRA = {'user' : geto('whoami')}
DIR = '/home/manfred/projects/nagiosctl/objectsVAP/'  #path completo a los archivos (.cfg) de configuracion de nagios
DIR_BK = '/home/manfred/projects/nagiosctl/bk/'  #path completo donde se guardaran los archivos de respaldo luego de un cambio (solo se guarda el ultimo cambio)

ORIG_SRV = 'services.cfg' # archivo original services.cfg
BACK_SRV = 'bk/' + ORIG_SRV + '.bk'
ORIG_HST = 'hosts.cfg' # archivo original hosts.cfg
BACK_HST = 'bk/' + ORIG_HST + '.bk'
ORIG_HGR = 'hostgroups.cfg' # archivo original hostgroup.cfg
BACK_HGR = 'bk/' + ORIG_HGR + '.bk'

TMP_SRV = DIR_BK + 'tmp/' + ORIG_SRV + '.tmp' # archivo temporal para escribir los cambios
TMP_HST = DIR_BK + 'tmp/' + ORIG_HST + '.tmp' # archivo temporal para escribir los cambios
TMP_HGR = DIR_BK + 'tmp/' + ORIG_HGR + '.tmp' # archivo temporal para escribir los cambios

LOG = '/var/log/nagios/nagiosctl.log' #path completo donde se almacenaran el log
LOG_CONF = '/home/manfred/projects/nagiosctl/v3/ngctl/config/logging.conf' #path completo al archivo de configuracion del logger

if __name__ == '__main__':
	pass
