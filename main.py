#!/usr/bin/python
# -*- coding: latin-1 -*-

import getopt
from rethinkdb import RethinkDB
import sys
import json

r = RethinkDB()

def abrirConexion() :
    global r
    global conn
    try:
        conn = r.connect("trabajo_rethinkdb_1", 28015).repl()
    except:
        print('No se ha podido abrir conexion con rethinkdb')
        sys.exit(2)
def cerrarConexión():
    global conn
    conn.close()

def crearBaseDeDatos(nombre):
    global r

    print('Se va a crear la base de datos con el nombre: '+nombre+'\n -------------')
    abrirConexion()
    try:
        r.db_create(nombre).run()
        print('Se ha creado la base de datos '+nombre+' correctamente')
    except:
        print('Ya existe la base de datos '+nombre)
        print('\nEstas son las bases de datos que existen:')
        for doc in r.db_list().run():
            print('- '+str(doc))
        print(' ')
    cerrarConexión()

def borrarBaseDeDatos(nombre):
    global r

    print('Se va a borrar la base de datos con el nombre: '+nombre+'\n -------------')
    abrirConexion()
    try:
        r.db_drop(nombre).run()
        print('Se ha borrado la base de datos '+nombre+' correctamente')
    except:
        print('ERROR: No existe la base de datos '+nombre+' o el formato no es el correcto.')
        print('\nEstas son las bases de datos que existen:')
        for doc in r.db_list().run():
            print('- '+str(doc))
        print(' ')
    cerrarConexión()

def crearTabla(nombreTabla): # Opción -t
    global r
    nombreBD = input('Añadir el nombre de la base de datos:\n')
    abrirConexion()

    print('Se va a crear la tabla '+nombreTabla+' en la base de datos con el nombre: ' + nombreTabla + '\n -------------')
    try:
        r.db(nombreBD).table_create(nombreTabla).run()
        print('Se ha creado la tabla '+nombreTabla)

    except:
        print('ERROR: No se ha podido crear la tabla ' + nombreTabla + ' en la base de datos con el nombre: ' + nombreTabla + '\nPor favor, revise los parametros')
        sys.exit(2)
def test(nombreBD): # Opcion -e
    global r
    print('- Test de conexion: \n ---------')
    abrirConexion()
    print('# Conexion correcta.')

    if nombreBD in r.db_list().run():
        db = r.db(nombreBD)
        print('# La base de datos '+nombreBD+' existe')
    else:
        print('# ERROR 1: La base de datos no existe. \n Estas son las bases de datos disponibles en el sistema:')
        for doc in r.db_list().run():
            print('- ' + str(doc))

        sys.exit(2)




    print('\n- Test de el estado de la tabla')
    nombreTabla = input(' Que tabla deseas mirar el estado?  ')

    try:
        print(db.table(nombreTabla).status().run())
    except:
        print('# ERROR 2: No existe la tabla con el nombre '+nombreTabla+' o el formato no es correcto.\n Estas son las tablas que tiene la base de datos '+nombreBD+':')
        for doc in db.table_list().run():
            print('- '+str(doc))
        print(' ')
        sys.exit(2)


# def escribirTabla(nombreBD):
#     global r
#     abrirConexion()
#     nombreTabla = input('En que tabla deseas escribir?  ')
#     rutaJson = input('Escribe la ruta completa de donde esta el archivo json que deseas subir')
#
#     try:
#         textJson = open(rutaJson).read()
#         print('Archivo que se va a subir a la base de datos '+nombreBD+':')
#         print(textJson)
#
#     except:
#         print('La ubicación de el archivo no es correcta')
#         sys.exit(2)
#
#     try:
#         r.db(nombreBD).table(nombreTabla).insert(textJson)
#         print('Se ha insertado correctamente el documento')
#     except:
#         print('ERROR: No se ha podido insertar el documento, revise los parametros y el formato del documento a subir')


if __name__ == "__main__":
    print('\n\n')
    print('  ##############')
    print('  # RETHINKDB: #')
    print('  ##############')
    print('\n\n')
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "c:d:t:e:")
    except getopt.GetoptError:
        #error
        print(
            'Ayuda: trabajo.py -c <name> (Nombre de la base de datos a crear) -d <name> (Nombre de la base de datos a borrar) -t <name> (nombre tabla a crear) -e <nombre> (Leer el estado de la BBDD)')
        print("Si algun argumento tiene espacios es IMPORTANTE ponerlo entre estas comillas: \"\"")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                'Ayuda: trabajo.py -c <name> (Nombre de la base de datos a crear) -d <name> (Nombre de la base de datos a borrar) -t <name> (nombre tabla a crear) -e <nombre> (Leer el estado de la BBDD)')
            print("Si algun argumento tiene espacios es IMPORTANTE ponerlo entre estas comillas: \"\"")
            sys.exit(2)
        elif opt in "-c":
            crearBaseDeDatos(arg)
        elif opt in "-d":
            borrarBaseDeDatos(arg)
        elif opt in "-t":
            crearTabla(arg)
        elif opt in "-e":
            test(arg)

    while True:
        print('\n\nQue quieres hacer?')
        print('- c: Crear una base de datos')
        print('- d: Borrar una base de datos')
        print('- t: Crear una tabla')
        print('- e: Ver el estado de la tabla de una BBDD')
        print('+ Presiona CTRL+C para salir\n')
        eleccion = input('Eleccion: ')
        print('-----------------------------------------------')
        if eleccion == "c":
            arg = input('Cual es el nombre de la base de datos que quieres crear?\n')
            crearBaseDeDatos(arg)
        elif eleccion == "d":
            arg = input('Cual es el nombre de la base de datos que quieres borrar?\n')
            borrarBaseDeDatos(arg)
        elif eleccion == "t":
            arg = input('Cual es el nombre de la tabla?\n')
            crearTabla(arg)
        elif eleccion == "e":
            arg = input('Cual es el nombre de la base de datos?\n')
            test(arg)
        print('\n--------------------------------------------------------\n\n')


