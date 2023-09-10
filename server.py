from flask import Flask, request, jsonify
from src.resolvers.sign_up.sign_up import signup
from src.resolvers.login.login import login
from src.resolvers.reset_password.reset_password import reset_password_request
from src.resolvers.reset_password.reset_link import reset_link
from Helpers.prisma_connection  import connect_to_prisma
from prisma import Prisma
import datetime
from Helpers.verify_password import verify_password
from Helpers.hash_password import hash_password
from Helpers.token import generate_reset_token
from email_service.send_mail import send_reset_password_email
prisma = Prisma()
app = Flask(__name__)
    
@app.route('/signup', methods=['POST'])
async def signup_route():
    data = request.get_json()
    if await connect_to_prisma(prisma):
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        hashed_password = await hash_password(password)

        if await prisma.user.find_first(where={'email': email}):
            return jsonify({'message': 'Email is already registered', 'status': 401})

        new_user = await prisma.user.create(
            {'full_name': full_name, 
             'email': email, 
             'password': hashed_password,
             }
            )
        if new_user:
            return jsonify({'message': 'User created successfully', 'status': 201 })

@app.route('/login', methods=['POST'])
async def login_route():
    data = request.get_json()
    if await connect_to_prisma(prisma):
        email = data.get('email')
        password = data.get('password')

        user = await prisma.user.find_first(where={'email': email})
        if user and await verify_password(password, user.password):
            return jsonify({'message': 'Login successful', 'status': 200})
        else:
            return jsonify({'message': 'Invalid credentials', 'status': 401})
    


@app.route('/reset_password', methods=['POST'])
async def reset_route():
    data = request.get_json()
    email = data.get('email')
    if await connect_to_prisma(prisma):
        user = await prisma.user.find_first(where={'email': str(email)})
        if user:
            reset_token = await generate_reset_token()
            check_user = await prisma.user.update_many(
                where={'email': str(email)},
                data={
                    'reset_token': reset_token,
                    'reset_token_expiration': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
            )
            if check_user:
                send_reset_password_email(email, user.full_name)
            return jsonify({'message': 'Password reset link sent to your email', 'status': 200})
        else:
            return jsonify({'message': 'Email not found', 'status': 404 })


@app.route('/reset_password/<reset_token>', methods=['POST'])
async def reset_route_link(reset_token):
    data = request.get_json()
    new_password = data.get('password')

    if await connect_to_prisma(prisma):
        user = await prisma.user.find_first(where={'reset_token': reset_token})
        
        if user and user.reset_token_expiration > datetime.datetime.utcnow():
            hashed_password = await hash_password(new_password)
            await prisma.user.update_many(
                where={
                    'reset_token':   None,
                    'reset_token_expiration':   None,
                    'password': hashed_password
                }
            )
            return jsonify({'message': 'Password reset successfully', 'status': 200})
        else:
            return jsonify({'message': 'Invalid or expired reset token', 'status': 400 })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
