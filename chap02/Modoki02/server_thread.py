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
        relative_path = None
        ext = None
        while True:
            # 一行読み取り
            line = self.util.read_line(input_stream)
            # 空行ならば終了
            if not line:
                break
            # リクエストラインの場合
            if line.startswith("GET"):
                relative_path = line.split(" ")[1]
                # リクエストされたファイルのパスを取得
                relative_path = os.path.join(
                    self.DOCUMENT_ROOT, relative_path.lstrip("/")
                )
                # 拡張子を取得
                _, ext = os.path.splitext(relative_path)

        try:
            # 相対パスを絶対パスに変換
            absolute_path = os.path.realpath(relative_path, strict=True)
            # 指定されたパスがドキュメントルート以下に無い場合(ディレクトリトラバーサル攻撃の可能性)
            if not absolute_path.startswith(self.DOCUMENT_ROOT):
                raise FileNotFoundError
            with open(absolute_path, "rb") as file:
                response_body = file.read()
                print("%sをレスポンスとして返します。" % absolute_path)
                self.send_response.send_ok_response(output_stream, response_body, ext)
        except FileNotFoundError:
            # 指定されたファイルが見つからなかった、またはドキュメントルート外にあった場合
            print("%s は見つかりませんでした。" % relative_path)
            self.send_response.send_not_found_response(
                output_stream, self.ERROR_DOCUMENT
            )
        finally:
            self.socket.close()
