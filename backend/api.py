from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask_restful import reqparse
from engine import search, get_youtube_messages

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

youtube_comments_parser = reqparse.RequestParser()
youtube_comments_parser.add_argument('link', required=True)
youtube_comments_parser.add_argument('start_time', type=int, help='An integer value is required.')
youtube_comments_parser.add_argument('end_time', type=int, help='An integer value is required.')

parser = reqparse.RequestParser()
parser.add_argument('link', required=True)
parser.add_argument('search_terms', required=True)
parser.add_argument('analysis_interval', required=True, type=int, help='An integer value is required.')
parser.add_argument('start_time', type=int, help='An integer value is required.')
parser.add_argument('end_time', type=int, help='An integer value is required.')

class YoutubeComments(Resource):
    def post(self):
        args = youtube_comments_parser.parse_args()
        link = args['link']
        start_time = args['start_time']
        end_time = args['end_time']
        results = {}

        try:
            results = get_youtube_messages(link, start_time, end_time)
        except Exception as e:
            return {'message': str(e)}, 422

        return results

class YoutubeAnalyzer(Resource):
    def get(self):
        args = parser.parse_args()
        link = args['link']
        search_terms = args['search_terms']
        analysis_interval = args['analysis_interval']
        start_time = args['start_time']
        end_time = args['end_time']
        return {
            'api_status': 'ready',
            'link': link,
            'search_terms': search_terms,
            'analysis_interval': analysis_interval,
            'start_time': start_time,
            'end_time': end_time
        }

    def post(self):
        args = parser.parse_args()
        link = args['link']
        search_terms = args['search_terms']
        analysis_interval = args['analysis_interval']
        start_time = args['start_time']
        end_time = args['end_time']
        results = {}

        # results = search(link, search_terms, analysis_interval, start_time, end_time)

        try:
            results = search(link, search_terms, analysis_interval, start_time, end_time)
        except Exception as e:
            return {'message': str(e)}, 422

        return results

api.add_resource(YoutubeAnalyzer, '/')
api.add_resource(YoutubeComments, '/comments')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')