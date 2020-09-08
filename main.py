import socket

URLS = {
    '/': 'hello index',
    '/blog': 'hello blog'
}


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if not url in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'

    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'

    return '<h1>{}</h1>'.format(URLS[url])


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)

    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # configuration
    server_socket.bind(('127.0.0.1', 5000))  # Bind with 127.0.0.1:5000 -> listen
    server_socket.listen()  # -> listen

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)  # num of bytes
        # print(request.decode('utf-8'))
        print(request)
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)  # response to the client
        client_socket.close()  # close socket


if __name__ == '__main__':
    run()
