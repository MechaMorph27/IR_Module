import socket

IP = "192.168.1.1"
# IP ="172.17.4.26"
PORT = 23

try:
    print("Connecting to device (Telnet mode)...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((IP, PORT))

    print("Connected successfully!")

    # send your instrument command
    cmd = "READ?\n"
    s.send(cmd.encode())

    data = s.recv(1024).decode(errors="ignore")

    print("RAW DATA FROM MACHINE:")
    print(data)

    s.close()

except Exception as e:
    print("Connection failed:", e)