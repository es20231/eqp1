from flask import Flask, render_template , url_for


app = Flask(__name__, static_folder='static')


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
    
@app.route('/pictures_add')
def pictures_add():
    return render_template("pictures_add.html")  

@app.route('/perfil')
def perfil():
    return render_template("perfil.html")


if __name__ == '__main__':
    app.run(debug=True)