import os
from comandos.objects import *

# se necesitan funciones de crear, delete, add 
class cmd_fdisk():

    ##funcion para crear una particion
    def createFdisk(self, size, path, name, unit, type, fit):
        ##debemos ver si el path es el correcto
        if self.checkPath(path) == True:
            ##debemos revisar si name ya existe 
            if self.checkName(name, path) == True:
                print('done')

    ##funcion paar revisar path, se usa mas arriba   
    def checkPath(self, path):
        directorios=path.split('/')
        directorios.pop(0)
        directorio=""
        #revisar si el path existe, si no crearlo 
        for x in directorios:
            directorio=os.path.join(directorio, x) #une las partes del dir
            if os.path.exists(directorio)!= True:
                print('path no existe')
                return False
        return True

    ##funcion para revisar si el nombre ya existe, se usa mas arriba
    def checkName(self, name, path):
        ## para esto se debe leer el mbr, y las partitions
        mbr_ = mbr()
        mbr_.leerBytes(path)
        ## en este punto ya se tiene toda la info en var mbr_
        print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
        for x in range (0,4):
            print(name)
            print(mbr_.partitions[x].name, len(mbr_.partitions[x].name))
            if mbr_.partitions[x].name == name:
                print('ya existe una particion con ese nombre')
                return False
        return True