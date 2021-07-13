from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False
numbers =[]

@app.route('/store', methods=['GET','POST'])
def store():
    content = request.get_json(silent=True)
    #Your code here
    numbers =[]
    result = numbers.append(content['x'])
    return jsonify( result )

@app.route('/retrieve', methods=['GET','POST'])
def retrieve():
    content = request.get_json(silent=True)
    #Your code here
    #JSON object with a single field "function". {'function': 'mean'}
    if content['function']== 'mean':
        result = mean(numbers)
    elif content['function']== 'min':
        result = min(numbers)
    elif content['function']== 'max':
        result = max(numbers)
    else: 
        print('error')
        
    return jsonify( result )

if __name__ == '__main__':
    app.run(port='5002')
