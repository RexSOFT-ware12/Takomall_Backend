from flask import Flask, request, jsonify
from src.resolvers.sign_up.sign_up import signup
from src.resolvers.login.login import login
from src.resolvers.reset_password.reset_password import reset_password_request
from src.resolvers.reset_password.reset_link import reset_link
from flask_cors import CORS

app = Flask(__name__)

# Define CORS settings for production and development environments
# Adjust the allowed origins accordingly
CORS(
    app,
    origins=['https://takomall-backend.onrender.com'], 
    supports_credentials=True,
    allow_headers=['Authorization']
)

@app.route('/', methods=['POST'])
def home():
    return 'Hello'

@app.route('/signup', methods=['POST'])
async def signup_route():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400
        
        response, status_code = await signup(data)
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
async def login_route():
    # try:
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400
    
    response, status_code = await login(data)
    return response, status_code
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

@app.route('/reset_password', methods=['POST'])
async def reset_route():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400
        
        response, status_code = await reset_password_request(data)
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset_password/<reset_token>', methods=['POST'])
async def reset_route_link(reset_token):
    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400
        
        response, status_code = await reset_link(data, reset_token)
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

