from flask import Flask, flash

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def test():
    print("Hello")
    return 0

if(__name__ == "__main__"):
    app.debug = True
    app.run()