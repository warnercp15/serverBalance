import const
from flask import Flask,request,jsonify
from flask_socketio import SocketIO,emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
socketio = SocketIO(app, cors_allowed_origins="*",async_mode='eventlet')

port = int(os.environ.get("PORT", 5000))

finalData=[]

requestStack = {
    const.METACRITIC_SOCKET_TYPE: [],
    const.COMPLEMENTS_SOCKET_TYPE: [],
    const.DIX_SOCKET_TYPE: [],
    const.IKURO_SOCKET_TYPE: [],
    const.HLTB_SOCKET_TYPE: []
}

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

listComplement=[]
listDixGamerPrice=[]
listIkuroGamePrice=[]
listHowLongToBeatTime=[]
listMetacriticScore=[]
listNames=[]


'''
La idea es que existe para cada tipo de modulo una lista
y tambien una lista de nombres, cada vez que un modulo termine una tarea, anade el nombre del juego que termino
para despues recorrer esa lista de nombre que es mas liviana y verificar si estan los 5 nombres de cada juego,
si estan procede a armar la data y anadirla a la lista y emitir la lista con la data nueva
'''

def haveAllData(name):
    global listComplement,listDixGamerPrice,listIkuroGamePrice,listHowLongToBeatTime,listMetacriticScore,listNames,finalData

    print('len(listNames): ' + str(len(listNames)))
    print('len(const.GAMES): ' + str(len(const.GAMES)*5))
    resNames = [x for x in listNames if x == name]  # se creo un lista con los nombres porque es mas rapido que recorrer que con los objetos

    if len(resNames) == 5:
        print()
        print('Starting data parsing')
        #cuando encuentre el nombre 5 veces quiere decir que tiene todos los datos

        resComplement=[x for x in listComplement if x["name"]== name]
        resDixGamerPrice=[x for x in listDixGamerPrice if x["name"]== name]
        resIkuroGamePrice=[x for x in listIkuroGamePrice if x["name"]== name]
        resHowLongToBeatTime=[x for x in listHowLongToBeatTime if x["name"]== name]
        resMetacriticScore=[x for x in listMetacriticScore if x["name"]== name]

        #empieza a armar la data

        n1=resDixGamerPrice[0]["price"]
        n2=resIkuroGamePrice[0]["price"]
        precio=""
        offer=False

        #acomoda los precios, si n1 es negativo es que hay oferta
        if float(n1)<0:
            offer=True

            if float(n1*-1)<float(n2):
                precio = "$" + str(float(n1* -1)) + "-$" + str(n2)

            elif float(n1*-1)==float(n2):
                precio = "$" + str(n2)

            else:
                precio = "$" + str(n2) + "-$" + str(float(n1 * -1))
        else:

            if float(n1)<float(n2):
                precio = "$" + str(n1) + "-$" + str(n2)

            elif float(n1*-1)==float(n2):
                precio = "$" + str(n2)

            else:
                precio = "$" + str(n2) + "-$" + str(n1)

        jsonData={
            "offer":offer,
            "name":name,
            "imageUrl":resComplement[0]["image"],
            "price":precio,
            "score":resMetacriticScore[0]["score"],
            "timeToBeat":resHowLongToBeatTime[0]["time"]+"h"
        }

        finalData.append(jsonData) #lo agrega a la lista de juegos que va a consultar el frontend
        socketio.emit('onNewData', jsonData,broadcast=True)  #emite nuevo juego

        if len(finalData)==len(const.GAMES):
            finalData=[]
            socketio.emit('end', [], broadcast=True)  # emite nuevo juego

@app.route('/')
def index():
    return "Hola soy el server principal"

############################################################################################################################################################

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
        client = availableSockets[data[1]].pop(0)
        busySockets[data[1]].append(client)
        print('--------------------- Socket ' + client + ' to complete the job.')
        socketio.emit('start-' + data[1], data[0], room=client)
    else:
        requestStack[data[1]].append(data[0])
        print('--------------------- Addedd to the ' + data[1].upper() + ' queue.')
        #return

""" Inicia cualquier tipo de scrapping

    Segun el socketType, se encarga de iniciar el scrapping si 
    existen clientes disponibles para realizar el scrape.

    Args:
      data:
        [0]: Un string con el nombre del juego a buscar
        [1]: Un string con el tipo de scrape a iniciar
          [En el archivo de constantes se encuentran los tipos]

    Returns:
      Nada
    """

