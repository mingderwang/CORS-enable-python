from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import uuid
import time
""" The HTTP request handler """


class RequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers",
                         "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(json.dumps(d), "utf8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        result = json.dumps(
            {
                "id": str(uuid.uuid4()),
                "選號日期": time.strftime("%m/%d/%Y", time.localtime()),
                "可能中獎號碼": random.sample(range(10), 3),
                "猜中機率": 0
            },
            ensure_ascii=False)

        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(result.encode(encoding='utf_8'))

    def do_POST(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)

        print(data)

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)


print("Starting server")
httpd = HTTPServer(("0.0.0.0", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()
