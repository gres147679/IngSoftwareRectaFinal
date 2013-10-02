from abc import ABCMeta, abstractmethod

class metodoFacturacion:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def facturar(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
