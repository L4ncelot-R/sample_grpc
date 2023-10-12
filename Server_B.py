import Server
import threading

if __name__ == '__main__':
    server = Server.Server("127.0.0.1", "50052")

    subscription = server.get_subscription("Topic A")

    server_thread = threading.Thread(target=server.run)
    subscribe_thread = threading.Thread(target=server.send_subscribe, args=(subscription, "127.0.0.1", "50053"))

    server_thread.start()
    subscribe_thread.start()

    server_thread.join()
    subscribe_thread.join()
