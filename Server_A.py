import Server
import threading

if __name__ == '__main__':
    server = Server.Server("127.0.0.1", "50051")

    server.address_book = {
        "Topic A": [
            ("127.0.0.1", "50053"),
        ]
    }

    message = Server.get_message("Topic A", "Question 1", ["Answer 1", "Answer 0"])
    subscription = server.get_subscription("Topic A")

    server_thread = threading.Thread(target=server.run)
    subscribe_thread = threading.Thread(target=Server.send_subscribe, args=(subscription, "127.0.0.1", "50052"))
    unsubscribe_thread = threading.Thread(target=Server.send_unsubscribe, args=(subscription, "127.0.0.1", "50052"))
    broadcast_thread = threading.Thread(target=server.broadcast, args=(message,))

    broadcast_thread.start()
    subscribe_thread.start()
    unsubscribe_thread.start()
    server_thread.start()

    broadcast_thread.join()
    subscribe_thread.join()
    unsubscribe_thread.join()
    server_thread.join()
