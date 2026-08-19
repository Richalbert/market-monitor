# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/sources/base.py
# Author      : Richalbert
# Created     : 2026-08-18
# Last Update : 
# Version     : 0.1
# Description : La classe abstraite Source : impose a toutes les sources
#               de respecter la meme structure
#               Ainsi toute classe qui veut etre une source doit fournir
#               une methode search()
# License     : MIT
#==============================================================================

from abc import ABC, abstractmethod

#-------------------------------------------------------------
# ABC signifie Abstract Base Class
# @abstractmethod marque search() comme methode obligatoire
# tant qu une sous classe n'implemente pas search(), 
# elle ne peut etre instanciee
#-------------------------------------------------------------
class Source(ABC):

    @abstractmethod
    def search(self, search):
        pass