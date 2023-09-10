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

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        response, status_code = asyncio.run(async_signup(data))
        if status_code == 200:
            return {"message": "SignUp successful"}
        else:
            return {"error": "Invalid credentials"}

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        response, status_code = asyncio.run(async_login(data))
        if status_code == 200 or status_code == 201:
            return {"message":"Login successful"}
        else:
            return {"error": "Invalid credentials"}
            

class ResetPasswordResource(Resource):
    def post(self):
        data = request.get_json()
        response, status_code = asyncio.run(async_reset_password_request(data))
        if status_code == 200:
            return {"message": "Reset link sent"}
        else:
            return {"error": "Invalid credential"}

class ResetLinkResource(Resource):
    def post(self, reset_token):
        data = request.get_json()
        response, status_code = asyncio.run(async_reset_link(data, reset_token))
        if status_code == 200:
            return {"message": "Password changed successful"}
        else:
            return {"error": "Invalid credentials"}

# Add resources to the API with their respective routes
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(ResetPasswordResource, '/reset_password')
api.add_resource(ResetLinkResource, '/reset_password/<reset_token>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
