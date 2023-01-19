#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        Alarma.py
# Purpose:     Define una alarma generica
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
from ngctl.clases.Body import Body
import logging,logging.config

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

class Alarma(Body):

    def __init__(self):
        super().__init__()
        self.__tipo = ''

    def __str__(self):
        return 'define ' + self.__tipo + '{\n' + super().__str__() + '}'

    def get_name(self):
        return super().get_valor(cons.ID_SRV)

    def get_host(self):
        return super().get_valor(cons.ID_HST)

    def add_tipo(self,tipo):
        self.__tipo = tipo

    def get_tipo(self):
        return self.__tipo

    def __eq__(self, other):
        return self.__tipo == other.get_tipo() and self.get_host() == \
        other.get_host() and self.get_name() == other.get_name()

    def __gt__(self,other):
        return self.__tipo == other.get_tipo() and self.get_host() == \
        other.get_host() and self.get_name() > other.get_name()

    def __ge__(self,other):
        return self.__tipo == other.get_tipo() and self.get_host() == \
        other.get_host() and self.get_name() >= other.get_name()

if __name__ == '__main__':
    l = Alarma()
    l.add_tipo('service{')
    l.add_parametro(['host_name','Siga'])
    l.add_parametro(['service_description','siga_ping'])
    l.add_parametro(['check','tartaer'])
    l.add_parametro(['contacs','lopeze'])
    print(l)
    f = Alarma()
    f.add_tipo('service{')
    f.add_parametro(['host_name','siga'])
    f.add_parametro(['service_description','siga_ping'])
    f.add_parametro(['check','tartaer'])
    print(f)

    print('l >= f', l >= f)
    print('l > f',l > f)
    print('l <= f',l <= f)
    print('l < f',l < f)
    print('l == f',l == f)
    print('l != f',l != f)

    lista = []
    lista.append(f)
    lista.append(l)

    lista.sort()
    for i in lista:
        print(i)
