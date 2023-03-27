import hazelcast

if __name__ == "__main__":
    # Start the client and connect to the cluster
    print()
    hz = hazelcast.HazelcastClient()
    # Create a Distributed Map in the cluster
    map = hz.get_map("my-distributed-map1").blocking()
    # Standard Put and Get
    for k in range(1000):
        map.put(k, f"El{k}")

    # Shutdown the client
    hz.shutdown()