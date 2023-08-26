import util


class SendResponse:
    def send_ok_response(self, output_stream, response_body, ext):
        m_util = util.Util()
        # レスポンスヘッダ送信
        m_util.write_line(output_stream, "HTTP/1.1 200 OK")
        m_util.write_line(output_stream, "Date: " + m_util.get_date_string_utc())
        m_util.write_line(output_stream, "Server: Modoki/0.2")
        m_util.write_line(output_stream, "Connection: close")
        m_util.write_line(
            output_stream, "Content-Type: " + m_util.get_content_type(ext)
        )
        m_util.write_line(output_stream, "")
        # レスポンスボディ送信
        output_stream.sendall(response_body)

    def send_move_permanently_response(self, output_stream, location):
        m_util = util.Util()
        # レスポンスヘッダ送信
        m_util.write_line(output_stream, "HTTP/1.1 301 Moved Permanently")
        m_util.write_line(output_stream, "Date: " + m_util.get_date_string_utc())
        m_util.write_line(output_stream, "Server: Modoki/0.2")
        m_util.write_line(output_stream, "Connection: close")
        m_util.write_line(output_stream, "Location: " + location)
        m_util.write_line(output_stream, "")
        # レスポンスボディは無し

    def send_not_found_response(self, output_stream, error_document_root):
        m_util = util.Util()
        # レスポンスヘッダ送信
        m_util.write_line(output_stream, "HTTP/1.1 404 Not Found")
        m_util.write_line(output_stream, "Date: " + m_util.get_date_string_utc())
        m_util.write_line(output_stream, "Server: Modoki/0.2")
        m_util.write_line(output_stream, "Connection: close")
        m_util.write_line(output_stream, "Content-type: text/html")
        m_util.write_line(output_stream, "")
        # レスポンスボディ送信
        file_path = error_document_root.rstrip("/") + "/404.html"
        try:
            with open(file_path, "rb") as file:
                print("%sをレスポンスとして返します。" % file_path)
                response_body = file.read()
                output_stream.sendall(response_body)
        except Exception as ex:
            print(ex)
