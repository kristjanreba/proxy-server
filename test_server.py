import http.server
import json
import os
import socketserver

# Get the test server port from the TEST_SERVER_PORT environment variable
PORT = int(os.environ.get("TEST_SERVER_PORT", 8001))


class TestServerHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode())

        # Prepare the response JSON
        response_data = {
            "status": "success",
            "message": "Data received successfully",
            "payload": payload,
        }

        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())


def run_test_server():
    server_address = ("0.0.0.0", PORT)
    httpd = socketserver.TCPServer(server_address, TestServerHandler)
    print(f"Test server started at port {PORT}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Test server shutting down.")
        httpd.server_close()


if __name__ == "__main__":
    run_test_server()
