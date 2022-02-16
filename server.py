import socket
from threading import Thread
from datetime import datetime
from serverHelper import broadcast, publicAnnouncement, privateMessage, sendFile, receiveFile, seeAll, clientStatus, instructions, createGroup, renameGroup, seeMembers, addMembers, removeMembers, joinGroup, leaveGroup, sendGroupMessage, deleteGroup, quitOnline

def accept_clients_IPv4():
    while True:
        clientIPv4, client_addressIPv4 = socket_IPv4.accept()
        print("%s:%s has connected." % client_addressIPv4)
        clientIPv4.send(bytes("Welcome to the chat server!", "utf8"))
        clientIPv4.send(bytes("\nFirst, please enter your name in the text box next to 'Register/Login' button and click on it to register/login", "utf8"))
        name = clientIPv4.recv(buffer).decode("utf8")
        registeredAddresses[name] = client_addressIPv4
        registeredClients[name] = clientIPv4 # socket
        onlineClients[name] = clientIPv4 # socket
        clientIPv4.send(bytes("\nClick 'Help' button to see instructions on how to use the chat application", "utf8"))
        message = f"{name} has joined the server"
        broadcast(message, onlineClients)

        if name not in bufferedMessages:
            bufferedMessages[name] = []
        elif len(bufferedMessages[name]) != 0:
            clientIPv4.send(bytes("Unseen messages\n", "utf8"))
            for unseenMessage in bufferedMessages[name]:
                clientIPv4.send(bytes(f"{unseenMessage}\n", "utf8"))
        Thread(target=handle_client, args=(name, clientIPv4)).start()

def accept_clients_IPv6():
    while True:
        clientIPv6, client_addressIPv6 = socket_IPv6.accept()
        print("%s:%s:%s:%s has connected." % client_addressIPv6)
        clientIPv6.send(bytes("Welcome to the chat server!", "utf8"))
        clientIPv6.send(bytes("\nFirst, please enter your name in message box and click 'Register/Login' button", "utf8"))
        name = clientIPv6.recv(buffer).decode("utf8")
        registeredAddresses[name] = client_addressIPv6
        registeredClients[name] = clientIPv6 # socket
        onlineClients[name] = clientIPv6 # socket
        clientIPv6.send(bytes("\nClick 'Help' button to see instructions on how to use the chat application", "utf8"))
        message = f"{name} has joined the server"
        broadcast(message, onlineClients)

        if name not in bufferedMessages:
            bufferedMessages[name] = []
        elif len(bufferedMessages[name]) != 0:
            clientIPv6.send(bytes("Unseen messages\n", "utf8"))
            for unseenMessage in bufferedMessages[name]:
                clientIPv6.send(bytes(f"{unseenMessage}\n", "utf8"))
        Thread(target=handle_client, args=(name, clientIPv6)).start()

def handle_client(senderName, client):  
    while True:
        if senderName not in onlineClients:
            break
        message = client.recv(buffer).decode("utf8") # String
        if message.startswith("/all "): # Command /all <message>
            publicAnnouncement(senderName, message[5:], onlineClients, registeredClients, bufferedMessages)
        elif message.startswith("/pm "): # Command /pm <client name> <message>
            privateMessage(senderName, message[4:], onlineClients, registeredClients, lastOnline, bufferedMessages)
        elif message.startswith("/file "): # Command /file <client name> <file path>
            sendFile(senderName, message[6:], onlineClients, fileDatabase, bufferedMessages)
        elif message.startswith("/receive "): # Command /receive <file path> as <file name>
            receiveFile(senderName, message[9:], onlineClients, fileDatabase)
        elif message.startswith("/see"): # Command /see
            seeAll(senderName, onlineClients, registeredClients, groupCreator)
        elif message.startswith("/status "): # Command /status <client name>
            clientStatus(senderName, message[8:], onlineClients, registeredClients, lastOnline)
        elif message.startswith("/command"): # Command /command
            instructions(senderName, onlineClients)
        elif message.startswith("/create "): # Command /create <group name>
            createGroup(senderName, message[8:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/rename "): # Command /rename <group name> <new group name> 
            renameGroup(senderName, message[8:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/add "): # Command /add <group name> <member> <member>...<member>
            addMembers(senderName, message[5:], groupCreator, groupMembers, onlineClients, registeredClients)
        elif message.startswith("/remove "): # Command /remove <group name> <member> <member>...<member>
            removeMembers(senderName, message[8:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/delete "): # Command /delete <group name>
            deleteGroup(senderName, message[8:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/members "): # Command /members <group name>
            seeMembers(senderName, message[9:], groupCreator, groupMembers, onlineClients)    
        elif message.startswith("/join "): # Command /join <group name>
            joinGroup(senderName, message[6:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/leave "): # Command /leave <group name>
            leaveGroup(senderName, message[7:], groupCreator, groupMembers, onlineClients)
        elif message.startswith("/send "): # Command /send <group name> <message>
            sendGroupMessage(senderName, message[6:], groupCreator, groupMembers, onlineClients, bufferedMessages)
        elif message.startswith("/quit"): # Command /quit
            quitOnline(senderName, onlineClients, lastOnline)
        else: 
            client.send(bytes("Unknown command", "utf8"))

# Server starts

registeredClients = {} # dict of name - registered client sockets
registeredAddresses = {} # dict of name - client addresses
onlineClients = {} # dict of name - online client sockets
lastOnline = {} # dict of name - last online time
groupCreator = {} # dict of group name - group creator
groupMembers = {} # dict of group name - group members
bufferedMessages = {} # dict of receiver - buffered messages list
fileDatabase = {} # dict of file name - file data

buffer = 4096
backlog = 5
localIPv4 = "192.168.1.208"
globalIPv4 = "87.92.16.209"
localIPv6 = "fe80::c10c:de5e:2cbf:132c%9"
globalIPv6 = "2001:14ba:a0bd:dd00:c10c:de5e:2cbf:132c"
port_IPv4 = 34000
port_IPv6 = 36000
address_IPv4 = (localIPv4, port_IPv4)
address_IPv6 = (globalIPv6, port_IPv6)
socket_IPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_IPv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
socket_IPv4.bind(address_IPv4)
socket_IPv6.bind(address_IPv6)
socket_IPv4.listen(backlog)
socket_IPv6.listen(backlog)

if __name__ == "__main__":
    socket_IPv4.listen(5)
    print("Waiting for the clients to connect...")
    server_IPv4 = Thread(target=accept_clients_IPv4)
    server_IPv6 = Thread(target=accept_clients_IPv6)
    server_IPv4.start()
    server_IPv6.start()
    server_IPv4.join()
    server_IPv6.join()
    socket_IPv4.close()
    socket_IPv6.close()