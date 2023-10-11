#importing require modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from pynput import keyboard
import time

#target ip to connect
ip = "127.0.0.1"
port = 6789

#creating client socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

#tkinter functions
def update_scrollbox_typing(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    time.sleep(0.2)
    message_box.delete(1.0, tk.END)
    message_box.config(state=tk.DISABLED)

#update message box when typing status and online
def update_scrollbox(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)

def connect_to_the_server():
    #connecting to the server
    try:
        client_socket.connect((ip,port))
        print(f"Connected To The Server {ip}:{port}")
        update_scrollbox(f"connection established {ip}:{port}")

    except:
        messagebox.showerror("Connection Error",f"unable to connect to the server {ip} {port}")

    communicate_to_server()

#main while loop functions which are modified for gui
def communicate_to_server():

    username = username_textbox.get()
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    if username != "":
        client_socket.sendall(username.encode())

    else:
        messagebox.showerror("ERROR","username is empty!!")
        exit(0)

    threading.Thread(target=send_typing_status, args=(client_socket,)).start()
    threading.Thread(target=listen_for_messages_from_server,args=(client_socket, )).start()
    send_message_to_the_server()


def send_message():
    send_message_to_the_server()


#tkinter definations
root = tk.Tk()  #creating window
root.geometry("600x600")
root.title("Chat Messanger")
root.resizable(False,False)

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg="black")
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame,text="Username: ",font=FONT, bg='black', fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=22)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text='join',font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect_to_the_server)
username_button.pack(side=tk.RIGHT, padx=10)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=33)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text='send',font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.RIGHT, padx=15)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=64, height=27)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def display_help():
    help_text = """
    Available commands:
    /help - Display this help message
    /quit - Exit the chat room
    simple write anything as message 
    """
    return help_text

# Function to send typing status to the server
def send_typing_status(client_socket):
    
    time.sleep(0.5)
    client_socket.send("online".encode())
    key_count = 0
    def on_key_press(key):

        nonlocal key_count
        key_count += 1
        if key_count == 1:
            client_socket.send("typing".encode())
        if key_count >=10:
            client_socket.send("typing".encode())
            key_count = 0


    def on_key_release(key):
        pass

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()


def listen_for_messages_from_server(client_socket):

    while 1:
        #print("client is listing for messages")
        message = client_socket.recv(1024).decode("utf-8")

        if message != '':
            username = message.split("~")[0]
            content = message.split("~")[1]
            #print(f"[{username}]: {content}")
            if content == "typing":
                update_scrollbox_typing(f"[{username}]: {content}")

            update_scrollbox(f"[{username}]: {content}")

        else:
            messagebox.showerror("ERROR", "message is empty!!")


def send_message_to_the_server():

    message = message_textbox.get()
    message_textbox.delete(0, len(message))
    #/help section
    if message == '/help':
        update_scrollbox(display_help())

    elif message == '/quit':
        client_socket.sendall(message.encode())
        exit(0)

    elif message != '':
        client_socket.sendall(message.encode())

    else:
        messagebox.showerror("Unknown Command! ","Unknown command. Type '/help' for a list of available commands.")


def main():
    
    root.mainloop()

if __name__ == "__main__":
    main()
