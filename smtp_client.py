import socket

HOST = "127.0.0.1"
PORT = 2525

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

print(client.recv(1024).decode())

# AUTH LOGIN
client.send(b"AUTH LOGIN\r\n")

print(client.recv(1024).decode())

username = input("Username: ")

client.send(f"{username}\r\n".encode())

print(client.recv(1024).decode())

password = input("Password: ")

client.send(f"{password}\r\n".encode())

response = client.recv(1024).decode()

print(response)

if "235" not in response:

    print("Login Failed")

    client.close()

    exit()

# HELO
client.send(b"HELO localhost\r\n")
print(client.recv(1024).decode())

sender = input("Sender Email: ")
receiver = input("Receiver Email: ")

client.send(
    f"MAIL FROM:<{sender}>\r\n".encode()
)

print(client.recv(1024).decode())

client.send(
    f"RCPT TO:<{receiver}>\r\n".encode()
)

print(client.recv(1024).decode())

client.send(b"DATA\r\n")

print(client.recv(1024).decode())

subject = input("Subject: ")
message = input("Message: ")

email = (
    f"Subject: {subject}\r\n\r\n"
    f"{message}\r\n.\r\n"
)

client.send(email.encode())

print(client.recv(1024).decode())

client.send(b"QUIT\r\n")

print(client.recv(1024).decode())

client.close()