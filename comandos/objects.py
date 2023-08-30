#partition-> status, type, fit, start, s, !!name --------------------------------------------------
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

#mbr -> tamaño, fecha, signature, fit, partitions --------------------------------------------------
class mbr():
    def __init__(self, size, date, signature, fit):
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