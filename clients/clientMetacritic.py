import os
import const
import subprocess
from socketIO_client import SocketIO

ruta=os.path.join(os.path.dirname(__file__), "..\\modules\\metacriticScores\\metacriticScores\\bin\\Debug\\netcoreapp3.1\\metacriticScores.exe")
#ejecutar el proyecto para tener el exe mas actualizado en caso de que hayan cambios

def tarea(args):
    global ruta
    params=args[0].replace(" ","-")  #por si el nombre lleva espacios no lo entienda como mas de un parametro, en c# se acomoda!
    print('Iniciando tarea con ' + params)
    process = subprocess.Popen(ruta+" "+params, shell=True)  #inicia proceso, se ejecuta en esta misma consola
    process.wait()  #espera que termine el proceso
    socketIO.emit('endScrape', (const.METACRITIC_SOCKET_TYPE, args[0]))  #emite evento para decirle al server que ya termino la tarea

socketIO = SocketIO("http://young-harbor-56590.herokuapp.com") #se conecta al server
socketIO.on('start-' + const.METACRITIC_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento

print("Conectado y escuchando.\n")
socketIO.emit('connect-socket', const.METACRITIC_SOCKET_TYPE)
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento