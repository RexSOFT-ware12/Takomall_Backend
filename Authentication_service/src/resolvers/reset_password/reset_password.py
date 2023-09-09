from prisma import Prisma
from flask import request, jsonify
from Helpers.prisma_connection  import connect_to_prisma
from Helpers.token import generate_reset_token 
import datetime
from email_service.send_mail import send_reset_password_email

prisma = Prisma()

async def reset_password_request(data):
    email = data.get('email')
    global first_name
    if await connect_to_prisma(prisma):
        user = await prisma.user.find_first(where={'email': str(email)})
        if user:
            reset_token = await generate_reset_token()
            await prisma.user.update_many(
                where={'email': str(email)},
                data={
                    'reset_token': reset_token,
                    'reset_token_expiration': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
            )
            send_reset_password_email(email, user.full_name)
            return jsonify({'message': 'Password reset link sent to your email'}), 200
        else:
            return jsonify({'message': 'Email not found'}), 404