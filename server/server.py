import const
from flask import Flask,request,jsonify
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')



dataMetacriticScore={}
dataDixGamerPrice={}
dataIkuroGamePrice={}
dataComplements={}
dataHowLongToBeatTime = {}

finalData=[]
availableSockets={
    const.METACRITIC_SOCKET_TYPE: [],
    const.COMPLEMENTS_SOCKET_TYPE: [],
    const.DIX_SOCKET_TYPE: [],
    const.IKURO_SOCKET_TYPE: [],
    const.HLTB_SOCKET_TYPE: []
}

busySockets={
    const.METACRITIC_SOCKET_TYPE: [],
    const.COMPLEMENTS_SOCKET_TYPE: [],
    const.DIX_SOCKET_TYPE: [],
    const.IKURO_SOCKET_TYPE: [],
    const.HLTB_SOCKET_TYPE: []
}

@app.route('/')
def index():
    return "Hola soy el server principal"

############################################################################################################################################################
# Manejo de sockets

@socketio.on('connect-socket')  #evento que activa el cliente/modulo para conectarse
def connect(socketType):
    global availableSockets
    availableSockets[socketType].append(request.sid)
    print(availableSockets)
    print('> Socket ' + request.sid + ' added to ' + socketType + ' queue.')

""" Inserta el socket en la cola correspondiente

    Se encarga de notificar al servidor que hay un nuevo nodo conectado 
    y lo inserta en la cola al que corresponde

    Args:
      socketType:
        Un string con el tipo de socket que se conecto
          [En el archivo de constantes se encuentran los tipos]

    Returns:
      Nada
    """

@socketio.on('startScrape')  
def startScrape(data):
    print('----------- Starting Scrape with ' + str(data))
    global availableSockets, busySockets
    if len(availableSockets[data[1]]) > 0:
        client = availableSockets[data[1]].pop()
        busySockets[data[1]].append(client)
        print('--------------------- Socket ' + client + ' to complete the job.')
        socketio.emit('start-' + data[1], data[0], room=client)
    else:
        # Fallback for no available sockets
        return

""" Inicia cualquier tipo de scrapping

    Segun el socketType, se encarga de iniciar el scrapping si 
    existen clientes disponibles para realizar el scrape.

    Args:
      game:
        Un string con el nombre del juego a buscar
      socketType:
        Un string con el tipo de scrape a iniciar
          [En el archivo de constantes se encuentran los tipos]

    Returns:
      Nada
    """

@socketio.on('endScrape')
def endScrape(data):
    global availableSockets, busySockets
    busySockets[data[0]].remove(request.sid)
    availableSockets[data[0]].append(request.sid)
    
    if len(data) < 1:
        if data[0] == const.METACRITIC_SOCKET_TYPE:
            dataMetacriticScore.update(data[1])
        if data[0] == const.COMPLEMENTS_SOCKET_TYPE:
            dataComplements.update(data[1])
        if data[0] == const.DIX_SOCKET_TYPE:
            dataDixGamerPrice.update(data[1])
        if data[0] == const.IKURO_SOCKET_TYPE:
            dataIkuroGamePrice.update(data[1])
        if data[0] == const.HLTB_SOCKET_TYPE:
            dataHowLongToBeatTime.update(data[1])

""" Notifica al servidor que un cliente termino el scrapping

    Se encarga de avisar devolver al servidor los datos
    obtenidos del scrapping, asi como notificar que se encuentra
    disponible para realizar tareas de nuevo

    Args:
      data:
        Un objeto con los datos del scrape
      socketType:
        Un string con el tipo de scrape que realizó
          [En el archivo de constantes se encuentran los tipos]

    Returns:
      Nada
    """

############################################################################################################################################################
# Data para en frontend, se supone que el cliente principal va a armar todo y mandarlo a este endpoint

@app.route('/setData' , methods=['GET'])  #endpoint que recibe la data de el app de c#
def setData():
    for game in const.GAMES:
        startScrape((game, const.METACRITIC_SOCKET_TYPE))
        # startScrape((game, const.COMPLEMENTS_SOCKET_TYPE))
        # startScrape((game, const.DIX_SOCKET_TYPE))
        # startScrape((game, const.IKURO_SOCKET_TYPE))
        # startScrape((game, const.HLTB_SOCKET_TYPE))

@app.route('/getData' , methods=['GET'])  # endpoint que da la data al frontend
def getData():
    global finalData
    return jsonify(finalData)

############################################################################################################################################################
#MetacriticScore

@app.route('/setMetacritic' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setMetacritic():
    global dataMetacriticScore
    dataMetacriticScore.update(request.json)
    return jsonify({"status": "finalizada"})

@app.route('/getMetacritic' , methods=['GET'])  # endpoint que da la data si es que hay
def getMetacritic():
    global dataMetacriticScore
    return jsonify({"data": dataMetacriticScore})

@app.route('/getMetacritic/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getMetacriticGame(game=None):
    global dataMetacriticScore
    return jsonify({"data": dataMetacriticScore[game]})

############################################################################################################################################################



############################################################################################################################################################
#DixGamerPrice

@app.route('/setDixGamerPrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setDixGamerPrice():
    global dataDixGamerPrice
    dataDixGamerPrice.update(request.json)
    return jsonify({"status": "finalizada"})

@app.route('/getDixGamerPrice/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getDixGamerPrice(game=None):
    global dataDixGamerPrice
    if game == None:
        return jsonify({"data": dataDixGamerPrice})
    else:
        return jsonify({"data": dataDixGamerPrice[game]})

############################################################################################################################################################


############################################################################################################################################################
#IkuroGamePrice

@app.route('/setIkuroGamePrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setIkuroGamePrice():
    global dataIkuroGamePrice
    dataIkuroGamePrice.update(request.json)
    return jsonify({"status": "finalizada"})

@app.route('/getIkuroGamePrice/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getIkuroGamePrice(game):
    global dataIkuroGamePrice
    if game == None:
        return jsonify({"data": dataIkuroGamePrice})
    else:
        return jsonify({"data": dataIkuroGamePrice[game]})


############################################################################################################################################################

############################################################################################################################################################
#Complements
@app.route('/setComplements' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setComplements():
    global dataComplements
    dataComplements.update(request.json)
    return jsonify({"status": "finalizada"})

@app.route('/getComplements/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getComplements(game):
    global dataComplements
    if game == None:
        return jsonify({"data": dataComplements})
    else:
        return jsonify({"data": dataComplements[game]})


############################################################################################################################################################

############################################################################################################################################################
# HowLongToBeat

#No es necesario el setHowLongToBeatTime porque el cliente esta en python entonces pasa la data como parametro cuando termine

@app.route('/setHowLongToBeatTime' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setHowLongToBeatTime():
    global dataHowLongToBeatTime
    dataHowLongToBeatTime.update(request.json)
    return jsonify({"status": "finalizada"})

@app.route('/getHowLongToBeatTime/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getHowLongToBeatTime(game):
    global dataHowLongToBeatTime
    if game == None:
        return jsonify({"data": dataHowLongToBeatTime})
    else:
        return jsonify({"data": dataHowLongToBeatTime[game]})


############################################################################################################################################################


if __name__ == '__main__':
    #socketio.run()  #para correrlo en el server
    socketio.run(app, debug=True,port="5000") #para correrlo local