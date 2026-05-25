
#!/usr/bin/env python3

import argparse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


def main():
    parser = argparse.ArgumentParser(description="Simple HTTP file server")
    parser.add_argument("-d", "--directory", default=".")
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    args = parser.parse_args()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=args.directory, **kw)

        def guess_type(self, path):
            return "application/octet-stream"

        def list_directory(self, path):
            self.send_error(403, "Directory listing disabled")
            return None

    server = ThreadingHTTPServer((args.bind, args.port), Handler)

    print(f"Serving {args.directory} on http://{args.bind}:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
