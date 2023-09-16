#partition-> status, type, fit, start, s, !!name --------------------------------------------------
mounted=[]

class partition():
    def __init__(self, status=b'0', type=b'0', fit=b'0', start=0, s=0, name="0"):
        self.status = status
        self.type = type
        self.fit = fit
        self.start = start
        self.s = s
        self.name = name[:16].ljust(16, " ")

    def imprimir(self):
        print('status', self.status, 'type', self.type, 'fit', self.fit, 'start', self.start, 's', self.s, 'name', self.name)
    
    def getBytes(self):
        buffer=bytearray()
        buffer+= self.status
        buffer+= self.type
        buffer+= self.fit
        buffer+= self.start.to_bytes(4, byteorder='big')  # int -4bytes
        buffer+= self.s.to_bytes(4, byteorder='big')      # int -4bytes
        buffer+= self.name.encode('UTF-8')
        return buffer
    
    def leerBytes(self,buffer):
        self.status= buffer[0:1]
        self.type= buffer[1:2]
        self.fit= buffer[2:3]
        self.start= int.from_bytes(buffer[3:7], byteorder= 'big')
        self.s= int.from_bytes(buffer[7:11], byteorder= 'big')
        self.name= buffer[11:27].decode('UTF-8')

    def getSize(self):
        size=0
        size+= 3
        size+= 8
        size+= 16
        return size

#mbr -> tamaño, fecha, signature, fit, partitions --------------------------------------------------
class mbr():
    def __init__(self, size="", date="", signature="", fit=""):
        self.size = size
        self.date = date
        self.signature = signature
        self.fit = fit
        self.partitions = []

    def getSize(self):
        size= 0
        size+= 4 # int -4bytes
        size+= 4 # int -4bytes
        size+= 4 # int -4bytes
        size+= 1 # char -1bytes
        return size
    
    def getBytes(self):
        buffer=bytearray()
        buffer+= self.size.to_bytes(4, byteorder='big')          # int -4bytes
        buffer+= self.date.to_bytes(4, byteorder='big')          # int -4bytes
        buffer+= self.signature.to_bytes(4, byteorder='big')     # int -4bytes
        buffer+= self.fit.encode('utf-8')                        # char -1bytes
        return buffer

    
    def leerBytes(self, path):
        ## leer solo los bytes de MBR 
        part= partition()
        size= self.getSize() + (part.getSize()*4)
        with open("."+path, "rb") as file:
            ## leer solo los bytes de partitions
            buffer = file.read(size)
        file.close()

        ##llenar var de objeto MBR
        self.size= int.from_bytes(buffer[0:4], byteorder= 'big')
        self.date= int.from_bytes(buffer[4:8], byteorder= 'big')
        self.signature= int.from_bytes(buffer[8:12], byteorder= 'big')
        self.fit= buffer[12:13].decode('UTF-8')
        buffer= buffer[13:]

        ##llenar var de objeto partitions
        for x in range(0,4):
            part=partition()
            part.leerBytes(buffer)
            buffer= buffer[27:]

            self.partitions.append(part)
    
    def imprimir(self):
        print('size', self.size, 'date', self.date, 'signature', self.signature, 'fit', self.fit)
        for x in self.partitions:
            x.imprimir()

class ebr():
    def __init__(self, part_status=b'0', part_fit=b'0', part_start=0, part_s=0, part_next=0, part_name=' '):
        self.part_status = part_status
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_s = part_s
        self.part_next = part_next
        self.part_name = part_name[:16].ljust(16, " ")

    def getBytes(self):
        buffer=bytearray()
        buffer+= self.part_status
        buffer+= self.part_fit
        buffer+= self.part_start.to_bytes(4, byteorder='big')
        buffer+= self.part_s.to_bytes(4, byteorder='big')
        buffer+= self.part_next.to_bytes(4, byteorder='big')
        buffer+= self.part_name.encode('UTF-8')
        return buffer 
    
    def getSize(self):
        size=0
        size+= 1
        size+= 1
        size+= 4
        size+= 4
        size+= 4
        size+= 16
        return size
    
    def leerBytes(self,path,start):
         
        with open("."+path, "rb") as file:
            ## leer solo los bytes de ebr
            file.seek(start)
            buffer = file.read(30)
        file.close()
    
        self.part_status= buffer[0:1]
        self.part_fit= buffer[1:2]
        self.part_start= int.from_bytes(buffer[2:6], byteorder= 'big')
        self.part_s= int.from_bytes(buffer[6:10], byteorder= 'big')
        self.part_next= int.from_bytes(buffer[10:14], byteorder= 'big')
        self.part_name= buffer[14:30].decode('UTF-8')
    
    def imprimir(self):
        print('status', self.part_status, 'fit', self.part_fit, 'start', self.part_start, 's', self.part_s, 'next', self.part_next, 'name', self.part_name)
