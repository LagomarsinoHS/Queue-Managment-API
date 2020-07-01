from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Queue
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
# os me permite conseguir lo que defini dentro de .env
app.config['DEBUG'] = os.environ.get("DEBUG")
app.config['ENV'] = os.environ.get("ENV")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLDATABASE")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database'
##app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://humberto:humberto@localhost:3306/BD_Local'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)
queue = Queue()

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/new", methods=["POST"])
def new_item():
    valorInput = request.json.get("valor", None)
    if valorInput == "" or valorInput ==None:
        return jsonify({"Msg": "Debe ingresar dato"})

    queue._queue.append(valorInput)
    queue.enqueue(valorInput)
    return jsonify({"Msg": f"Valor ingresado correctamente, faltan {queue.size()-1} y serás atendido!"})

@app.route("/next", methods=["GET"])
def next_item():
    queue.dequeue()
    if(queue.size()>0):
        return jsonify({"Msg": f"Procesado, {queue.size()} elementos restantes"})
    else:
        return jsonify({"Msg": f"Procesado, No hay elementos restantes"})

@app.route("/all", methods=["GET"])
def all_items():
    return jsonify({"Msg": queue._queue})

if (__name__) == "__main__":
    manager.run()
