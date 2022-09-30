# Author: Yuzhao Luo
from flask import Flask, abort, Response, request
from socket import *

app = Flask(__name__)

@app.route('/')
def initialize():
    return "You can visit /fibonacci with a number to obtain its fibonacci number"

@app.route('/register', methods = ["PUT"], endpoint="register")
def fibonacciServer():

    hostname = request.json.get("hostname")
    ip = request.json.get("ip")
    as_ip = request.json.get("as_ip")
    as_port = request.json.get("as_port")

    dnsMessage = "TYPE=A\n" + "NAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
    address = (ip, 53533)

    fibonacciSocket = socket(AF_INET, SOCK_DGRAM)
    fibonacciSocket.sendto(dnsMessage.encode(), address)

    response, addr = fibonacciSocket.recvfrom(2048)
    print(response.decode())

    return Response("Registration Finished!", status=201)

@app.route('/fibonacci', methods = ["GET"], endpoint="fibonacci")
def fibonacciServer():
    arg = request.args
    if not arg.get("number"):
        abort(400, "Parameter Missing!")
    num = arg.get("number")

    for character in num:
        if character not in [str(i) for i in range(10)]:
            abort(400, "Wrong Parameter Type!")
    num = int(num)

    def fib(n):
        a, b = 1, 1
        for i in range(n - 1):
            a, b = b, a + b
        return a

    return str(fib(num))

app.run(host = '0.0.0.0',
        port = 9090,
        debug = True)