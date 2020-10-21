from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @property
    def serialize(self):
       return {
           'id': self.id,
           'username': self.username,
           'email': self.email,
           'role': self.role,
           'name': self.name,
           'password': self.password
       }

    def __repr__(self):
        return '<User %r>' % self.username

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(80), unique=True, nullable=False)
    douban_id = db.Column(db.String(10), unique=True)
    director = db.Column(db.String(50))
    lead_actors = db.Column(db.String(150))
    movie_type = db.Column(db.String(50))

    @property
    def serialize(self):
       return {
           'id': self.id,
           'movie_name': self.movie_name,
           'douban_id': self.douban_id,
           'director': self.director,
           'lead_actors': self.lead_actors,
           'movie_type': self.movie_type
       }

    def __repr__(self):
        return '<Movie %r>' % self.movie_name

class UserMovieInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'),
        nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(350))
    watch_status = db.Column(db.Boolean)

    @property
    def serialize(self):
       return {
           'id': self.id,
           'user_id': self.user_id,
           'movie_id': self.movie_id,
           'rank': self.rank,
           'tag': self.tag,
           'watch_status': self.watch_status
       }

def abort_if_user_doesnt_exist(user_id):
    users = [str(i.id) for i in User.query.all()]
    if user_id not in users:
        abort(404, message="User {} doesn't exist".format(user_id))

def abort_if_movie_doesnt_exist(movie_id):
    movies = [str(i.id) for i in Movie.query.all()]
    if movie_id not in movies:
        abort(404, message="Movie {} doesn't exist".format(movie_id))

def abort_if_movie_info_doesnt_exist(movie_id, user_id):
    movie_infos = [(str(i.movie_id), str(i.user_id)) for i in UserMovieInfo.query.all()]
    if (movie_id, user_id) not in movie_infos:
        abort(404, message="UserMovieInfo {},{} doesn't exist".format(user_id, movie_id))

