
from flask import request, jsonify
from prisma import Prisma
from Helpers.prisma_connection   import connect_to_prisma
from Helpers.hash_password import hash_password



# Initialize the Prisma client
prisma = Prisma()
async def signup(data):
    if await connect_to_prisma(prisma):
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        # Hash the password
        hashed_password = await hash_password(password)

        if await prisma.user.find_first(where={'email': email}):
            return {'message': 'Email is already registered'}

        new_user = await prisma.user.create(
            {'full_name': full_name, 
             'email': email, 
             'password': hashed_password,
             }
            )

        return {'message': 'User created successfully', 'user_id': new_user.id}