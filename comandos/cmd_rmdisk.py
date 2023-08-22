import os

class cmd_rmdisk:
    def removeDisk(self, path):
        try:
            os.remove('.'+path)
            print ('disco removido')
        except:
            print('disco no encontrado')