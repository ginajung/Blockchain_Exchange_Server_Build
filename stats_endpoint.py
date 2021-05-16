from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/store', methods=['GET','POST'])
def store():
    content = request.get_json(silent=True)
    #Your code here
    result = content
    return jsonify( result )

@app.route('/retrieve', methods=['GET','POST'])
def retrieve():
    content = request.get_json(silent=True)
    #Your code here
    result = content
    return jsonify( result )

if __name__ == '__main__':
    app.run(port='5002')
