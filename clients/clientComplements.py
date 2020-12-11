import os
import const
import subprocess
from socketIO_client import SocketIO

ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\complements\\complements\\bin\\Debug\\netcoreapp3.1\\complements.exe")
#ejecutar el proyecto para tener el exe mas actualizado en caso de que hayan cambios

def tarea(args):
    global ruta
    print('Iniciando tarea con ' + args.replace(" ","-"))
    params=args.replace(" ","-")  #por si el nombre lleva espacios no lo entienda como mas de un parametro, en c# se acomoda!
    process = subprocess.Popen(ruta+" "+params, shell=True)  #inicia proceso, se ejecuta en esta misma consola
    process.wait()  #espera que termine el proceso
    socketIO.emit('endScrape', (const.COMPLEMENTS_SOCKET_TYPE, args))  #emite evento para decirle al server que ya termino la tarea

socketIO = SocketIO("https://young-harbor-56590.herokuapp.com") #se conecta al server
socketIO.on('start-' + const.COMPLEMENTS_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento

socketIO.emit('connect-socket', const.COMPLEMENTS_SOCKET_TYPE,broadcast=True)
print("Conectado y escuchando.\n")
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento