import secrets

async def generate_reset_token():
    return secrets.token_urlsafe(32)