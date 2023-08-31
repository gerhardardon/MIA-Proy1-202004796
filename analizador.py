import argparse
from comandos.cmd_mkdisk import cmd_mkdisk 
from comandos.cmd_rmdisk import cmd_rmdisk 
from comandos.cmd_fdisk import cmd_fdisk

#funciones para comandos (reemplazar con clases)
def crear_disco(path, size, fit, unit):
    print(f"mkdisk path {path}, size {size}, fit {fit}, unit {unit}")
def crear_archivo(name, age):
    print(f"Creando archivo '{name}' con edad {age} años")

#main function 
def cmd_parser():
    #description
    parser = argparse.ArgumentParser(description='Comandos mkdisk y mkfile')

    # each subparser must be a proyect command
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')

    # first cmd MKDISK
    mkdisk_parser = subparsers.add_parser('mkdisk', help='Crear disco')
    mkdisk_parser.add_argument('-path', required=True, help='Ruta para el disco')
    mkdisk_parser.add_argument('-size', type=int, required=True, help='Tamaño del disco en MB')
    ## arguments -> (name, type, category, options, default option)
    mkdisk_parser.add_argument('-fit', type=str, required=False, choices=['bf','ff','wf'], default='ff')
    mkdisk_parser.add_argument('-unit', type=str, required=False, choices=['k','m'], default='m')
    
    # cmd RMDISK
    rmdisk_parser = subparsers.add_parser('rmdisk', help='remover disco')
    rmdisk_parser.add_argument('-path', required=True, help='Ruta para el disco')
    
    # cmd FDISK
    fdisk_parser = subparsers.add_parser('fdisk', help='Administrar particion')
    fdisk_parser.add_argument('-path', required=True, help='Ruta para la particion')
    fdisk_parser.add_argument('-size', type=int, required=True, help='Tamaño de la particion')
    fdisk_parser.add_argument('-name', type=str, required=True, help='Nombre de la particion')
    fdisk_parser.add_argument('-unit', type=str, required=False, choices=['b','k','m'], default='k')
    fdisk_parser.add_argument('-type', type=str, required=False, choices=['p','e','l'], default='p')
    fdisk_parser.add_argument('-fit', type=str, required=False, choices=['bf','ff','wf'], default='wf')
    fdisk_parser.add_argument('-delete', type=str, required=False, choices=['full'], default='full')
    fdisk_parser.add_argument('-add', type=int, required=False)
   
    args = parser.parse_args()
    entrada = 'fdisk -name=a -size=10 -path=/home/user/Disco1.dsk'

    #read the input, must be changed to file content
    try:
        args = parser.parse_args(entrada.split())
    except SystemExit:
        print("Entrada no válida")
        return

    #calls to cmd functions, must be classes ------------------------------------------
    if args.comando == 'mkdisk':
        if args.size <=0:
            print('error in size')
        else:
            path = args.path.strip('"')
            ##llamamos a la clase
            x=cmd_mkdisk()
            x.createDisk(args.size, path, args.fit, args.unit)

    elif args.comando == 'rmdisk':
        path = args.path.strip('"')
        ##llamamos a la clase
        x=cmd_rmdisk()
        x.removeDisk(path)

    elif args.comando == 'fdisk':
        if args.size <=0:
            print('error in size')
        else:
            path = args.path.strip('"')
            ##llamamos a la clase
            x=cmd_fdisk()
            x.createFdisk(args.size, args.path, args.name, args.unit, args.type, args.fit)

    elif args.comando == 'mkfile':
        crear_archivo(args.name, args.age)
    else:
        print("Comando no reconocido")

cmd_parser()