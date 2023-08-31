#partition-> status, type, fit, start, s, !!name --------------------------------------------------
class partition():
    def __init__(self, status=b'0', type=b'0', fit=b'0', start=0, s=0, name="a"):
        self.status = status
        self.type = type
        self.fit = fit
        self.start = start
        self.s = s
        self.name = name[:16].ljust(16, " ")

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
    
    def leerBytes(self,buffer):
        self.status= buffer[0:1]
        self.type= buffer[1:2]
        self.fit= buffer[2:3]
        self.start= int.from_bytes(buffer[3:7], byteorder= 'big')
        self.s= int.from_bytes(buffer[7:11], byteorder= 'big')
        self.name= buffer[11:27].decode('UTF-8')
        self.name=self.name.replace(" ", "")

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
