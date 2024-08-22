from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Define the class to handle HTTP requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check the request path
        if self.path == '/' or self.path == '/readonly':
            # Read the current count
            try:
                with open('number.txt', 'r') as f:
                    count = int(f.read().strip())
            except FileNotFoundError:
                count = 0
                with open('number.txt', 'w') as f:
                    f.write(str(count))

            # If the request path is /readonly, do not increment the count
            if self.path == '/readonly':
                response_data = {
                    "status": 200,
                    "description": "Nothing but a counter.",
                    "count": count
                }
            else:
                # Increment the count
                count += 1
                with open('number.txt', 'w') as f:
                    f.write(str(count))

                # Prepare the response data
                response_data = {
                    "status": 200,
                    "description": "Nothing but a counter.",
                    "count": count
                }

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # Return 404 status code
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "status": 404,
                "description": "Not Found"
            }
            self.wfile.write(json.dumps(response_data).encode())

# Set up the server
def run_server(port=1145):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Server is listening on port {port}...')
    httpd.serve_forever()

# Run the server
if __name__ == '__main__':
    run_server()
