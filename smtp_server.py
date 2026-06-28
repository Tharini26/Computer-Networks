import socket
import threading
import os
from datetime import datetime

HOST = "127.0.0.1"
PORT = 2525

# User Accounts
USERS = {
    "admin": "1234",
    "alice": "alice123",
    "bob": "bob123"
}

os.makedirs("mail_storage", exist_ok=True)

# ==========================
# LOGGING FUNCTION
# ==========================

def write_log(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "smtp.log",
        "a",
        encoding="utf-8"
    ) as log:

        log.write(
            f"[{timestamp}] {message}\n"
        )


# ==========================
# CLIENT HANDLER
# ==========================

def handle_client(conn, addr):

    print(f"\nConnected: {addr}")

    write_log(
        f"CLIENT CONNECTED {addr}"
    )

    authenticated = False
    username = ""
    receiver = ""

    conn.send(
        b"220 SMTP Server Ready\r\n"
    )

    while True:

        try:

            data = conn.recv(1024)

            if not data:
                break

            text = data.decode().strip()

            print("CLIENT:", text)

            # =====================
            # AUTH LOGIN
            # =====================

            if text == "AUTH LOGIN":

                conn.send(
                    b"334 Username:\r\n"
                )

                username = conn.recv(
                    1024
                ).decode().strip()

                conn.send(
                    b"334 Password:\r\n"
                )

                password = conn.recv(
                    1024
                ).decode().strip()

                if (
                    username in USERS
                    and USERS[username] == password
                ):

                    authenticated = True

                    write_log(
                        f"LOGIN SUCCESS : {username}"
                    )

                    conn.send(
                        b"235 Authentication Successful\r\n"
                    )

                else:

                    write_log(
                        f"LOGIN FAILED : {username}"
                    )

                    conn.send(
                        b"535 Authentication Failed\r\n"
                    )

            # =====================
            # REQUIRE LOGIN
            # =====================

            elif not authenticated:

                conn.send(
                    b"530 Authentication Required\r\n"
                )

            # =====================
            # HELO
            # =====================

            elif text.startswith("HELO"):

                conn.send(
                    b"250 Hello\r\n"
                )

            # =====================
            # MAIL FROM
            # =====================

            elif text.startswith(
                "MAIL FROM"
            ):

                conn.send(
                    b"250 Sender OK\r\n"
                )

            # =====================
            # RCPT TO
            # =====================

            elif text.startswith(
                "RCPT TO"
            ):

                email = text.split(
                    "<"
                )[1].split(">")[0]

                receiver = email.split(
                    "@"
                )[0]

                conn.send(
                    b"250 Recipient OK\r\n"
                )

            # =====================
            # DATA
            # =====================

            elif text == "DATA":

                conn.send(
                    b"354 Enter message, end with '.'\r\n"
                )

                email_data = ""

                while True:

                    chunk = conn.recv(
                        1024
                    ).decode()

                    if not chunk:
                        break

                    if "\r\n.\r\n" in chunk:

                        email_data += chunk.replace(
                            "\r\n.\r\n",
                            ""
                        )

                        break

                    email_data += chunk

                filename = (
                    f"mail_storage/{receiver}.txt"
                )

                with open(
                    filename,
                    "a",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        "\n========== EMAIL ==========\n"
                    )

                    f.write(email_data)

                    f.write(
                        "\n===========================\n"
                    )

                print(
                    f"EMAIL SAVED TO {filename}"
                )

                write_log(
                    f"MAIL DELIVERED -> "
                    f"User:{username} "
                    f"Mailbox:{receiver}"
                )

                conn.send(
                    b"250 Message Saved\r\n"
                )

            # =====================
            # QUIT
            # =====================

            elif text == "QUIT":

                conn.send(
                    b"221 Goodbye\r\n"
                )

                break

            else:

                conn.send(
                    b"500 Unknown Command\r\n"
                )

        except Exception as e:

            print("ERROR:", e)

            write_log(
                f"ERROR {e}"
            )

            break

    write_log(
        f"CLIENT DISCONNECTED {addr}"
    )

    conn.close()

    print("Connection Closed")


# ==========================
# SERVER START
# ==========================

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen(5)

print(
    f"SMTP Server running on {HOST}:{PORT}"
)

while True:

    conn, addr = server.accept()

    threading.Thread(
        target=handle_client,
        args=(conn, addr)
    ).start()