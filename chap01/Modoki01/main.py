import socket
import threading
import server_thread


def connect():
    # アドレスファミリーにIPv4プロトコル、ソケットタイプにTCPソケット通信を指定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 8001))
        server.listen()
        # ここは無限ループする
        while True:
            print("クライアントからの接続を待ちます...")
            client_socket, _ = server.accept()
            server_thread_obj = server_thread.ServerThread(client_socket)
            thread = threading.Thread(target=server_thread_obj.run)
            thread.start()


if __name__ == "__main__":
    connect()
