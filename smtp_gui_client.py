import socket
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
PORT = 2525


def send_email():

    username = username_entry.get()
    password = password_entry.get()

    sender = sender_entry.get()
    receiver = receiver_entry.get()

    subject = subject_entry.get()

    message = message_text.get("1.0", tk.END).strip()

    try:

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client.connect((HOST, PORT))

        client.recv(1024)

        # AUTH LOGIN
        client.send(b"AUTH LOGIN\r\n")

        client.recv(1024)

        client.send(
            f"{username}\r\n".encode()
        )

        client.recv(1024)

        client.send(
            f"{password}\r\n".encode()
        )

        response = client.recv(1024).decode()

        if "235" not in response:

            messagebox.showerror(
                "Error",
                "Authentication Failed"
            )

            client.close()

            return

        # HELO
        client.send(
            b"HELO localhost\r\n"
        )

        client.recv(1024)

        # MAIL FROM
        client.send(
            f"MAIL FROM:<{sender}>\r\n".encode()
        )

        client.recv(1024)

        # RCPT TO
        client.send(
            f"RCPT TO:<{receiver}>\r\n".encode()
        )

        client.recv(1024)

        # DATA
        client.send(
            b"DATA\r\n"
        )

        client.recv(1024)

        email = (
            f"Subject: {subject}\r\n\r\n"
            f"{message}\r\n.\r\n"
        )

        client.send(email.encode())

        response = client.recv(1024).decode()

        if "250" in response:

            messagebox.showinfo(
                "Success",
                "Email Sent Successfully!"
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed To Send Email"
            )

        client.send(b"QUIT\r\n")

        client.close()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==========================
# GUI
# ==========================

root = tk.Tk()

root.title("SMTP Mail Client")

root.geometry("600x500")

# Username

tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(
    root,
    width=40
)

username_entry.pack()

# Password

tk.Label(
    root,
    text="Password"
).pack()

password_entry = tk.Entry(
    root,
    show="*",
    width=40
)

password_entry.pack()

# Sender

tk.Label(
    root,
    text="Sender Email"
).pack()

sender_entry = tk.Entry(
    root,
    width=40
)

sender_entry.pack()

# Receiver

tk.Label(
    root,
    text="Receiver Email"
).pack()

receiver_entry = tk.Entry(
    root,
    width=40
)

receiver_entry.pack()

# Subject

tk.Label(
    root,
    text="Subject"
).pack()

subject_entry = tk.Entry(
    root,
    width=50
)

subject_entry.pack()

# Message

tk.Label(
    root,
    text="Message"
).pack()

message_text = tk.Text(
    root,
    height=10,
    width=60
)

message_text.pack()

# Send Button

send_button = tk.Button(
    root,
    text="SEND EMAIL",
    command=send_email,
    bg="lightgreen"
)

send_button.pack(pady=10)

root.mainloop()