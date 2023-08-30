from datetime import datetime
import os
import random

class mbr():
    def __init__(self, size, path, fit, unit):
        self.size = size
        self.path = path
        self.fit = fit
        self.unit = unit

#partition-> status, type, fit, start, s, !!name
class partition():
    def __init__(self, status=b'0', type=b'0', fit=b'0', start=0, s=0, name="a"):
        self.status = status
        self.type = type
        self.fit = fit
        self.start = start
        self.s = s
        self.name = name[:15].ljust(15, "a")

    def imprimir(self):
        print(self.status, self.type, self.fit, self.start, self.s, self.name)
    
    def getBytes(self):
        buffer=bytearray()
        buffer+= self.status
        buffer+= self.type
        buffer+= self.fit
        buffer+= self.start.to_bytes(4, byteorder='big')  # int -4bytes
        buffer+= self.s.to_bytes(4, byteorder='big')      # int -4bytes
        buffer+= self.name.encode('UTF-8')
        return buffer
    
    def getSize(self):
        size=0
        size+= 3
        size+= 8
        size+= 16
        return size

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
    
    ## define la estructura del mbr para luego escrubirlo en los primeros bites del dsk
    def createMBR(self, size, path, fit , unit):
        print("entra")
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
        ## tenemos que crear la var partriciones y luego escribir en el dsk, ver la grabacion del aux
        mbr_partition = []
        #partition-> status, type, fit, start, s, !!name
        part=partition()
        mbr_partition.append(part)
        mbr_partition.append(part)
        mbr_partition.append(part)
        mbr_partition.append(part)

        ## ecribir mbr en disk <--------- TRAL VEZ SE PUEDA HACER UNA CLASE PARA SOLO LLAMARLA
        buffer=bytearray()
        buffer+= mbr_tamano.to_bytes(4, byteorder='big')         # int -4bytes
        buffer+= mbr_fecha_cracion.to_bytes(4, byteorder='big')  # int -4bytes
        buffer+= mbr_dsk_signature.to_bytes(4, byteorder='big')  # int -4bytes
        buffer+= dsk_fit.encode('utf-8')                         # char -1bytes

        '''for num_partition in range(0,4):
            for param_partition in range(0,5):
                buffer+= mbr_partition[num_partition][param_partition]
                #print(mbr_partition[num_partition][param_partition])'''
                # CAMBIAR PATICIONES A CLASS CON OBJS ---------------------- IMPORTANTE
        for x in mbr_partition:
            buffer+= x.getBytes()
        
        print(buffer)
        #escribir en el DSK
        with open("."+path, "rb") as file:
            old_buffer = file.read()
        file.close()

        new_buffer= buffer+old_buffer[len(buffer):]
        
        try:
            with open("."+path, "wb+") as file:
                file.write(new_buffer)
            file.close()
            print('MBR creado')
        except:
            print('no se creo MBR')
    
    def getSize(self):
        size= 0
        size+= 4 # int -4bytes
        size+= 4 # int -4bytes
        size+= 4 # int -4bytes
        size+= 1 # char -1bytes
        return size

    def setBytes(self, buffer):
        tamano= int.from_bytes(buffer[0:4], byteorder= 'big')
        fecha= int.from_bytes(buffer[4:8], byteorder= 'big')
        signature= int.from_bytes(buffer[8:12], byteorder= 'big')
        fit= buffer[12:13].decode('UTF-8')
        print(tamano,' ', fecha,' ',signature,' ',fit)
        
        particiones= []
        for x in range(0,4):
            part=partition()
            

    ## obtiene los valores del mbr   leer-> decode mbr -> decode partitions
    def getMBR(self, path):
        part= partition()
        size= self.getSize() + (part.getSize()*4)
        with open("."+path, "rb") as file:
            ## leer solo los bytes de partitions
            old_buffer = file.read(size)
        file.close()
        return old_buffer
