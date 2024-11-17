import redis


cursor = redis.Redis(
    host="localhost",
    port=6379
)

print(cursor.hget("accounts", "123456"))