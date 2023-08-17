import datetime


class Util:
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
