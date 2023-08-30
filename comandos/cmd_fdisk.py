import os
from comandos.cmd_mkdisk import cmd_mkdisk 

# se necesitan funciones de crear, delete, add 
class cmd_fdisk():
    
    def createFdisk(self, size, path, name, unit, type, fit):
        ## revisar path existente
        if self.checkPath(path) == True:
            ## revisar si exsite el nombre de partition
            print('path existe')
            self.checkName(path, name)

    def checkPath(self,path):
        #revisa si el path existe
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
            
        
    def checkName(self, path, name):
        ## leer partitions del MBR, luego atributo name 
        mbr= cmd_mkdisk()
        mbr.setBytes(mbr.getMBR(path))

    