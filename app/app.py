from flask import Flask
from flask import request
from flask import render_template, render_template_string
import mysql.connector
import hashlib

config = {
  'user': 'crackme',
  'password': 'thisisacrackablepassword_orno?',
  'host': 'db',
  'database': 'app',
  'raise_on_warnings': True
}

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/lista.txt')
def get_list():
    with open('./static/lista.txt') as f:
        lista = f.readlines()
    
    return '<br>'.join(lista)

def get_country_data(cod):
    try:
        db = mysql.connector.connect(**config)
        
        if db.is_connected():
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM city WHERE CountryCode = '{cod}'")
            data = cursor.fetchall()
            return data
    except Error as ex:
        print("Error during connection: {}".format(ex))
    finally:
        if db.is_connected():
            db.close()
            print("Connection closed.")


@app.route('/app', methods=["GET"])
def show_data():
    cod = request.args.get("cod")
    data = get_country_data(cod)
    
    tabla_html = '{% include "meta.html" %}'
    tabla_html += '{% include "header.html" %}'
    tabla_html += '<form action="" method="get">'
    tabla_html += '<label for="cod">Introduce código país: </label>'
    tabla_html += '<input type="text" name="cod" id="cod" maxlength=3 value="{{ request.form[\'cod\'] }}">'
    tabla_html += '<input type="submit" value="submit">'
    tabla_html += '</form>'
    tabla_html += '<table>\n'
    tabla_html += '<tr><th>Codigo</th><th>Nombre</th><th>Poblacion</th></tr>\n'
    for resultado in data:
        tabla_html += f'<tr><td>{resultado[2]}</td><td>{resultado[1]}</td><td>{resultado[4]}</td></tr>\n'
    tabla_html += '</table>'

    return render_template_string(tabla_html)


def valid_login(user, password):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE Name = %s AND Password = %s", (user, hashlib.sha256(password.encode()).hexdigest(), ))
    account = cursor.fetchall()
    return account


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    try:
        db = mysql.connector.connect(**config)
        if db.is_connected():
            error = None
            if request.method == "POST" and "user" in request.form and "pass" in request.form:
                if valid_login(request.form["user"],
                    request.form["pass"]):
                    return r"Felicidades!, aquí tienes la flag (: <br><br>UAM{SQL1_1NT0_SST1_1NT0_RC3_F3l1C1D4D3S!}" if request.form["user"] == "admin" else "Bienvenido!"
            else:
                error = "usuario/contraseña no válidos"
        return render_template("login.html", error=error)
    except Error as ex:
        print("Error during connection: {}".format(ex))
    finally:
        if db.is_connected():
            db.close()
            print("Connection closed.")


@app.route('/5392ac9d2d51895e7b918edc88623607', methods=["GET"])
def flag():
    return render_template_string("""UAM{L3cTur4_D3_U$B_Pc4P!!}""")


if __name__ == '__main__':
    app.run()
