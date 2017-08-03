from flask import Flask, jsonify
from flask_restful import Resource, Api

from aboki import Aboki

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
api = Api(app)


class getCurrentRates(Resource):
    def get(self):
        try:
            abokiInstance = Aboki()
            current_rates = abokiInstance.get_current_rates()
            response = jsonify({
                'current_rates': current_rates
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            return jsonify({
                'error': e
            })

api.add_resource(getCurrentRates, "/api/rates")


if __name__ == "__main__":
    # app.run(debug=True)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()