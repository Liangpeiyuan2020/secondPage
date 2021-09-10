import os,demo

from flask import Flask
app = Flask(__name__)

@app.route('/<id>')
def hello_world(id):
    try:
        sttr=demo.main2(id)
        return sttr
    except Exception as e:
        saa=str(e)
        saa=saa+"error!"
        return saa


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
