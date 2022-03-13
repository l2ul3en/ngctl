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
		self.__tipo = 'define '

	def __str__(self):
		return self.__tipo + '\n' + super().__str__() + '}'

	def get_id(self):
		return self.__id

	def get_name(self):
		return super().get_valor('service_description')

	def get_host(self):
		return super().get_valor('host_name')

	def add_tipo(self,tipo):
		self.__tipo += tipo

	def get_tipo(self):
		return self.__tipo

	def __eq__(self, other):
		return self.__tipo == other.__tipo and self.get_host() == other.get_host() and self.get_name() == other.get_name()

	def __gt__(self,other):
		return self.__tipo == other.__tipo and self.get_host() == other.get_host() and self.get_name() > other.get_name()

	def __ge__(self,other):
		return self.__tipo == other.__tipo and self.get_host() == other.get_host() and self.get_name() >= other.get_name()

if __name__ == '__main__':
	l = Alarma()
	l.add_tipo('service{')
	l.add_parametro(['host_name','Siga'])
	l.add_parametro(['service_description','siga_ping'])
	l.add_parametro(['check','tartaer'])
	l.add_parametro(['contacs','lopeze'])
	l.add_host('Siga')
	l.add_name('siga_ping')
	print(l)
	f = Alarma()
	f.add_tipo('service{')
	f.add_parametro(['host_name','siga'])
	f.add_parametro(['service_description','siga_ping'])
	f.add_parametro(['check','tartaer'])
	f.add_host('siga')
	f.add_name('siga_ping')
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
