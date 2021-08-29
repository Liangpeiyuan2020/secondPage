import os,demo

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<id>')
def hello_world(id):
    try:
        sttr=demo.main(id)
        sttr=str(sttr)
        return sttr
    except Exception as e:
        aa=str(e)
        aa=aa+"error"
        return aa

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