class UserListAPI(Resource):
    def get(self):
        users=[i.serialize for i in User.query.all()]
        return users, 200, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'],
         role=args['role'], name=args['name'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        getted_user = User.query.filter_by(username=args['username']).first()
        return getted_user.serialize, 201, {'Access-Control-Allow-Origin': '*'}

class UserAPI(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        getted_user = User.query.filter_by(id=user_id).first()
        return getted_user.serialize, 200, {'Access-Control-Allow-Origin': '*'}

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        getted_user = User.query.filter_by(id=user_id).first()
        db.session.delete(getted_user)
        db.session.commit()
        return '', 204, {'Access-Control-Allow-Origin': '*'}

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('role')
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()
        update_dict = {k:v for k,v in args.items() if v}
        getted_user = User.query.filter_by(id=user_id).update(update_dict)
        db.session.commit()
        return User.query.filter_by(id=user_id).first().serialize, 201, {'Access-Control-Allow-Origin': '*'}

class MovieListAPI(Resource):
    def get(self):
        return [i.serialize for i in Movie.query.all()]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('movie_name', required=True)
        parser.add_argument('douban_id')
        parser.add_argument('director')
        parser.add_argument('lead_actors')
        parser.add_argument('movie_type')
        args = parser.parse_args()
        movie = Movie(movie_name=args['movie_name'], douban_id=args['douban_id'],
         director=args['director'], lead_actors=args['lead_actors'], movie_type=args['movie_type'])
        db.session.add(movie)
        db.session.commit()
        getted_movie = Movie.query.filter_by(movie_name=args['movie_name']).first()
        return getted_movie.serialize, 201, {'Access-Control-Allow-Origin': '*'}

class UserMovieInfoAPI(Resource):
    def get(self, movie_id, user_id):
        abort_if_movie_info_doesnt_exist(movie_id, user_id)
        movie_info = UserMovieInfo.query.filter_by(movie_id=movie_id, user_id=user_id).first()
        return movie_info.serialize, 200, {'Access-Control-Allow-Origin': '*'}

    def post(self, movie_id, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rank')
        parser.add_argument('tag')
        parser.add_argument('watch_status')
        args = parser.parse_args()
        args['watch_status'] = True if args['watch_status'] == 'true' else False
        getted_movie_info = UserMovieInfo.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if (getted_movie_info):
            return '', 200, {'Access-Control-Allow-Origin': '*'}
        movie_info = UserMovieInfo(movie_id=movie_id, user_id=user_id,
         rank=args['rank'], tag=args['tag'], watch_status=args['watch_status'])
        db.session.add(movie_info)
        db.session.commit()
        getted_movie_info = UserMovieInfo.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        return getted_movie_info.serialize, 201, {'Access-Control-Allow-Origin': '*'}

    def put(self, movie_id, user_id):
        abort_if_movie_info_doesnt_exist(movie_id, user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('rank')
        parser.add_argument('tag')
        parser.add_argument('watch_status')
        args = parser.parse_args()
        getted_movie_info = UserMovieInfo.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if args['rank']:
            getted_movie_info.rank = args['rank']
        if args['tag']:
            getted_movie_info.tag = args['tag']
        if args['watch_status']:
            watch_status = True if args['watch_status'] == 'true' else False
            getted_movie_info.watch_status = watch_status
        db.session.commit()
        return getted_movie_info.serialize, 201, {'Access-Control-Allow-Origin': '*'}

class MovieAPI(Resource):
    def get(self, movie_id):
        abort_if_movie_doesnt_exist(movie_id)
        getted_movie = Movie.query.filter_by(id=movie_id).first()
        return getted_movie.serialize

    def delete(self, movie_id):
        abort_if_movie_doesnt_exist(movie_id)
        getted_movie = Movie.query.filter_by(id=movie_id).first()
        db.session.delete(getted_movie)
        db.session.commit()
        return '', 204, {'Access-Control-Allow-Origin': '*'}

    def put(self, movie_id):
        parser = reqparse.RequestParser()
        parser.add_argument('movie_name')
        parser.add_argument('douban_id')
        parser.add_argument('director')
        parser.add_argument('lead_actors')
        parser.add_argument('movie_type')
        args = parser.parse_args()
        update_dict = {k:v for k,v in args.items() if v}
        getted_user = Movie.query.filter_by(id=movie_id).update(update_dict)
        db.session.commit()
        return Movie.query.filter_by(id=movie_id).first().serialize, 201, {'Access-Control-Allow-Origin': '*'}

class MovieSearchAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('movie_name')
        parser.add_argument('user_id')
        parser.add_argument('rank')
        parser.add_argument('tag')
        parser.add_argument('watch_status')
        args = parser.parse_args()
        movies = Movie.query.all()
        if args['movie_name']:
            movies = [movie for movie in movies if movie.movie_name == args['movie_name']]
        if args['user_id']:
            movies_info = UserMovieInfo.query.all()
            movie_info = [info for info in movies_info if str(info.user_id) == args['user_id']]
            if args['rank']:
                movies = [movie for movie in movies if movie.id == movie_info[0].movie_id and args['rank'] == str(movie_info[0].rank)]
            if args['tag']:
                movies = [movie for movie in movies if movie.id == movie_info[0].movie_id and args['tag'] in movie_info[0].tag]
            if args['watch_status']:
                watch_status = True if args['watch_status'] == 'true' else False
                movies = [movie for movie in movies if movie.id == movie_info[0].movie_id and watch_status == movie_info[0].watch_status]
        return [movie.serialize for movie in movies], 200, {'Access-Control-Allow-Origin': '*'}

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user.password == args['password']:
            return {'login_status': 'success'}, 200
        return {'login_status': 'failed'}, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(UserListAPI, '/users')
api.add_resource(UserAPI, '/users/<user_id>')
api.add_resource(UserMovieInfoAPI, '/moviesInfo/<movie_id>/<user_id>')
api.add_resource(MovieListAPI, '/movies')
api.add_resource(MovieAPI, '/movies/<movie_id>')
api.add_resource(MovieSearchAPI, '/movies/search')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
