# Author: Yuzhao Luo

from socket import *

authoritativeSocket = socket(AF_INET, SOCK_DGRAM)
authoritativeSocket.bind(('', 53533))

while True:
    message, clientAddress = authoritativeSocket.recvfrom(2048)
    message = message.decode()

    print(message)

    length = message.split('\n')

    if len(length) == 2:
        flag = 'Query'
    else:
        flag = 'Register'
    for line in length:
        name, value = line.split('=')
        if name == "NAME":
            hostname = value
        if name == "VALUE":
            ip = value
    if flag == "Register":
        file = open("DNS.txt", "a+")
        file.write(message + '\n')
        file.close()

        response = b'Finished Registration!'
        authoritativeSocket.sendto(response, clientAddress)
    else:
        ip = "0.0.0.0"
        with open("DNS.txt", "r") as f:
            line = f.readline()
            while line.strip() != "":
                if line.find(hostname) != -1:
                    line = f.readline()
                    name, value = line.split('=')
                    ip = value
                    break
                line = f.readline()

        responseMessage = "TYPE=A\n" + "NAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
        authoritativeSocket.sendto(responseMessage.encode(), clientAddress)
        print("Query DNS File Successfully!")