# app.py
from flask import Flask,jsonify,request 
from flask_cors import CORS
from generate_routes import GenerateRoutes

app = Flask(__name__)
CORS(app)


@app.route('/get/<lat>/<lon>/<dist>/<marginErr>', methods=['GET'])
def getRoutes(lat, lon, dist, marginErr):
    # Example with a set
    print(type(lat), type(lon), type(dist), type(marginErr))
    
    # print()
    obj = GenerateRoutes(float(lon), float(lat), float(dist), float(marginErr))
    print(obj.getFinalRoutes(5))

    return(jsonify(lat, lon))

@app.route('/lab/<username>')
def bye(username):
    return f"{username}"

if __name__ == "__main__":
    app.run()