import os
import const
import subprocess
from socketIO_client import SocketIO

ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\metacriticScores\\metacriticScores\\bin\\Debug\\netcoreapp3.1\\metacriticScores.exe")
#ejecutar el proyecto para tener el exe mas actualizado en caso de que hayan cambios

def tarea(args):
    print('Iniciando tarea con ' + args.replace(" ","-"))
    global ruta
    params=args.replace(" ","-")  #por si el nombre lleva espacios no lo entienda como mas de un parametro, en c# se acomoda!
    process = subprocess.Popen(ruta+" "+params, shell=True)  #inicia proceso, se ejecuta en esta misma consola
    process.wait()  #espera que termine el proceso
    socketIO.emit('endScrape', (const.METACRITIC_SOCKET_TYPE, args))  #emite evento para decirle al server que ya termino la tarea

socketIO = SocketIO("http://localhost",5000) #se conecta al server
socketIO.on('start-' + const.METACRITIC_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento

print("Conectado y escuchando.\n")
socketIO.emit('connect-socket', const.METACRITIC_SOCKET_TYPE)
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento