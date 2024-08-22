from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 定义处理HTTP请求的类
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 检查请求路径
        if self.path == '/' or self.path == '/readonly':
            # 读取当前计数
            try:
                with open('number.txt', 'r') as f:
                    count = int(f.read().strip())
            except FileNotFoundError:
                count = 0
                with open('number.txt', 'w') as f:
                    f.write(str(count))

            # 如果请求路径是 /readonly，则不增加计数
            if self.path == '/readonly':
                response_data = {
                    "status": 200,
                    "description": "Nothing but a counter.",
                    "count": count
                }
            else:
                # 增加计数
                count += 1
                with open('number.txt', 'w') as f:
                    f.write(str(count))

                # 准备响应数据
                response_data = {
                    "status": 200,
                    "description": "Nothing but a counter.",
                    "count": count
                }

            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # 返回404状态码
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "status": 404,
                "description": "Not Found"
            }
            self.wfile.write(json.dumps(response_data).encode())

# 设置服务器
def run_server(port=1145):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'服务器正在监听端口 {port}...')
    httpd.serve_forever()

# 运行服务器
if __name__ == '__main__':
    run_server()
