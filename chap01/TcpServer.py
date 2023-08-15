import socket

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8001))
    server.listen(1)
    print("クライアントからの接続を待ちます。")
    client_socket, client_address = server.accept()
    print("クライアント接続。")

    # server_recv.txtにバイナリデータを新規に書き込み、server_send.txtをバイナリファイルとして読み込む
    with open("server_recv.txt", "wb") as recv_file, open("server_send.txt", "rb") as send_file:
        # クライアントから受け取った内容をserver_recv.txtに出力
        while True:
            data = client_socket.recv(1)
            if not data:
                print("受信データが空になった。")
                break
            if data == b'\x00':
                print("クライアントから0を受信した。")
                break
            recv_file.write(data)

        # server_send.txtの内容をクライアントに送付
        while True:
            data = send_file.read(1)
            if not data:
                break
            client_socket.send(data)
        
    client_socket.close()
    print("通信を終了しました。")
    server.close()

if __name__ == "__main__":
    main()
