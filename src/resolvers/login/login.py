import bcrypt
from prisma import Prisma
from flask import jsonify
from Helpers.prisma_connection import connect_to_prisma
from Helpers.verify_password import verify_password

prisma = Prisma()


async def login(data):
    if await connect_to_prisma(prisma):
        email = data.get('email')
        password = data.get('password')

        user = await prisma.user.find_first(where={'email': email})
        print("User:", user)
        if user and await verify_password(password, user.password):
            return {'message': 'Login successful', 'user_id': user.id}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
