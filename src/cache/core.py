from redis import Redis

current_connection = Redis(host="host.docker.internal", port=6379)

