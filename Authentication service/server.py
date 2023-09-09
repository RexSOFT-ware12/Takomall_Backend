from flask import Flask, request, jsonify
from src.resolvers.sign_up.sign_up import signup
from src.resolvers.login.login import login
import asyncio
from src.resolvers.reset_password.reset_password import reset_password_request
from src.resolvers.reset_password.reset_link import reset_link
app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    print('Hello')
    
@app.route('/signup', methods=['POST'])
async def signup_route():
    data = request.get_json()
    response, status_code = await signup(data)
    return response, status_code  

@app.route('/login', methods=['POST'])
async def login_route():
    data = request.get_json()
    response, status_code = await login(data)
    return response, status_code  


@app.route('/reset_password', methods=['POST'])
async def reset_route():
    data = request.get_json()
    response, status_code = await reset_password_request(data)
    return response, status_code 


@app.route('/reset_password/<reset_token>', methods=['POST'])
async def reset_route_link(reset_token):
    data = request.get_json()
    response, status_code = await reset_link(data, reset_token)
    return response, status_code 

if __name__ == '__main__':
    app.run(debug=True)
