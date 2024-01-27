# app.py
from flask import Flask,jsonify,request 
from flask_cors import CORS
from generate_routes import GenerateRoutes

app = Flask(__name__)
CORS(app)



# /get/49.2317256/-122.8927259/200/100/1
# @app.route('/get/<lat>/<lon>/<dist>/<marginErr>', methods=['GET'])
@app.route('/get/<lat>/<lon>/<dist>/<marginErr>/<numberOfRoutes>', methods=['GET'])
def getRoutes(lat, lon, dist, marginErr, numberOfRoutes=5):
    # Example with a set
    # print(type(lat), type(lon), type(dist), type(marginErr), type(numberOfRoutes))
    
    # print()
    obj = GenerateRoutes(xCoord=float(lon), yCoord=float(lat), targetDistance=float(dist), marginOfErrorDist=float(marginErr))
    finalRoutes = obj.getFinalRoutes(numberOfRoutes=int(numberOfRoutes))

    return(jsonify(finalRoutes))

@app.route('/lab/<username>')
def bye(username):
    return f"{username}"

if __name__ == "__main__":
    app.run()