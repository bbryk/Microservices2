
import hazelcast
import threading

hz = hazelcast.HazelcastClient()
map = hz.get_map("my-distributed-map").blocking()
key = "1"


def default():
    value = map.get(key)
    value += 1
    map.put(key, value)


def pessimistic():
    map.lock(key)
    try:
        value = map.get(key)
        value += 1
        map.put(key, value)
    finally:
        map.unlock(key)


def optimistic():
    while True:
        value = map.get(key)
        if(map.replace_if_same(key, value, value + 1)):
            break

iter_num = 100

map.put(key, 0)
threads = [threading.Thread(target=default) for i in range(iter_num)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Default: The value is {map.get(key)} after 100 iterations")

map.put(key, 0)

threads = [threading.Thread(target=pessimistic) for i in range(iter_num)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Pessimistic: The value is {map.get(key)} after 100 iterations")

map.put(key, 0)

threads = [threading.Thread(target=optimistic) for i in range(iter_num)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(f"Optimistic: The value is {map.get(key)} after 100 iterations")

hz.shutdown()
