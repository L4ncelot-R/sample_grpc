import Server
import threading

if __name__ == '__main__':
    server = Server.Server("127.0.0.1", "50053")
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    server_thread.join()
