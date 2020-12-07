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

@app.route('/')
def index():
    return "Hola soy el server principal"

############################################################################################################################################################
# Data para en frontend, se supone que el cliente principal va a armar todo y mandarlo a este endpoint

@app.route('/setData' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setData():
    global finalData
    finalData = request.json
    print(finalData)
    return jsonify({"status": "ok"})

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
    print(request.sid)
    emit('onMetacriticScore',data,broadcast=True) #Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finMetacriticScore')  #Evento que usa el cliente/modulo para decir que termino la tarea
def finMetacriticScore():
    global tareaMetacriticScoreTerminada,dataMetacriticScore
    tareaMetacriticScoreTerminada = True
    emit('onFinishMetacriticScore',dataMetacriticScore,broadcast=True)

############################################################################################################################################################



############################################################################################################################################################
#DixGamerPrice

@app.route('/setDixGamerPrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setDixGamerPrice():
    global dataDixGamerPrice
    dataDixGamerPrice = request.json
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
    print(request.sid)
    emit('onDixGamerPrice',data,broadcast=True) #Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finDixGamerPrice')  #Evento que usa el cliente/modulo para decir que termino la tarea
def finDixGamerPrice():
    global tareaDixGamerPriceTerminada,dataDixGamerPrice
    tareaDixGamerPriceTerminada = True
    emit('onFinishDixGamerPrice',dataDixGamerPrice,broadcast=True)

############################################################################################################################################################


############################################################################################################################################################
#IkuroGamePrice

@app.route('/setIkuroGamePrice' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setIkuroGamePrice():
    global dataIkuroGamePrice
    dataIkuroGamePrice = request.json
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
    print(request.sid)
    emit('onIkuroGamePrice', data, broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finIkuroGamePrice')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finIkuroGamePrice():
    global tareaIkuroGamePriceTerminada, dataIkuroGamePrice
    tareaIkuroGamePriceTerminada = True
    emit('onFinishIkuroGamePrice',dataIkuroGamePrice,broadcast=True)

############################################################################################################################################################

############################################################################################################################################################
#Complements

@app.route('/setComplements' , methods=['POST'])  #endpoint que recibe la data de el app de c#
def setComplements():
    global dataComplements
    dataComplements = request.json
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
    print(request.sid)
    emit('onComplements', data, broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finComplements')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finComplements():
    global tareaComplements, dataComplements
    tareaComplements = True
    emit('onFinishComplements',dataComplements,broadcast=True)

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
    print(request.sid)
    emit('onHowLongToBeatTime', data,broadcast=True)  # Activa el evento para que el cliente/modulo haga la tarea
    # broadcast es para que emita a todos, porque si no solo emite al ultmimo que conecto

@socketio.on('finHowLongToBeatTime')  # Evento que usa el cliente/modulo para decir que termino la tarea
def finHowLongToBeatTime(data):  #trae la data aca, no es necesario el endpoint setHowLongToBeatTime
    global tareaHowLongToBeatTimeTerminada, dataHowLongToBeatTime
    dataHowLongToBeatTime=data
    tareaHowLongToBeatTimeTerminada = True
    emit('onFinishHowLongToBeatTime',dataHowLongToBeatTime,broadcast=True)
############################################################################################################################################################


if __name__ == '__main__':
    #socketio.run()  #para correrlo en el server
    socketio.run(app, debug=True,port="5000") #para correrlo local