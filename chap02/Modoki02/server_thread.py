import os
import socket
import util
import send_response


class ServerThread:
    DOCUMENT_ROOT = "/var/www/html"

    # コンストラクタ
    def __init__(self, socket: socket.socket):
        self.socket = socket
        self.util = util.Util()
        self.send_response = send_response.SendResponse()

    def run(self):
        input_stream = self.socket
        output_stream = self.socket

        line = None
        file_path = None
        ext = None
        while True:
            line = self.util.read_line(input_stream)
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
                self.send_response.send_ok_response(output_stream, response_body, ext)

        except Exception as ex:
            print(ex)
        finally:
            self.socket.close()
