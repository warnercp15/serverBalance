from socketIO_client import SocketIO
import requests
import json

listaJuegos=["uncharted the nathan drake collection", "final fantasy vii remake", "sekiro shadows die twice", "devil may cry 5",
             "the evil within 2", "borderlands 3", "cuphead", "doom eternal", "fallout 76", "fifa 21", "payday 2 crimewave edition",
             "middle earth shadow of mordor", "ark survival evolved", "red dead redemption 2", "ghost of tsushima",
             "tomb raider definitive edition", "need for speed payback", "resident evil 0 hd", "lego marvel super heroes",
             "batman arkham knight", "lego marvel avengers", "lego harry potter collection", "street fighter v", "until dawn",
             "bloodborne", "heavy rain", "dying light", "dishonored 2", "just cause 4", "ufc 3", "doom", "days gone",
             "resident evil 5", "resident evil hd", "mad max", "dirt 4", "tekken 7", "lego worlds", "mortal kombat x",
             "battlefield 4"]

def newData(data):
    print(data)

print('Iniciando eventos')
# socketIO = SocketIO("http://localhost",5000) #se conecta al server
socketIO = SocketIO('http://invokeee.pythonanywhere.com') #se conecta al server

socketIO.on('onNewData', newData)  # define que hacer cuando se actice el evento

for game in listaJuegos:
    socketIO.emit('connectIkuroGamePrice', game)  # activa el evento y le manda el primer juego de la lista
    socketIO.emit('connectDixGamerPrice', game)  # activa el evento y le manda el primer juego de la lista
    socketIO.emit('connectMetacriticScore', game)  # activa el evento y le manda el primer juego de la lista
    socketIO.emit('connectComplements',game)  # activa el evento y le manda el primer juego de la lista
    socketIO.emit('connectHowLongToBeatTime', game)  # activa el evento y le manda el primer juego de la lista
socketIO.wait()
