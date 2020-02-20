import socket, time, os, mimetypes, threading, glob, sys

access_counter = {}


class MultiThreading(threading.Thread):
    def __init__(self, addr, conn):
        threading.Thread.__init__(self)
        self.csocket = conn
        self.address = addr
        # print("New connection added: ", addr)

    def run(self):
        addr = self.address
        conn = self.csocket

        conn_info = conn.recv(4096)
        current_dt_str = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime())

        try:
            file_name = conn_info.split()[1].decode("utf-8")
            file_mime_type = mimetypes.guess_type(file_name)[0]
            if file_mime_type is None:
                file_mime_type = "application/octet-stream"

            to_show = file_name + "|" + str(addr[0]) + "|" + str(addr[1])
            file_path_name = './www' + file_name

            if glob.glob(file_path_name):
                lock = threading.Lock()
                lock.acquire()
                with open(file_path_name, 'rb') as content_file:
                    content = content_file.read()

                    last_modified = os.path.getmtime(file_path_name)
                    last_modified_str = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(last_modified))

                    conn.send('HTTP/1.1 200 OK\r\n'.encode())
                    conn.send("Server: shankyDaemon\r\n".encode())
                    conn.send(("Date: " + current_dt_str + "\r\n").encode())
                    conn.send(("Last-Modified: " + last_modified_str + "\r\n").encode())
                    conn.send(("Content-Length: " + str(len(content)) + "\r\n").encode())
                    conn.send(("Content-Type: " + file_mime_type + "\r\n\r\n").encode())
                    conn.send(content)

                    new_access_counter = access_counter[file_name] + 1
                    access_counter[file_name] = new_access_counter
                    print(to_show + "|" + str(new_access_counter))

                lock.release()

            else:
                raise Exception()

        except:
            # print("[Error]: File not found")
            with open('./error.html', 'rb') as content_file:
                content = content_file.read()
                conn.send('HTTP/1.1 404 Not found\r\n'.encode())
                conn.send("Server: shankyDaemon\r\n".encode())
                conn.send(("Date: " + current_dt_str + "\r\n").encode())
                conn.send(("Content-Length: " + str(len(content)) + "\r\n").encode())
                conn.send("Content-Type: text/html\r\n\r\n".encode())
                conn.send(content)

        conn.close()
        sys.exit()


def createAccessCounterMap():
    for files in os.walk("./www/"):
        key_str_pre = files[0][6:] + "/"
        if not key_str_pre.startswith("/"):
            key_str_pre = "/" + key_str_pre
        for filename in files[2]:
            key_str = key_str_pre + filename
            access_counter[key_str] = 0


def run():
    # next create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # reserve a port
    PORT = 8081

    sock.bind(('', PORT))
    print("socket binded to %s" % PORT)

    # put the socket into listening mode
    sock.listen(5)
    print("socket is listening")

    createAccessCounterMap()

    while True:
        conn, addr = sock.accept()
        client_thread = MultiThreading(addr, conn)
        client_thread.start()


run()