@socketio.on('endScrape')
def endScrape(data):
    global availableSockets, busySockets, listNames, listComplement, listDixGamerPrice, listIkuroGamePrice, listHowLongToBeatTime, listMetacriticScore
    listNames.append(data[1])  # se termino tarea, agrego nombre
    
    if data[0] == const.METACRITIC_SOCKET_TYPE:
        if len(data) > 2:
            listMetacriticScore.append(data[2])

        haveAllData(data[1])  # se termino tarea, agrego nombre
        if len(requestStack[const.METACRITIC_SOCKET_TYPE]) > 0:
            print('------------ Theres processes in queue for ' + data[0] + ', socket ' + request.sid + ' will continue with next in queue ')
            socketio.emit('start-' + data[0], requestStack[const.METACRITIC_SOCKET_TYPE].pop(0), room=request.sid)
            return
    elif data[0] == const.COMPLEMENTS_SOCKET_TYPE:
        if len(data) > 2:
            listComplement.append(data[2])

        haveAllData(data[1])  # se termino tarea, agrego nombre
        if len(requestStack[const.COMPLEMENTS_SOCKET_TYPE]) > 0:
            print('------------ Theres processes in queue for ' + data[0] + ', socket ' + request.sid + ' will continue with next in queue ')
            socketio.emit('start-' + data[0], requestStack[const.COMPLEMENTS_SOCKET_TYPE].pop(0), room=request.sid)
            return
    elif data[0] == const.DIX_SOCKET_TYPE:
        if len(data) > 2:
            listDixGamerPrice.append(data[2])

        haveAllData(data[1])  # se termino tarea, agrego nombre
        if len(requestStack[const.DIX_SOCKET_TYPE]) > 0:
            print('------------ Theres processes in queue for ' + data[0] + ', socket ' + request.sid + ' will continue with next in queue ')
            socketio.emit('start-' + data[0], requestStack[const.DIX_SOCKET_TYPE].pop(0), room=request.sid)
            return
    elif data[0] == const.IKURO_SOCKET_TYPE:
        if len(data) > 2:
            listIkuroGamePrice.append(data[2])

        haveAllData(data[1])  # se termino tarea, agrego nombre
        if len(requestStack[const.IKURO_SOCKET_TYPE]) > 0:
            print('------------ Theres processes in queue for ' + data[0] + ', socket ' + request.sid + ' will continue with next in queue ')
            socketio.emit('start-' + data[0], requestStack[const.IKURO_SOCKET_TYPE].pop(0), room=request.sid)
            return
    elif data[0] == const.HLTB_SOCKET_TYPE:
        print(data[0].upper() + '------------ Socket ' + request.sid + ' ended processing ' + data[1])

        if len(data) > 2:
            listHowLongToBeatTime.append(data[2]['data'])
        haveAllData(data[1])  # se termino tarea, agrego nombre
        if len(requestStack[const.HLTB_SOCKET_TYPE]) > 0:
            # print('------------ Theres processes in queue for ' + data[0] + ', socket ' + request.sid + ' will continue with next in queue ')
            socketio.emit('start-' + data[0], requestStack[const.HLTB_SOCKET_TYPE].pop(0), room=request.sid)
            return

    print(data[0].upper() + '-------- No more requests in queue')
    busySockets[data[0]].remove(request.sid)
    availableSockets[data[0]].append(request.sid)

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

@socketio.on('startAll')
def startAll():
    global listComplement,listDixGamerPrice,listIkuroGamePrice,listHowLongToBeatTime,listMetacriticScore,listNames,finalData, requestStack

    # Reset data
    listMetacriticScore=[]
    listDixGamerPrice=[]
    listIkuroGamePrice=[]
    listComplement=[]
    listHowLongToBeatTime=[]
    listNames=[]

    requestStack = {
        const.METACRITIC_SOCKET_TYPE: [],
        const.COMPLEMENTS_SOCKET_TYPE: [],
        const.DIX_SOCKET_TYPE: [],
        const.IKURO_SOCKET_TYPE: [],
        const.HLTB_SOCKET_TYPE: []
    }

    for game in const.GAMES:
        startScrape((game, const.METACRITIC_SOCKET_TYPE))
        startScrape((game, const.COMPLEMENTS_SOCKET_TYPE))
        startScrape((game, const.DIX_SOCKET_TYPE))
        startScrape((game, const.IKURO_SOCKET_TYPE))
        startScrape((game, const.HLTB_SOCKET_TYPE))

