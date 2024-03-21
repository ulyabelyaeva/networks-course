import sys, socket, subprocess

HOST = "127.0.0.1"
PORT = 65432
#PORT = int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('Server started')

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))

        command = data
        print("Command is:",command)
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if op:
            output = str(op.stdout.read())
            print("Output:",output)
            error = str(op.stderr.read())
            print("Error:",error)
            streamdata = op.communicate()[0]
            code = str(op.returncode)
            print("Return Code:",code)
            message = "Output: " + output + "\n Error: " + error + "\n Code: " + code
            conn.sendall(message.encode())

    conn.close()

