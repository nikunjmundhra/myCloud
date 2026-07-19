from flask import Flask,render_template ,request

app = Flask(__name__)

@app.route("/",methods =["GET","POST"])
def home():
    name = None
    if request.method =="POST":
        name=request.form["name"]
        print(name)
    return render_template("index.html",
                           title ="Home",
                           name=name)

@app.route("/login")
def login():
    return render_template("login.html",title ="Login")

if __name__ == "__main__":
    app.run(debug=True)
