import json

from flask import Flask,request,jsonify
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

tareaMetacriticScoreTerminada=False
tareaDixGamerPriceTerminada=False
tareaIkuroGamePriceTerminada=False
tareaComplements=False
tareaHowLongToBeatTimeTerminada = False

dataMetacriticScore=None
dataDixGamerPrice=None
dataIkuroGamePrice=None
dataComplements=None
dataHowLongToBeatTime = None

finalData=[]

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
    global listComplement,listDixGamerPrice,listIkuroGamePrice,listHowLongToBeatTime,listMetacriticScore,listNames

    #cuando encuentre el nombre 5 veces quiere decir que tiene todos los datos
    resNames = [x for x in listNames if x == name]  #se creo un lista con los nombres porque es mas rapido que recorrer que con los objetos

    if len(resNames)==5:
        resComplement=[x for x in listComplement if x["name"]== name]
        resDixGamerPrice=[x for x in listDixGamerPrice if x["name"]== name]
        resIkuroGamePrice=[x for x in listIkuroGamePrice if x["name"]== name]
        resHowLongToBeatTime=[x for x in listHowLongToBeatTime if x["name"]== name]
        resMetacriticScore=[x for x in listMetacriticScore if x["name"]== name]

        print()
        print(len(resComplement))
        print(len(resDixGamerPrice))
        print(len(resIkuroGamePrice))
        print(len(resHowLongToBeatTime))
        print(len(resMetacriticScore))
        #imprime 1 por cada lista, porque ya sabemos que estan los 5 datos


        #empieza a armar la data

        n1=resDixGamerPrice[0]["price"]
        n2=resIkuroGamePrice[0]["price"]
        precio=""
        offer=False

        #acomoda los precios, si n1 es negativo es que hay oferta
        if float(n1)<0:
            offer=True

            if float(n1*-1)<float(n2):
                precio = "oferta: $" + str(float(n1* -1)) + "-$" + str(n2)

            elif float(n1*-1)==float(n2):
                precio = "oferta: $" + str(n2)

            else:
                precio = "oferta: $" + str(n2) + "-$" + str(float(n1 * -1))
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
        emit('onNewData', finalData,broadcast=True)  #emite nuevo juego

@app.route('/')
def index():
    return "Hola soy el server principal"

############################################################################################################################################################
# Data para en frontend, se supone que el cliente principal va a armar todo y mandarlo a este endpoint

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
    global dataMetacriticScore
    dataMetacriticScore = request.json
    listMetacriticScore.append(dataMetacriticScore["data"])  #se anade la data obtenida a la lista correspondiente
    return jsonify({"status": "finalizada"})

@app.route('/getMetacritic' , methods=['GET'])  # endpoint que da la data si es que hay
def getMetacritic():
    global tareaMetacriticScoreTerminada,dataMetacriticScore
    if tareaMetacriticScoreTerminada==True:
        return jsonify({"data": dataMetacriticScore})
    else:
        return jsonify({"status": "enProceso"})

@socketio.on('connectMetacriticScore')  #evento que activa el cliente/modulo para conectarse
def connectMetacriticScore(data):
    global tareaMetacriticScoreTerminada
    tareaMetacriticScoreTerminada = False
    emit('onMetacriticScore',data,broadcast=True) #Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finMetacriticScore')  #Evento que usa el cliente/modulo para decir que termino la tarea
def finMetacriticScore(name):
    global tareaMetacriticScoreTerminada,dataMetacriticScore
    tareaMetacriticScoreTerminada = True
    listNames.append(name)  #se termino tarea, agrego nombre
    haveAllData(name)  #verifico si tengo todos los datos para armar la data y actualizar
    #emit('onFinishMetacriticScore',dataMetacriticScore,broadcast=True)
############################################################################################################################################################



############################################################################################################################################################
#DixGamerPrice

