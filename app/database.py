from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://Yauheni:8!*bD2ZeENpYSmb@authservicedb.mii9n.mongodb.net/"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.auth_service_db
users = database.users
admin_password = database.admin_password
