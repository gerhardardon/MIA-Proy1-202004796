from comandos.objects import*
import os

class cmd_mount:

    def mountPartition(self, path, name):
        if os.path.exists('.'+path):
            disco=path.split('/')[-1]
            disco=disco.split('.')[0]
            id="96"+name[-1]+disco 
            if id not in mounted:
                mounted.append(id)
                print('particion montada')
                print('partciones montadas: ', mounted)
            else:
                print("[err]particion ya montada")
    
    def unmountPartition(self, id):
        if id in mounted:
            mounted.remove(id)
            print('particion desmontada')
        else:
            print("[err]particion no montada")