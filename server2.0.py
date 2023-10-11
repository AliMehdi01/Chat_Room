#importing require modules
import socket
import threading

# DEFINE
ip = "127.0.0.1"
port = 6789
active_clients = [] # list of all connected users

#function to listen for upcomming messages from the client
def listen_for_messages(client_socket,username):
    
    while 1:

        #print("listening for messages")
        message = client_socket.recv(1024).decode('utf-8')
        
        if message == '/quit':
            quit_promte = "| ADMIN |" + '~' f"'{username}'" + " exit the chat!!"
            send_messages_to_all(quit_promte)
            username_to_remove = username
           
            for username, client_socket in active_clients:
                if username == username_to_remove:
                    active_clients.remove((username,client_socket))
                    print(f"'{username_to_remove}' exit the chat!!")
                    break
        
        elif message == 'typing':
            #active_clients[(username,client_socket)]['status'] = 'typing'
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        
        elif message == 'online':
            #active_clients[(username,client_socket)]['status'] = 'Online'
            final_msg = username + '~' + "Online"
            send_messages_to_all(final_msg)

        elif message == 'offline':
            final_msg = username + '~' + "offline"
            send_messages_to_all(final_msg)

        elif message != '':
            final_msg = username + '~' + message
            #print("send messages to all function called")
            send_messages_to_all(final_msg)
        
        else:
            print(f"empty message {username}")


#function to send message to a single client
def send_message_to_client(client_socket,message):
    
    #print("message send success full")
    client_socket.sendall(message.encode())
    

#this will broadcast the message from client to all the clients connected in the instance
def send_messages_to_all(message):
    
    #user[1] is client sockets
    #print("send_message to all")
    for users in active_clients:
        send_message_to_client(users[1], message)

#function to handle clients
def client_handler(client_socket):
    #server asking for clients username
    while 1:

        username = client_socket.recv(128).decode('utf-8')
        print(f"'{username}' join the chat")
        notify = "| ADMIN |" + '~' f"'{username}' join the chat!!"
        send_messages_to_all(notify)
        
        if username != "":
            active_clients.append((username,client_socket))
            #print("append success!!")
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_messages,args=(client_socket,username, )).start()

def main():
    
    #creating the socket class object
    #AF_INET = IPv4 address family
    #socket_stream = tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #giving server ip and port to bind
        server_socket.bind((ip, port))
        print(f"server started running on {ip}:{port}")
    except:
        #if any error in binding
        print(f"Unable to find the ip {ip} and port {port}")

    #setting server limit and setting on listing
    server_socket.listen(5)

    #this while loop will keep listing to client connections
    while 1:

        client_socket, client_add = server_socket.accept()
        print(f"Client connected {client_add[0]} {client_add[1]}")

        #its just like funciton call thats it client_handler
        threading.Thread(target=client_handler,args=(client_socket, )).start()



if __name__ == '__main__': 
    main()
