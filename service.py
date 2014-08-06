from flask import Flask, jsonify, make_response
from poi import start_poi_fetching_thread, get_cached_poi

app = Flask(__name__)

@app.route('/clever/api/v1.0/poi', methods = ['GET'])
def poi():
    return jsonify(get_cached_poi())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

start_poi_fetching_thread()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

