import util


class SendResponse:
    def send_ok_response(self, output_stream, response_body, ext):
        m_util = util.Util()
        # レスポンスヘッダ送信
        m_util.write_line(output_stream, "HTTP/1.1 200 OK")
        m_util.write_line(output_stream, "Date: " + m_util.get_date_string_utc())
        m_util.write_line(output_stream, "Server: Modoki/0.1")
        m_util.write_line(output_stream, "Connection: close")
        m_util.write_line(
            output_stream, "Content-Type: " + m_util.get_content_type(ext)
        )
        m_util.write_line(output_stream, "")
        # レスポンスボディ送信
        output_stream.sendall(response_body)
