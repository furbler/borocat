import socket
import os
import time
from datetime import datetime

DOCUMENT_ROOT = "/var/www/html"


def read_line(sock):
    line = b""
    while True:
        byte = sock.recv(1)
        if byte == b"\n" or not byte:
            break
        if byte != b"\r":
            line += byte
    return line.decode("utf-8")


def write_line(sock, line):
    sock.sendall(line.encode("utf-8") + b"\r\n")


def get_date_string_utc():
    now = datetime.utcnow()
    return now.strftime("%a, %d %b %Y %H:%M:%S") + " GMT"


def main():
    # アドレスファミリーにIPv4プロトコル、ソケットタイプにTCPソケット通信を指定
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8001))
    server.listen(1)
    print("クライアントからの接続を待ちます。")
    client_socket, client_address = server.accept()
    print("Connected to", client_address)

    try:
        file_path = ""
        # クライアントの通信を一行ずつ読み込む
        while True:
            request_line = read_line(client_socket)
            # 空白区切りで行を分割
            request_parts = request_line.split(" ")
            # リクエストヘッダ終了の空行を受け取ったらループを抜ける
            if request_parts[0] == "":
                break
            # リクエストラインの場合
            elif len(request_parts) >= 2 and request_parts[0] == "GET":
                requested_path = request_parts[1]
                file_path = os.path.join(DOCUMENT_ROOT, requested_path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                response_body = file.read()
            response_head = [
                "HTTP/1.1 200 OK",
                "Date: " + get_date_string_utc(),
                "Server: Modoki/0.1",
                "Connection: close",
                "Content-type: text/html",
                "",
            ]
            # 送信文字列をbytes型に変換して送信
            # レスポンスヘッダ送信
            client_socket.sendall("\r\n".join(response_head).encode("utf-8"))
            # レスポンスボディ送信
            client_socket.sendall(response_body)
        else:
            # リクエストされたファイルが存在しなければ404 Not Foundと空行を返す
            client_socket.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode("utf-8"))
    except Exception as e:
        print("Error:", e)

    client_socket.close()


if __name__ == "__main__":
    main()
