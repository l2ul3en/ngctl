#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Purpose:     Funciones para procesamiento a nivel de contacts.cfg 
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Contact import Contact
from subprocess import getoutput as geto
from copy import deepcopy as copiar #permite copiar un objeto
import logging,logging.config

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

def aplicar_cambios(datos):
    """Guarda los cambios previo Backup."""

    with open(cons.TMP_CNT, 'w') as f:
        for i in datos:
            print(i,file=f,flush=True)
    c = geto(f'cp -f {cons.DIR}{cons.ORIG_CNT} {cons.BACK_CNT}')
    c = geto(f'cp -f {cons.TMP_CNT} {cons.DIR}{cons.ORIG_CNT}')
    logger.info(f'OK Backup!!/se aplico los cambios a {cons.ORIG_CNT}', extra=cons.EXTRA)

def cargar():
    """Devuelve una lista de objetos Contacts.

Lee linea a linea el archivo especificado en constantes.py cargando todo las definiciones de contacts.
Lista     ->  [['contact_name',['atributo valor1',...,'atributo valorN']]]"""
    lista_contact = []
    contact = Contact()
    with open (cons.DIR + cons.ORIG_CNT,'r') as f:
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
                contact.ordenar()
                if contact.existe_atributo(cons.ID_CNT,log=False):
                    lista_contact.append(contact)
                contact = Contact()
            else:
                if ',' in i:
                    contact.add_parametro(_procesar(i,','))
                else: contact.add_parametro(i.split(maxsplit=1))
    return lista_contact

def _procesar(cad,char):
    atr = cad.split(maxsplit=1)[0]
    lista = cad.split(maxsplit=1)[1].split(char)
    lista = [i.strip() for i in lista if i != '']
    lista.sort(key=str.lower)
    if len(lista) == 1:
        val = ''.join(lista)
    else: val = char.join(lista)
    return [atr,val]

def get_contact(datos,contact,log=True):
    """Retorna el objeto contact."""
    for i in datos:
        if i.get_name() == contact:
            if log:
                logger.info(f'se obtuvo el contact {contact}', extra=cons.EXTRA)
            return i
    logger.error(f'no se encontro el contact {contact}, exit..', extra=cons.EXTRA)
    raise SystemExit(2)

def delete_contact(datos,contact):
    """Elimina el contact indicado."""
    i = 0
    while i < len(datos):
        while i < len(datos) and datos[i].get_name() == contact:
            del datos[i]
            logger.info(f'se elimino el contact {contact}', extra=cons.EXTRA)
        i += 1

def show_contact(datos,contact):
    """Imprime por pantalla la config del contact indicado."""
    for i in (x for x in datos if x.get_name() == contact):
        print(i)

def copy_contact(datos,old,new):
    """Realiza la copia del contact old para el contact new."""
    contact = Contact()
    for i in range(len(datos)):
        if datos[i].get_name() == old:
            contact = copiar(datos[i])
            datos.append(contact)
            datos[-1].add_valor(cons.ID_CNT, new)
            logger.info(f'se copio {old} a {new} en {cons.ORIG_CNT}', extra=cons.EXTRA)

def existe_contact(datos,contact):
    """Verifica si el contact existe."""
    for x in datos:
        if x.get_name() == contact:
            return True
    return False


if __name__ == '__main__':
    pass
