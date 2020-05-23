import redis
import time

client = redis.Redis('localhost')

cart_session = 'user_1'
items = {'item1': 'x', 'item2': 'y'}

client.hmset(cart_session, items)
client.expire(cart_session, 2)
print('before', client.hgetall(cart_session))
time.sleep(3)
print('after', client.hgetall(cart_session))
