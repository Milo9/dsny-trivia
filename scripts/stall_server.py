"""Static file server for the isolated browser checks that can simulate stalled wifi.

Usage: python scripts/stall_server.py PORT STALL_FLAG_PATH   (serves the current directory)

While STALL_FLAG_PATH exists, every request is accepted but left unanswered (up to
60 s), like ship or hotel wifi that connects but never delivers. Removing the flag
releases waiting requests at once. Test-only; never used by the app.
"""
import os
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    stall_flag = ''

    def handle_one_request(self):
        deadline = time.monotonic() + 60
        while os.path.exists(self.stall_flag) and time.monotonic() < deadline:
            time.sleep(0.1)
        super().handle_one_request()

    def log_message(self, *args):
        pass


def main():
    port, flag = int(sys.argv[1]), sys.argv[2]
    Handler.stall_flag = flag
    server = ThreadingHTTPServer(('127.0.0.1', port), partial(Handler, directory=os.getcwd()))
    server.daemon_threads = True
    server.serve_forever()


if __name__ == '__main__':
    main()
