from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector
import os

PORT = 8080

db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASS", ""),
    database=os.environ.get("DB_NAME", "")
)

cursor = db.cursor(dictionary=True)

class TodoHandler(BaseHTTPRequestHandler):
    def _send_response(self, code=200, data=None):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/tasks":
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            self._send_response(200, tasks)
        else:
            self._send_response(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/tasks":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                task = json.loads(post_data)
                if "title" in task:
                    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (task["title"],))
                    db.commit()
                    task_id = cursor.lastrowid
                    task["id"] = task_id
                    self._send_response(201, task)
                else:
                    self._send_response(400, {"error": "Task missing title"})
            except Exception as e:
                self._send_response(400, {"error": str(e)})
        else:
            self._send_response(404, {"error": "Not found"})

    def do_DELETE(self):
        if self.path.startswith("/tasks/"):
            try:
                task_id = int(self.path.split("/")[-1])
                cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                db.commit()
                self._send_response(200, {"message": f"Deleted task {task_id}"})
            except Exception as e:
                self._send_response(400, {"error": "Invalid task id"})
        else:
            self._send_response(404, {"error": "Not found"})

if __name__ == "__main__":
    print(f"Starting ToDo server on port {PORT}...")
    httpd = HTTPServer(("", PORT), TodoHandler)
    httpd.serve_forever()
