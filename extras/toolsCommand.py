#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel de commands.cfg 
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Command import Command
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_CMD, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_CMD} {cons.BACK_CMD}')
    c = geto(f'cp -f {cons.TMP_CMD} {cons.DIR}{cons.ORIG_CMD}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_CMD}', extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos Commands.

Lee linea a linea el archivo especificado en constantes.py cargando todo las definiciones de commands.
Lista     ->  [['command_name',['atributo valor1',...,'atributo valorN']]]"""
    lista_command = []
    command = Command()
    with open (cons.DIR + cons.ORIG_CMD,'r') as f:
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
                command.ordenar(rev=True)
                if command.existe_atributo(cons.ID_CMD, log=False):
                    lista_command.append(command)
                command = Command()
            else:
                if ',' in i:
                    command.add_parametro(_procesar(i,','))
                else: command.add_parametro(i.split(maxsplit=1))
    return lista_command

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_command(datos,command,log=True):
    """Retorna el objeto command."""
    for i in datos:
        if i.get_name() == command:
            if log:
                logger.info(f'se obtuvo el command {command}', extra=cons.EXTRA)
            return (True, i)
    logger.error(f'no se encontro el command {command}', extra=cons.EXTRA)
    return (False, None)

def delete_command(datos,command):
    """Elimina el command indicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_name() == command:
            del datos[i]
            logger.info(f'se elimino el command {command}', extra=cons.EXTRA)
        i += 1

def show_command(datos,command):
    """Imprime por pantalla la config del command indicado."""
    for i in (x for x in datos if x.get_name() == command):
        print(i)

def copy_command(datos,old,new):
    """Realiza la copia del command old para el command new."""
    command = Command()
    for i in range(len(datos)):
        if datos[i].get_name() == old:
            command = copiar(datos[i])
            datos.append(command)
            datos[-1].add_valor(cons.ID_CMD, new)
            logger.info(f'se copio {old} a {new} en {cons.ORIG_CMD}', extra=cons.EXTRA)

def existe_command(datos,command):
    """Verifica si el command existe."""
    for x in datos:
        if x.get_name() == command:
            return True
    return False


if __name__ == '__main__':
    l = cargar()
    l.sort()
    for i in l:
        print(i.get_name())
