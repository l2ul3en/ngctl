#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        Body.py
# Purpose:     Define una lista parametros generica [[ATRIBUTO VALOR],..,[ATRIBUTO-N VALOR-N]]
#              Ademas de metodos para su procesamiento
# Author:      Personal
#
# Created:     13/09/2020
# Copyright:   (c) Personal 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
import logging,logging.config
from subprocess import getoutput as geto

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

class Body:

	def __init__(self):
		self.__parametros = []

	def __str__(self):
		cad = ''
		for datos in self.__parametros:
			if len(datos) == 2: cad += self.eval_espacios(datos[0],datos[1]) + '\n'
			else: cad+= self.eval_espacios(datos[0]) + '\n'
		return cad

	def eval_espacios(self,atr,val=''):
		"""Formatea la cadena para la visualizacion en el archivo de configuracion."""
		for i in range(self.__get_max() - len(atr)):
			atr += ' '
		return '\t'+ atr +'\t'+ val

	def __get_max(self):
		return max([len(self.__parametros[i][0]) for i in range(len(self.__parametros))])

	def get_valor(self,atr):
		"""Devuelve copia/valor asociado al atributo.
		Si no encuentra el atributo devuelve None."""
		for lista in self.__parametros:
			if lista[0] == atr:
				return lista[1]

	def get_parametro(self,atr):
		"""Devuelve una lista a la que apunta atr [ATRIBUTO VALOR]."""
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				return self.__parametros[i]

	def get_lista_parametros(self):
		"""Retorna la lista completa de parametros."""
		return self.__parametros

	def add_parametro(self,lista):
		"""Añade una lista a la lista de parametros [atributo, valor]."""
		self.__parametros.append(lista)

	def add_valor(self,atr,val):
		"""Asigna el valor del atributo atr."""
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				self.__parametros[i][1] = val
				logger.debug(f'se actualizo el atributo {atr} con {val}', extra=cons.EXTRA)
				break

	def add_elemento(self,atr,val,sep=','):
		"""Añade el elemento (val) al atributo (atr)."""
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				if self.__parametros[i][1] != '':
					self.__parametros[i][1] += sep + val
					self.__parametros[i][1] = sep.join(sorted(list(set(self.__parametros[i][1].split(sep)))))
				else: self.__parametros[i][1] = val
				logger.debug(f'se actualizo el atributo {atr} añadiendo {val}', extra=cons.EXTRA)
				break

	def del_parametro(self,atr):
		"""Elimina el parametro al que apunta atr."""
		b = False
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				b = not b
				del self.__parametros[i]
				if atr != 'define':#debido a que en cargar eliminanos este parametro
					logger.debug(f'se elimino {atr}', extra=cons.EXTRA)
				break
		if not b:
			logger.debug(f'no se encontro {atr}', extra=cons.EXTRA)

	def __clean_elementos(self,lista,atr,val):
		"""Elimina el parametro si el valor de atr es vacio."""
		if len(lista) == 1 and lista[0] == val:
			logger.info('se limpiara el atributo vacio', extra=cons.EXTRA)
			self.del_parametro(atr)
			return True
		return False

	def del_elemento(self,atr,val,sep=','):
		"""Elimina el valor de un atributo con separador."""
		parametro = self.get_parametro(atr)
		aux = parametro[1].split(sep)
		if not self.__clean_elementos(aux,atr,val):
			for i in range(len(aux)):
				if aux[i] == val:
					del aux[i]
					parametro[1] = sep.join(aux)
					logger.debug(f'se elimino {val}', extra=cons.EXTRA)
					break
            
	def rename_elemento(self, atr, val, new, sep=','):
		"""Renombra el elemento de un atributo."""
		parametro = self.get_parametro(atr)
		aux = parametro[1].split(sep)
		for i in range(len(aux)):
			if aux[i] == val:
				aux[i] = new
				parametro[1] = sep.join(aux)
				logger.debug(f'se asigno a {atr} {new} en lugar de {val}', extra=cons.EXTRA)
				break
            
	def ordenar(self,rev=False):
		"""Ordena la lista de parametros rev indica el sentido de ordenacion."""
		if rev:
			return self.__parametros.sort(reverse=True)
		else: return self.__parametros.sort()

	def existe_atributo(self,atr,log=True):
		"""Verifica si el atributo esta definido."""
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				if log:
					logger.debug(f'existe el atributo {atr}', extra=cons.EXTRA)
				return True
		return False

	def existe_elemento(self,atr,val,sep=','):
		"""Verifica si el valor existe en atr."""
		for i in range(len(self.__parametros)):
			if self.__parametros[i][0] == atr:
				for k in self.__parametros[i][1].split(sep):
					if k == val:
						return True
		return False

    
if __name__ == '__main__':
	print('hola')

