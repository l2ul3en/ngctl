#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        Hostgroup.py
# Purpose:     Define un command generico
#
# Author:      Personal
#
# Created:     30/08/2022
# Copyright:   (c) Personal 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sys import path
path.append('../../')
import ngctl.config.constantes as cons
from ngctl.clases.Body import Body
import logging,logging.config

logging.config.fileConfig(cons.LOG_CONF)
logger = logging.getLogger(__name__)

class Command(Body):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'define command{' + '\n' + super().__str__() + '}'

    def get_name(self):
        return super().get_valor('command_name')

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __ge__(self, other):
        return self.get_name() >= other.get_name()

if __name__ == '__main__':
    pass
