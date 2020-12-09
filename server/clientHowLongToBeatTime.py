import datetime
import const
from socketIO_client import SocketIO
from howlongtobeatpy import HowLongToBeat

name=''

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

    socketIO.emit('endScrape', (const.HLTB_SOCKET_TYPE, json))  #emite evento para decirle al server que ya termino la tarea

    print("Proceso exitoso!\n");

def tarea(args):
    global name
    print("Proceso HowLongToBeat")
    try:
        print('Iniciando tarea con ' + args.replace(" ","-"))
        name=args
        results = HowLongToBeat(0).search(args)
        result = max(results, key=lambda element: element.similarity).gameplay_main
        if result != -1:
            send_json(format_result(result))  # Da formato al valor obtenido, intercambia '½' por '.30'
        else:
            send_json("n/a")
    except ValueError as e:
        print(e)

socketIO = SocketIO("http://localhost",5000) #se conecta al server
socketIO.on('start-' + const.HLTB_SOCKET_TYPE, tarea)  # define que hacer cuando se actice el evento

socketIO.emit('connect-socket', const.HLTB_SOCKET_TYPE)
print("Conectado y escuchando.\n")
socketIO.wait()  #queda escuchando al server en caso de que se active algun evento