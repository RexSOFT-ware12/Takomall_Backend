from flask import Flask, request, jsonify
from src.resolvers.sign_up.sign_up import signup
from src.resolvers.login.login import login
from src.resolvers.reset_password.reset_password import reset_password_request
from src.resolvers.reset_password.reset_link import reset_link
from Helpers.prisma_connection   import connect_to_prisma
from prisma import Prisma
from Helpers.verify_password import verify_password
from flask_cors import CORS

app = Flask(__name__)

prisma = Prisma()
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
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Debugging: Print the received data
        print("Received data:", data)
        
        response, status_code = await signup(data)
        return response, status_code
    except Exception as e:
        # Debugging: Print the exception
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
async def login_route():
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Debugging: Print the received data
        print("Received data:", data)
        if await connect_to_prisma(prisma):
            email = data.get('email')
            password = data.get('password')

            user = await prisma.user.find_first(where={'email': email})
            print("User:", user)
            if user and await verify_password(password, user.password):
                return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        # Handle exceptions that occur outside of the try block
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/reset_password', methods=['POST'])
async def reset_route():
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Debugging: Print the received data
        print("Received data:", data)

        response, status_code = await reset_password_request(data)
        return response, status_code
    except Exception as e:
        # Debugging: Print the exception
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/reset_password/<reset_token>', methods=['POST'])
async def reset_route_link(reset_token):
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'error': 'Invalid Content-Type, must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Debugging: Print the received data
        print("Received data:", data)

        response, status_code = await reset_link(data, reset_token)
        return response, status_code
    except Exception as e:
        # Debugging: Print the exception
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
