import os

user = input("Enter mailbox name: ")

filename = f"mail_storage/{user}.txt"

if os.path.exists(filename):

    with open(filename, "r", encoding="utf-8") as f:
        print("\nMAILBOX CONTENTS\n")
        print(f.read())

else:
    print("Mailbox does not exist.")