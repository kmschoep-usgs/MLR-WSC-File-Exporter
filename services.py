
from flask_restplus import Api, Resource

from app import application

api = Api(application,
          title='MLR WSC File Exporter',
          description='Provides a service whose payload is a JSON legacy location object and writes out a MLR legacy output file',
          default='WSC File Export',
          doc='/api')

@api.route('/file_exporter')
class FileExporter(Resource):
    def post(self):
        return 'Not yet implemented', 400