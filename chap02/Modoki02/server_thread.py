import os
import socket
import util
import send_response


class ServerThread:
    DOCUMENT_ROOT = os.path.expanduser("~/test/webserver/")
    ERROR_DOCUMENT = os.path.expanduser("~/test/webserver/error_document")
    SERVER_NAME = "localhost:8001"

    # コンストラクタ
    def __init__(self, socket: socket.socket):
        self.socket = socket
        self.util = util.Util()
        self.send_response = send_response.SendResponse()

    def run(self):
        input_stream = self.socket
        output_stream = self.socket

        line = None
        request_path = None
        ext = None
        host = None
        while True:
            # 一行読み取り
            line = self.util.read_line(input_stream)
            # 空行ならば終了
            if not line:
                break
            # リクエストラインの場合
            if line.startswith("GET"):
                request_path = line.split(" ")[1]
                # 拡張子を取得
                _, ext = os.path.splitext(request_path)
            elif line.startswith("Host:"):
                # Hostヘッダフィールドを取得
                host = line[len("Host:") :].strip()
        # リクエストラインが無い場合は終了
        if request_path is None:
            return
        # リクエストされたパスがディレクトリの場合
        if request_path.endswith("/"):
            # パスにindex.htmlを追加する
            request_path += "index.html"
            ext = ".html"

        try:
            # リクエストされたファイルのパスを取得
            relative_path = os.path.join(self.DOCUMENT_ROOT, request_path.lstrip("/"))
            # 相対パスを絶対パスに変換(パスが存在しない場合は例外を投げる)
            absolute_path = os.path.realpath(relative_path, strict=True)
            # 指定されたパスがドキュメントルート以下に無い場合(ディレクトリトラバーサル攻撃の可能性)
            if not absolute_path.startswith(self.DOCUMENT_ROOT):
                # パスが存在しない場合と同じ例外を投げる
                raise FileNotFoundError
            elif os.path.isdir(absolute_path):
                # 指定されたパスがディレクトリの場合はリダイレクト処理を行う
                location = (
                    "http://"
                    + (host if host is not None else self.SERVER_NAME)
                    + request_path
                    + "/"
                )
                self.send_response.send_move_permanently_response(
                    output_stream, location
                )
                # 関数を抜ける前にfinallyブロックは実行される
                return

            with open(absolute_path, "rb") as file:
                response_body = file.read()
                print("%sをレスポンスとして返します。" % absolute_path)
                self.send_response.send_ok_response(output_stream, response_body, ext)
        except FileNotFoundError:
            # 指定されたファイルが見つからなかった、またはドキュメントルート外にあった場合
            print("%s は見つかりませんでした。" % absolute_path)
            self.send_response.send_not_found_response(
                output_stream, self.ERROR_DOCUMENT
            )
        finally:
            self.socket.close()
