from prisma import Prisma
from flask import request, jsonify
from Helpers.prisma_connection  import connect_to_prisma 
import datetime
from Helpers.hash_password import hash_password
prisma = Prisma()


async def reset_link(data , reset_token):
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
            return jsonify({'message': 'Password reset successfully'}), 200
        else:
            return jsonify({'message': 'Invalid or expired reset token'}), 400