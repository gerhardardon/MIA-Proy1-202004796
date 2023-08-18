import argparse

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
    
    # cmd MKFILE
    mkfile_parser = subparsers.add_parser('mkfile', help='Crear archivo')
    mkfile_parser.add_argument('-name', required=True, help='Nombre del archivo')
    mkfile_parser.add_argument('-age', type=int, required=True, help='Edad del archivo')

    args = parser.parse_args()


    entrada = 'mkdisk -size=10 -path="/home/misdiscos/Disco4.dsk"'

    #read the input, must be changed to file content
    try:
        args = parser.parse_args(entrada.split())
    except SystemExit:
        print("Entrada no válida")
        return

    #calls to cmd functions, must be classes
    if args.comando == 'mkdisk':
        path = args.path.strip('"')
        crear_disco(path, args.size, args.fit, args.unit)
    elif args.comando == 'mkfile':
        crear_archivo(args.name, args.age)
    else:
        print("Comando no reconocido")

cmd_parser()