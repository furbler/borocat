import socket

def main():
    # アドレスファミリーにIPv4プロトコル、ソケットタイプにTCPソケット通信を指定
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 指定のアドレス、ポート番号に接続要求
    client.connect(('localhost', 8001))

    # client_send.txtをバイナリファイルとして読み込み、client_recv.txtにバイナリデータを新規に書き込む
    with open("client_send.txt", "rb") as send_file, open("client_recv.txt", "wb") as recv_file:
        # client_send.txtの内容をサーバに送信
        while True:
            data = send_file.read(1)
            if not data:
                break
            client.send(data)
        
        # 終了を示すため、ゼロを送信
        client.send(b'\x00')
        print("送信完了の0を送信した。")
        
        # サーバからの返信をclient_recv.txtに出力
        while True:
            data = client.recv(1)
            if not data:
                break
            recv_file.write(data)

    client.close()

if __name__ == "__main__":
    main()
