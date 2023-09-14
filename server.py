from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import asyncio
from src.resolvers.sign_up.sign_up import signup
from src.resolvers.login.login import login
from src.resolvers.reset_password.reset_password import reset_password_request
from src.resolvers.reset_password.reset_link import reset_link

app = Flask(__name__)
api = Api(app)

async def async_signup(data):
    with app.app_context():
        return await signup(data)

async def async_login(data):
    with app.app_context():
        return await login(data)

async def async_reset_password_request(data):
    with app.app_context():
        return await reset_password_request(data)

async def async_reset_link(data, reset_token):
    with app.app_context():
        return await reset_link(data, reset_token)

# async def business_account(data, reset_token):
#     with app.app_context():
#         return await create_business_account(data, reset_token)

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(asyncio.run(async_signup(data)))

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(asyncio.run(async_login(data)))
            

class ResetPasswordResource(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(asyncio.run(async_reset_password_request(data)))

class ResetLinkResource(Resource):
    def post(self, reset_token):
        data = request.get_json()
        return jsonify(asyncio.run(async_reset_link(data, reset_token)))

# Add resources to the API with their respective routes
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(ResetPasswordResource, '/reset_password')
api.add_resource(ResetLinkResource, '/reset_password/<reset_token>')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
