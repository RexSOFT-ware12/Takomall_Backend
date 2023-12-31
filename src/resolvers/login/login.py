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
        if user and await verify_password(password, user.password):
            return {'message': 'Login successful', 'user_id': user.id}
        else:
            return {'message': 'Invalid credentials'}
