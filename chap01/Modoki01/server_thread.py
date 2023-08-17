import os

import socket
import datetime


class ServerThread:
    DOCUMENT_ROOT = "/var/www/html"

    # コンストラクタ
    def __init__(self, socket: socket.socket):
        self.socket = socket

    # 一行読み込む
    def read_line(self, input_stream):
        ret = ""
        while True:
            ch = input_stream.recv(1).decode("utf-8")
            if ch == "\r":
                # 何もしない
                pass
            elif ch == "\n":
                break
            else:
                ret += ch
        return ret

    def write_line(self, output_stream, string):
        output_stream.sendall(string.encode("utf-8"))
        output_stream.sendall("\r\n".encode("utf-8"))

    def get_date_string_utc(self):
        cal = datetime.datetime.now(datetime.timezone.utc)
        date_format = "%a, %d %b %Y %H:%M:%S"
        return cal.strftime(date_format) + " GMT"

    def get_content_type(self, ext: str):
        # 拡張子の先頭のドットを削除
        ext = ext.lstrip(".")
        content_type_map = {
            "html": "text/html",
            "htm": "text/html",
            "txt": "text/plain",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
        }
        # レスポンスで送るファイル形式を返す(不明の場合のデフォルト値も用意)
        return content_type_map.get(ext.lower(), "application/octet-stream")

    def run(self):
        input_stream = self.socket
        output_stream = self.socket

        line = None
        file_path = None
        ext = None
        while True:
            line = self.read_line(input_stream)
            if not line:
                break
            if line.startswith("GET"):
                file_path = line.split(" ")[1]
                file_path = os.path.join(self.DOCUMENT_ROOT, file_path.lstrip("/"))
                _, ext = os.path.splitext(file_path)
                print("%sをレスポンスとして返します。" % file_path)

        try:
            with open(file_path, "rb") as file:
                response_body = file.read()
                # レスポンスヘッダ送信
                self.write_line(output_stream, "HTTP/1.1 200 OK")
                self.write_line(output_stream, "Date: " + self.get_date_string_utc())
                self.write_line(output_stream, "Server: Modoki/0.1")
                self.write_line(output_stream, "Connection: close")
                self.write_line(
                    output_stream, "Content-Type: " + self.get_content_type(ext)
                )
                self.write_line(output_stream, "")
                # レスポンスボディ送信
                output_stream.sendall(response_body)
        except Exception as ex:
            print(ex)
        finally:
            self.socket.close()