@app.route('/setDixGamerPrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setDixGamerPrice():
    global dataDixGamerPrice
    dataDixGamerPrice = request.json
    listDixGamerPrice.append(dataDixGamerPrice["data"]) #se anade la data obtenida a la lista correspondiente
    return jsonify({"status": "finalizada"})

@app.route('/getDixGamerPrice' , methods=['GET'])  # endpoint que da la data si es que hay
def getDixGamerPrice():
    global tareaDixGamerPriceTerminada,dataDixGamerPrice
    if tareaDixGamerPriceTerminada==True:
        return jsonify({"data": dataDixGamerPrice})
    else:
        return jsonify({"data": "enProceso"})

@socketio.on('connectDixGamerPrice')  #evento que activa el cliente/modulo para conectarse
def connectDixGamerPrice(data):
    global tareaDixGamerPriceTerminada
    tareaDixGamerPriceTerminada = False
    emit('onDixGamerPrice',data,broadcast=True) #Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finDixGamerPrice')  #Evento que usa el cliente/modulo para decir que termino la tarea
def finDixGamerPrice(name):
    global tareaDixGamerPriceTerminada,dataDixGamerPrice
    tareaDixGamerPriceTerminada = True
    listNames.append(name)  # se termino tarea, agrego nombre
    haveAllData(name)  # verifico si tengo todos los datos para armar la data y actualizar
    #emit('onFinishDixGamerPrice',dataDixGamerPrice,broadcast=True)

############################################################################################################################################################


############################################################################################################################################################
#IkuroGamePrice

@app.route('/setIkuroGamePrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setIkuroGamePrice():
    global dataIkuroGamePrice
    dataIkuroGamePrice = request.json
    listIkuroGamePrice.append(dataIkuroGamePrice["data"])  #se anade la data obtenida a la lista correspondiente
    return jsonify({"status": "finalizada"})

@app.route('/getIkuroGamePrice' , methods=['GET'])  # endpoint que da la data si es que hay
def getIkuroGamePrice():
    global tareaIkuroGamePriceTerminada,dataIkuroGamePrice
    if tareaIkuroGamePriceTerminada==True:
        return jsonify({"data": dataIkuroGamePrice})
    else:
        return jsonify({"data": "enProceso"})

@socketio.on('connectIkuroGamePrice')  # evento que activa el cliente/modulo para conectarse
def connectIkuroGamePrice(data):
    global tareaIkuroGamePriceTerminada
    tareaIkuroGamePriceTerminada = False
    emit('onIkuroGamePrice', data, broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finIkuroGamePrice')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finIkuroGamePrice(name):
    global tareaIkuroGamePriceTerminada, dataIkuroGamePrice
    tareaIkuroGamePriceTerminada = True
    listNames.append(name)  # se termino tarea, agrego nombre
    haveAllData(name)  # verifico si tengo todos los datos para armar la data y actualizar
    #emit('onFinishIkuroGamePrice',dataIkuroGamePrice,broadcast=True)

############################################################################################################################################################

############################################################################################################################################################
#Complements

@app.route('/setComplements' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setComplements():
    global dataComplements
    dataComplements = request.json
    listComplement.append(dataComplements["data"])  #se anade la data obtenida a la lista correspondiente
    return jsonify({"status": "finalizada"})

@app.route('/getComplements' , methods=['GET'])  # endpoint que da la data si es que hay
def getComplements():
    global tareaComplements,dataComplements
    if tareaComplements==True:
        return jsonify({"data": dataComplements})
    else:
        return jsonify({"data": "enProceso"})

@socketio.on('connectComplements')  # evento que activa el cliente/modulo para conectarse
def connectComplements(data):
    global tareaComplements
    tareaComplements = False
    emit('onComplements', data, broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finComplements')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finComplements(name):
    global tareaComplements, dataComplements
    tareaComplements = True
    listNames.append(name)  # se termino tarea, agrego nombre
    haveAllData(name)  # verifico si tengo todos los datos para armar la data y actualizar
    #emit('onFinishComplements',dataComplements,broadcast=True)

############################################################################################################################################################

############################################################################################################################################################
# HowLongToBeat

#No es necesario el setHowLongToBeatTime porque el cliente esta en python entonces pasa la data como parametro cuando termine

@app.route('/getHowLongToBeatTime' , methods=['GET'])  # endpoint que da la data si es que hay
def getHowLongToBeatTime():
    global tareaHowLongToBeatTimeTerminada, dataHowLongToBeatTime
    if tareaHowLongToBeatTimeTerminada==True:
        return jsonify({"data": dataHowLongToBeatTime})
    else:
        return jsonify({"data": "enProceso"})

@socketio.on('connectHowLongToBeatTime')  # evento que activa el cliente/modulo para conectarse
def connectHowLongToBeatTime(data):
    global tareaHowLongToBeatTimeTerminada
    tareaHowLongToBeatTimeTerminada = False
    emit('onHowLongToBeatTime', data,broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finHowLongToBeatTime')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finHowLongToBeatTime(data):  #trae la data aca, no es necesario el endpoint setHowLongToBeatTime
    global tareaHowLongToBeatTimeTerminada, dataHowLongToBeatTime
    dataHowLongToBeatTime=data["data"]
    tareaHowLongToBeatTimeTerminada = True
    listHowLongToBeatTime.append(dataHowLongToBeatTime)  #se anade la data obtenida a la lista correspondiente
    listNames.append(dataHowLongToBeatTime["name"])  # se termino tarea, agrego nombre
    haveAllData(dataHowLongToBeatTime["name"])    #verifico si tengo todos los datos para armar la data y actualizar
############################################################################################################################################################


if __name__ == '__main__':
    #socketio.run()  #para correrlo en el server
    socketio.run(app, debug=True,port="5000") #para correrlo local