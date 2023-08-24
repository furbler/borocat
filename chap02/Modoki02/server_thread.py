import os
import socket
import util
import send_response


class ServerThread:
    DOCUMENT_ROOT = os.path.expanduser("~/test/webserver/index")
    ERROR_DOCUMENT = os.path.expanduser("~/test/webserver/error_document")

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
            # 一行読み取り
            line = self.util.read_line(input_stream)
            # 空行ならば終了
            if not line:
                break
            # リクエストラインの場合
            if line.startswith("GET"):
                file_path = line.split(" ")[1]
                # フルパスを取得
                file_path = os.path.join(self.DOCUMENT_ROOT, file_path.lstrip("/"))
                # 拡張子を取得
                _, ext = os.path.splitext(file_path)

        try:
            with open(file_path, "rb") as file:
                response_body = file.read()
                print("%sをレスポンスとして返します。" % file_path)
                self.send_response.send_ok_response(output_stream, response_body, ext)
        except FileNotFoundError:
            # 指定されたファイルが見つからなかった場合
            self.send_response.send_not_found_response(
                output_stream, self.ERROR_DOCUMENT
            )
        finally:
            self.socket.close()
