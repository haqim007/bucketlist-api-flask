from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import json, request, jsonify, abort
from functools import wraps
import jwt
import datetime

# local import
from instance.config import app_config

# init sql-alchemy
db = SQLAlchemy()

"""
The create_app function wraps the creation of a new Flask object, and returns it 
after it's loaded up with configuration settings using app.config and connected 
to the DB using db.init_app(app).
"""



def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # def check_for_token(func):
    #     @wraps(func)
    #     def wrapped(*args, **kwargs):
    #         token = request.args.get("token")
    #         if not token:
    #             return jsonify({'message': 'Missing Token'}), 403
            
    #         try:
    #             data = jwt.decode(token, app.config["SECRET_KEY"])
    #         except: 
    #             return jsonify({'message': 'Invalid Token'}), 403

    #         return func(*args, **kwargs)
    #     return wrapped


    from models.models import BucketList

    # @app.route("/login", methods=["POST"])
    # def login():
    #     username = str(request.data.get("username"))
    #     password = str(request.data.get("password"))
    #     if username and password:
    #         token = jwt.encode({
    #             'user': username,
    #             'exp' : datetime.datetime.now() + datetime.timedelta(seconds=60)
    #             },
    #             app.config['SECRET_KEY']
    #         )
    #         return jsonify({"token": token})
    #     else:
    #         return jsonify({"message": "unable to verify"}), 403
    
    @app.route("/bucketlist", methods=["POST", "GET"])
    # @check_for_token
    def bucketlist():
        if request.method == "POST":
            name = str(request.data.get("name"))
            if name:
                bucketlist = BucketList(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name':bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified':bucketlist.date_modified
                })

                response.status_code = 201
                return response

        else:
            # GET
            bucketlists = BucketList.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name':bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified':bucketlist.date_modified
                }
                results.append(obj)

            response = jsonify(results)
            response.status_code = 200

            return response

    @app.route('/bucketlist/<int:id>', methods=[ "GET", "PUT", "DELETE"])
    def bucketlist_manipulation(id, **kwargs):
        
        bucketlist = BucketList.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                "message": f"bucketlist {bucketlist.id} deleted successfully"
            }, 200
        
        elif request.method == "PUT":

            new_name = str(request.data.get("name", ""))
            bucketlist.name = new_name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name':bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified':bucketlist.date_modified
            })
            response.status_code = 200
            return response

        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name':bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified':bucketlist.date_modified
            })
            response.status_code = 200
            return response





    return app
