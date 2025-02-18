from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')  #Com2
    
@app.route('/contact/')
def contact():
    return render_template('contact.html')
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme.html')
@app.route('/commits/')
def commits():
    # Récupérer les commits de GitHub via l'API
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits_data = response.json()

    # Dictionnaire pour stocker la quantité de commits par minute
    commit_minutes = {}

    # Extraire la minute de chaque commit
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        minute = extract_minutes(date_string)
        
        if minute not in commit_minutes:
            commit_minutes[minute] = 1
        else:
            commit_minutes[minute] += 1

    # Convertir les données en format utilisable par Google Charts
    results = [{'minute': minute, 'commits': count} for minute, count in commit_minutes.items()]
    
    # Retourner les données sous forme de JSON
    return jsonify(results=results)

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    # Convertir la date en objet datetime
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    # Extraire la minute de l'heure
    minutes = date_object.minute
    return minutes

if __name__ == "__main__":
    app.run(debug=True)
