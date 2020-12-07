from socketIO_client import SocketIO
import subprocess

ruta="C:\\Users\\warner\\Desktop\\modulos\\ikuroGamesPrices\\ikuroGamesPrices\\bin\\Debug\\netcoreapp3.1\\ikuroGamesPrices.exe"
#ejecutar el proyecto para tener el exe mas actualizado en caso de que hayan cambios

def tarea(args):
    global ruta
    params=args.replace(" ","-")  #por si el nombre lleva espacios no lo entienda como mas de un parametro, en c# se acomoda!
    process = subprocess.Popen(ruta+" "+params, shell=True)  #inicia proceso, se ejecuta en esta misma consola
    process.wait()  #espera que termine el proceso
    socketIO.emit('finIkuroGamePrice')  #emite evento para decirle al server que ya termino la tarea

socketIO = SocketIO("http://localhost",5000) #se conecta al server
socketIO.on('onIkuroGamePrice', tarea)  # define que hacer cuando se actice el evento

print("Conectado y escuchando.\n")
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento