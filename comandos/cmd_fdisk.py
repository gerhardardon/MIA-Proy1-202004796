import os
from comandos.objects import *

# se necesitan funciones de crear, delete, add


class cmd_fdisk():
    diskfit = ""
    # funcion para crear una particion

    def createFdisk(self, size, path, name, unit, type, fit):
        # debemos ver si el path es el correcto
        if self.checkPath(path) == True:
            # debemos revisar si name ya existe
            if self.checkName(name, path) == True:
                # definir unit y fit
                if unit == 'k':
                    unit = 1024
                elif unit == 'm':
                    unit = 1024*1024
                elif unit == 'b':
                    unit = 1
                else:
                    print('[err]en unit')
                fdisk_tamano = size*unit

                # debemos insertar segun tipo
                if type == 'p':
                    self.primary(fdisk_tamano, path, name, type, fit)
                elif type == 'e':
                    self.extended(fdisk_tamano, path, name, type, fit)
                elif type == 'l':
                    self.logic(fdisk_tamano, path, name, type, fit)

    # funcion paar revisar path, se usa mas arriba
    def checkPath(self, path):
        directorios = path.split('/')
        directorios.pop(0)
        directorio = ""
        # revisar si el path existe, si no crearlo
        for x in directorios:
            directorio = os.path.join(directorio, x)  # une las partes del dir
            if os.path.exists(directorio) != True:
                print('[err]path no existe')
                return False
        return True

    # funcion para revisar si el nombre ya existe, se usa mas arriba
    def checkName(self, name, path):
        # para esto se debe leer el mbr, y las partitions
        mbr_ = mbr()
        mbr_.leerBytes(path)
        # en este punto ya se tiene toda la info en var mbr_
        # print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
        self.diskfit = mbr_.fit
        for x in range(0, 4):
            if mbr_.partitions[x].name == name[:16].ljust(16, " "):
                print('[err]ya existe una particion con ese nombre')
                return False
        return True

    # funcion para insertar segun fit ff
    def primary(self, fdisk_tamano, path, name, type, fit):
        # leer partitions en orden -> buscar la primera vacia -> ver si cabe -> insertar
        # tomar en cuenta el type de la particion
        # para esto se debe leer el mbr, y las partitions
        mbr_ = mbr()
        mbr_.leerBytes(path)
        '''print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
        for x in range (0,4):
            print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit, 'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)
        print(" ")    '''
        # en este punto ya se tiene toda la info en var mbr_
        start = mbr_.getSize()
        start += mbr_.partitions[0].getSize()*4
        # se llena la info del nuevo partition
        # print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
        for x in range(0, 4):
            # print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit, 'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)
            if mbr_.partitions[x].status == b'0':
                mbr_.partitions[x].status = b'1'
                mbr_.partitions[x].type = type.encode('utf-8')
                mbr_.partitions[x].fit = fit[1:].encode('utf-8')
                mbr_.partitions[x].start = start+1
                mbr_.partitions[x].s = fdisk_tamano
                mbr_.partitions[x].name = name[:16].ljust(16, " ")
                break
            else:
                start += mbr_.partitions[x].s
        # se debe escribir el mbr nuevamente
        # se convierte a bytes
        buffer = ""
        buffer = mbr_.getBytes()
        for x in range(0, 4):
            buffer += mbr_.partitions[x].getBytes()
        # se escribe en el dsk
        with open("."+path, "rb+") as file:
            file.seek(0)
            file.write(buffer)
        file.close()

        mbr_ = mbr()
        mbr_.leerBytes(path)
        # en este punto ya se tiene toda la info en var mbr_
        # se llena la info del nuevo partition
        print('size', mbr_.size, 'date', mbr_.date,
              'signature', mbr_.signature, 'fit', mbr_.fit)
        for x in range(0, 4):
            print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit,
                  'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)

    def extended(self, fdisk_tamano, path, name, type, fit):
        # leer partitions en orden -> buscar la primera vacia -> ver si cabe -> insertar
        # tomar en cuenta el type de la particion
        # para esto se debe leer el mbr, y las partitions
        mbr_ = mbr()
        mbr_.leerBytes(path)
        '''print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
        for x in range (0,4):
            print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit, 'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)
        print(" ")    '''
        # en este punto ya se tiene toda la info en var mbr_
        start = mbr_.getSize()
        start += mbr_.partitions[0].getSize()*4
        ebr_ = ebr()

        flag = False
        for x in range(0, 4):
            if mbr_.partitions[x].type == b'e' and mbr_.partitions[x].status == b'1':
                print('[err]ya existe una particion extendida')
                flag = True

        if flag == False:
            # se llena la info del nuevo partition
            # print('size', mbr_.size, 'date', mbr_.date, 'signature', mbr_.signature, 'fit', mbr_.fit)
            for x in range(0, 4):
                # print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit, 'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)
                if mbr_.partitions[x].status == b'0':
                    mbr_.partitions[x].status = b'1'
                    mbr_.partitions[x].type = type.encode('utf-8')
                    mbr_.partitions[x].fit = fit[1:].encode('utf-8')
                    mbr_.partitions[x].start = start+1
                    mbr_.partitions[x].s = fdisk_tamano
                    mbr_.partitions[x].name = name[:16].ljust(16, " ")

                    ebr_.part_status = b'0'
                    ebr_.part_start = mbr_.partitions[x].start
                    inicio_ebr = mbr_.partitions[x].start
                    break
                else:
                    start += mbr_.partitions[x].s
            # se debe escribir el mbr nuevamente
            # se convierte a bytes
            buffer = ""
            buffer = mbr_.getBytes()
            for x in range(0, 4):
                buffer += mbr_.partitions[x].getBytes()
            # se escribe en el dsk
            with open("."+path, "rb+") as file:
                file.seek(0)
                file.write(buffer)
                file.seek(inicio_ebr)
                file.write(ebr_.getBytes())
            file.close()

            # se debe escribir el ebr
            '''buffer=""
            buffer = ebr_.getBytes()
            with open("."+path, "rb+") as file:
                file.seek(inicio_ebr)
                file.write(buffer)
            file.close()'''

            mbr_ = mbr()
            mbr_.leerBytes(path)
            # en este punto ya se tiene toda la info en var mbr_
            # se llena la info del nuevo partition
            print('size', mbr_.size, 'date', mbr_.date,
                  'signature', mbr_.signature, 'fit', mbr_.fit)
            for x in range(0, 4):
                print('status', mbr_.partitions[x].status, 'type', mbr_.partitions[x].type, 'fit', mbr_.partitions[x].fit,
                      'start', mbr_.partitions[x].start, 's', mbr_.partitions[x].s, 'name', mbr_.partitions[x].name)

    def logic(self, fdisk_tamano, path, name, type, fit):
        mbr_ = mbr()
        mbr_.leerBytes(path)
        flag=False
        ebr_ = ebr()
        for x in range(0, 4):
            # revisar si hay particion extendida
            if mbr_.partitions[x].type == b'e':
                flag=True
                ubicacion = mbr_.partitions[x].start
                # leer ebr
                ebr_.leerBytes(path, ubicacion)
                ebr_.imprimir()
                # primer ebr
                if ebr_.part_status == b'0':
                    ebr_.part_status = b'1'
                    ebr_.part_fit = fit[1:].encode('utf-8')
                    ebr_.part_start = ubicacion
                    ebr_.part_s = fdisk_tamano
                    ebr_.part_next = ubicacion + fdisk_tamano + 1
                    ebr_.part_name = name[:16].ljust(16, " ")

                    with open("."+path, "rb+") as file:
                        file.seek(ubicacion)
                        file.write(ebr_.getBytes())
                    file.close()
                    print('primer ebr')
                    ebr_.imprimir()

                elif ebr_.part_status == b'1':
                    # bubscar ultimo ebr_
                    while ebr_.part_status == b'1':
                        ubicacion = ebr_.part_next
                        ebr_.leerBytes(path, ubicacion)
                        print('ebr')
                        ebr_.imprimir()
                    # insertar ebr
                    ebr_.part_status = b'1'
                    ebr_.part_fit = fit[1:].encode('utf-8')
                    ebr_.part_start = ubicacion
                    ebr_.part_s = fdisk_tamano
                    ebr_.part_next = ubicacion + fdisk_tamano + 1
                    ebr_.part_name = name[:16].ljust(16, " ")

                    with open("."+path, "rb+") as file:
                        file.seek(ubicacion)
                        file.write(ebr_.getBytes())
                    file.close()
                    print('nuevo ebr')
                    ebr_.imprimir()
        if flag==False:
            print('[err]no hay particion extendida')

    def deletePartition(self, path, name, delete):
        mbr_ = mbr()
        mbr_.leerBytes(path)
        # en este punto ya se tiene toda la info en var mbr_
        for x in range(0, 4):
            if mbr_.partitions[x].name == name[:16].ljust(16, " "):
                print('borrando')
                mbr_.partitions[x].status = b'0'
                mbr_.partitions[x].type = b'0'
                mbr_.partitions[x].fit = b'0'

                #borramos contenido del disk
                with open("."+path, "rb+") as file:
                    file.seek(mbr_.partitions[x].start)
                    file.write(b'\x00' * mbr_.partitions[x].s)
                file.close()

                #borramos mbr
                buffer = ""
                buffer = mbr_.getBytes()
                for x in range(0, 4):
                    buffer += mbr_.partitions[x].getBytes()
                # se escribe en el dsk
                with open("."+path, "rb+") as file:
                    file.seek(0)
                    file.write(buffer)
                file.close()

                mbr_ = mbr()
                mbr_.leerBytes(path)
                mbr_.imprimir()

