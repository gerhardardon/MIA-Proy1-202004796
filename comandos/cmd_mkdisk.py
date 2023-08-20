from datetime import datetime
import os
import random

class cmd_mkdisk:
    
    # function to create an empty file that works as a disk 
    def createDisk(self, size, path, fit, unit):
        self.createRoutes(path)
        self.create(size, path, fit, unit)
        self.createMBR(size, path, fit, unit)


    ## descompone y crea las rutas 
    def createRoutes(self, path):
        directorios=path.split('/')
        directorios.pop()
        directorio=""
        #revisar si el patrh existe, si no crearlo 
        for x in directorios:
            directorio=os.path.join(directorio, x) #une las partes del dir
            if os.path.exists(directorio)!= True:
                #no existe, crear dir
                try:
                    os.makedirs(directorio)
                except:
                    pass

    ## crea el archivo
    def create(self, size, path, fit, unit):
        print("creando--"+path)
        if unit== 'k':
            unit = 1024
        elif unit== 'm':
            unit= 1024*1024
        else:
            print('error al crear disco')

        try:
            with open("."+path, "wb+") as file:
                for i in range(0, size):
                    file.write(b'\x00' * unit)
            file.close()
            print("disk creado")
        except:
            print("fallo creando disk")
 
    def createMBR(self, size, path, fit, unit):
        if unit== 'k':
            unit = 1024
        elif unit== 'm':
            unit= 1024*1024
        else:
            print('error al crear disco')
        mbr_tamano = size*unit
        mbr_fecha_cracion = int(datetime.timestamp(datetime.now()))
        mbr_dsk_signature = random.randint(0,10000)
        dsk_fit = fit

        