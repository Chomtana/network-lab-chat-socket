import socket  
import select  
import sys  
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

HOST = '127.0.0.1'
PORT = int('6131307621'[3:8]) + 20000
  
server.bind((HOST, PORT))
server.listen(100)
  
clients = []  
  
def client_handler(conn, addr):
    username = conn.recv(2048).decode('utf8')
    print("LOGIN", username)

    # conn.send("Welcome".encode('utf8'))
    while True:  
        try:  
            message = conn.recv(2048)  
            if message:  
                print("RECEIVED", message)
                broadcast(message, username, conn)

            else:
                remove(conn) # Remove connection if no content provided

        except:  
            continue
  
def broadcast(message, username, connection):  
    for client in clients:
        try:
            targetMessage = "[" + username + "] " + message.decode('utf8')
            client.send(targetMessage.encode('utf8'))  
            print("SEND", targetMessage)
        except Exception as e:
            print("SEND ERROR")
            print(e)
            client.close()
            remove(client) # If sending failed -> Remove connection  

def remove(connection):  
    if connection in clients:  
        clients.remove(connection)

print("SERVER LISTENING ON PORT", PORT)  

while True:
    conn, addr = server.accept()  
    clients.append(conn)
    print (addr[0] + " Connected !!!") 
    threading.Thread(target=client_handler, args=(conn,addr)).start()  
  
conn.close()  
server.close()  