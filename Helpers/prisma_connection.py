import asyncio
from prisma import Prisma

#Declared variables for retrying
MAX_RETRIES = 2
RETRY_DELAY = 3


#Retry function if database is not responding
async def connect_to_prisma(prisma: Prisma) -> bool:
    retry_count = 0  # Initialize retry count to 0
    while retry_count < MAX_RETRIES:  # Loop until retry count reaches the maximum retries
        try:
            if prisma.is_connected():
                await prisma.disconnect()  # Disconnect from Prisma if already connected
            await prisma.connect()  # Connect to Prisma
            return True  # Return True if connection is successful
        except Exception:
            retry_count += 1  # Increment retry count if an exception occurs
            await asyncio.sleep(RETRY_DELAY)  # Wait for a delay before retrying
    return False  # Return False if connection is unsuccessful after maximum retries