@app.route('/setData/<game>' , methods=['GET'])  #endpoint que recibe la data de el app de c#
def setDataGame(game):
    startScrape((game, const.METACRITIC_SOCKET_TYPE))
    startScrape((game, const.COMPLEMENTS_SOCKET_TYPE))
    startScrape((game, const.DIX_SOCKET_TYPE))
    startScrape((game, const.IKURO_SOCKET_TYPE))
    startScrape((game, const.HLTB_SOCKET_TYPE))

@socketio.on('addGame')  #evento agrega los datos de un juego
def addGame(data):
    finalData.append(data)

@app.route('/getData' , methods=['GET'])  # endpoint que da la data al frontend
def getData():
    global finalData
    return jsonify(finalData)

############################################################################################################################################################
#MetacriticScore

@app.route('/setMetacritic' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setMetacritic():
    global listMetacriticScore
    listMetacriticScore.append(request.json['data'])
    return jsonify({"status": "finalizada"})

@app.route('/getMetacritic' , methods=['GET'])  # endpoint que da la data si es que hay
def getMetacritic():
    global listMetacriticScore
    return jsonify({"data": listMetacriticScore})

@app.route('/getMetacritic/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getMetacriticGame(game):
    global listMetacriticScore
    return jsonify({"data": [x for x in listMetacriticScore if x['name'] == game]})

############################################################################################################################################################



############################################################################################################################################################
#DixGamerPrice

@app.route('/setDixGamerPrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setDixGamerPrice():
    global listDixGamerPrice
    listDixGamerPrice.append(request.json['data'])
    return jsonify({"status": "finalizada"})

@app.route('/getDixGamerPrice' , methods=['GET'])  # endpoint que da la data si es que hay
def getDixGamerPrice():
    global listDixGamerPrice
    return jsonify({"data": listDixGamerPrice})

@app.route('/getDixGamerPrice/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getDixGamerPriceGame(game):
    global listDixGamerPrice
    return jsonify({"data": [x for x in listDixGamerPrice if x['name'] == game]})

############################################################################################################################################################


############################################################################################################################################################
#IkuroGamePrice

@app.route('/setIkuroGamePrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setIkuroGamePrice():
    global listIkuroGamePrice
    listIkuroGamePrice.append(request.json['data'])
    return jsonify({"status": "finalizada"})

@app.route('/getIkuroGamePrice' , methods=['GET'])  # endpoint que da la data si es que hay
def getIkuroGamePrice():
    global listIkuroGamePrice
    return jsonify({"data": listIkuroGamePrice})

@app.route('/getIkuroGamePrice/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getIkuroGamePriceGame(game):
    global listIkuroGamePrice
    return jsonify({"data": [x for x in listIkuroGamePrice if x['name'] == game]})


############################################################################################################################################################

############################################################################################################################################################
#Complements
@app.route('/setComplements' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setComplements():
    global listComplement
    listComplement.append(request.json['data'])
    return jsonify({"status": "finalizada"})

@app.route('/getComplements' , methods=['GET'])  # endpoint que da la data si es que hay
def getComplements():
    global listComplement
    return jsonify({"data": listComplement})

@app.route('/getComplements/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getComplementsGame(game):
    global listComplement
    return jsonify({"data": [x for x in listComplement if x['name'] == game]})


############################################################################################################################################################

############################################################################################################################################################
# HowLongToBeat

#No es necesario el setHowLongToBeatTime porque el cliente esta en python entonces pasa la data como parametro cuando termine

@app.route('/setHowLongToBeatTime' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setHowLongToBeatTime():
    global listHowLongToBeatTime
    listHowLongToBeatTime.append(request.json['data'])
    return jsonify({"status": "finalizada"})

@app.route('/getHowLongToBeatTime' , methods=['GET'])  # endpoint que da la data si es que hay
def getHowLongToBeatTime():
    global listHowLongToBeatTime
    return jsonify({"data": listHowLongToBeatTime})

@app.route('/getHowLongToBeatTime/<game>' , methods=['GET'])  # endpoint que da la data si es que hay
def getHowLongToBeatTimeGame(game):
    global listHowLongToBeatTime
    return jsonify({"data": [x for x in listHowLongToBeatTime if x['name'] == game]})


############################################################################################################################################################
if __name__ == '__main__':
    #socketio.run()  #para correrlo en el server
    socketio.run(app,debug=True,host='0.0.0.0',port=port) #para correrlo local