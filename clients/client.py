import datetime
import const
import subprocess
from socketIO_client import SocketIO
from howlongtobeatpy import HowLongToBeat
import os
name=''
ruta=''

# Función para dar formato a los números antes de ser escritos en un archivo
def format_result(time_to_beat):
    half_index = time_to_beat.find('½')               # Retorna el índice donde se encuentra el caracter '½'
    if half_index != -1:                              # Si el caracter '½' existe en el string...
        return time_to_beat[0:half_index] + '.30'     # retorna el número antes del '½' y lo sustituye por '.30'
    return time_to_beat                               # De lo contrario retorna el número de horas (sin 'h.')

def send_json(timeToBeat):
    global name
    #Da el mismo formato establecido para el tiempo (igual que en los módulos de C#)
    today = datetime.date.today().strftime("%d-%m-%Y")
    time = datetime.datetime.now()
    time_format = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second) + "." + str(time.microsecond)

    data = {'name': name, 'time': timeToBeat}

    # Se arma el json
    json = {"type": "howLongToBeat", "date": today + "$" + time_format, "data": data}

    socketIO.emit('endScrape', (const.HLTB_SOCKET_TYPE, name, json))  #emite evento para decirle al server que ya termino la tarea

    print("Proceso exitoso!\n");

def hltb(args):
    global name
    print("\nProceso HLTB")
    try:
        print('Iniciando tarea con ' + args[0].replace(" ","-"))
        name=args[0]
        results = HowLongToBeat(0).search(args[0])
        result = max(results, key=lambda element: element.similarity).gameplay_main
        if result != -1:
            send_json(format_result(result))  # Da formato al valor obtenido, intercambia '½' por '.30'
        else:
            send_json("n/a")
    except ValueError as e:
        print(e)

def tarea(args):
    global ruta

    if args[1] == const.DIX_SOCKET_TYPE:
        ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\dixGamerPrices\\dixGamerPrices\\bin\\Debug\\netcoreapp3.1\\dixGamerPrices.exe")
    elif  args[1] == const.IKURO_SOCKET_TYPE:
        ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\ikuroGamesPrices\\ikuroGamesPrices\\bin\\Debug\\netcoreapp3.1\\ikuroGamesPrices.exe")
    elif  args[1] == const.COMPLEMENTS_SOCKET_TYPE:
        ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\complements\\complements\\bin\\Debug\\netcoreapp3.1\\complements.exe")
    else:
        ruta=os.path.join(os.path.dirname(__file__), "..\\modulos\\metacriticScores\\metacriticScores\\bin\\Debug\\netcoreapp3.1\\metacriticScores.exe")

    params=args[0].replace(" ","-")  #por si el nombre lleva espacios no lo entienda como mas de un parametro, en c# se acomoda!
    print("\nProceso "+str(args[1]))
    print('Iniciando tarea con ' + str(params))
    process = subprocess.Popen(ruta+" "+params, shell=True)  #inicia proceso, se ejecuta en esta misma consola
    process.wait()  #espera que termine el proceso
    socketIO.emit('endScrape', (args[1], args[0]))  #emite evento para decirle al server que ya termino la tarea

socketIO = SocketIO("http://young-harbor-56590.herokuapp.com") #se conecta al server
socketIO.on('start-' + const.HLTB_SOCKET_TYPE, hltb)  # define que hacer cuando se actice el evento
socketIO.on('start-' + const.DIX_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento
socketIO.on('start-' + const.IKURO_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento
socketIO.on('start-' + const.COMPLEMENTS_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento
socketIO.on('start-' + const.METACRITIC_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento

socketIO.emit('connect-socket', const.HLTB_SOCKET_TYPE)  # empieza con la tarea mas rapida

print("Conectado y escuchando.\n")
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento