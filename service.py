from flask import Flask, jsonify, make_response
from poi import get_cached_poi, update_poi, initialize

app = Flask(__name__)

@app.route('/clever/api/v1.0/poi', methods = ['GET'])
def poi():
    return jsonify(get_cached_poi())

@app.route('/clever/api/v1.0/refresh', methods = ['GET'])
def refresh():
    return jsonify(update_poi())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

initialize()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

