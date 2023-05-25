from flask import Flask, render_template, redirect, request, url_for, abort
app = Flask(__name__)	
import json
import requests
import os

url_base = "https://api.sportradar.com/formula1/trial/v2/en/sport_events/sr:stage:1031763/summary.json?api_key="
key = "fjupxcztqnk9wbpby58r9vk9"


@app.route('/',methods=["GET","POST"])
def inicio():
    return render_template("inicio.html")
    

@app.route('/pilotos', methods=['GET', 'POST'])
def pilotos():
    if request.method == 'POST':
        nombre = request.form.get('busqueda','')
        payload = {'key':key}
        r = requests.get(url_base + key)
        if r.status_code == 200:
            doc = r.json()
            lista = doc["stage"]["competitors"]
            pilotos_encontrados = buscar_piloto(lista, nombre)
            return render_template("pilotos.html", lista = pilotos_encontrados)
        else:
            abort(404)
    else:
        payload = {'key':key}
        r = requests.get(url_base + key)
        if r.status_code == 200:
            doc = r.json()
            return render_template("pilotos.html", lista = doc["stage"]["competitors"])
        else:
            abort(404)

def buscar_piloto(lista, nombre):
    pilotos_encontrados=[]
    for piloto in lista:
        print(piloto)
        print(piloto["name"])
        if str(nombre).lower() in str(piloto["name"]).lower():
            pilotos_encontrados.append(piloto)
            return pilotos_encontrados
        

@app.route('/piloto/<string:id>',methods=["GET"])
def piloto(id):
    payload = {'key':key}
    r = requests.get(url_base + key)
    if r.status_code == 200:
        doc = r.json()
        lista = doc["stage"]["competitors"]
        for i in lista:
            if i["id"] == id:
                return render_template('piloto.html',piloto=i)
    else:
        abort(404)


app.run("0.0.0.0",5000,debug=True)