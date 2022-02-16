import socket
from threading import Thread
import tkinter
import tkinter.messagebox

top = tkinter.Tk()
top.title("Chat Application")

# The ISP of the network does not support IPv6. There are no global IPv6

localIPv6 = "fe80::c10c:de5e:2cbf:132c%9"
portIPv6 = 36000
buffer = 1024
backlog = 5

def receive(event=None):
    while True:
        message = clientSocketIPv6.recv(buffer).decode("utf8")
        if message.startswith("/downloaded"):
            fileData = message.split("\n")[1]
            fileName = message.split("\n")[2]
            newFile = open(fileName, "a")
            newFile.write(fileData)
            newFile.close()
        elif message.startswith("You have quitted from the server. See you again"):
            receiveBox.insert(tkinter.END, message + "\n")
            clientSocketIPv6.close()
            top.quit()
            break
        else:
            receiveBox.insert(tkinter.END, message + "\n")

def send(command):
    message = sendBox.get()
    receiverName = receiverBox.get()
    groupName = groupBox.get()
    if command == "": # Logging in
        name = registerLoginName.get()
        top.title(f"User {name} - IPv6")
        serverMessage = f"{name}"
        sendBox.set("")  
        registerLoginName.set("")
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/all" or command == "/receive": # Announce
        serverMessage = f"{command} {message}"
        sendBox.set("") 
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/pm" or command == "/file": # Send PM, send file
        serverMessage = f"{command} {receiverName} {message}"
        sendBox.set("")  
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/command" or command == "/see":
        serverMessage = f"{command}"
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/status": 
        serverMessage = f"{command} {receiverName}"
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/create" or command == "/delete" or command == "/join" or command == "/leave": 
        serverMessage = f"{command} {groupName}"
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/rename": 
        serverMessage = f"{command} {groupName} {message}"
        sendBox.set("")
        groupBox.set("")
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/add" or command == "/remove": 
        serverMessage = f"{command} {groupName} {message}"
        sendBox.set("")
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/send":
        serverMessage = f"{command} {groupName} {message}"
        sendBox.set("")
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 
    elif command == "/quit":
        serverMessage = f"{command}"
        sendBox.set("")  # Clears input field.
        receiverBox.set("")
        groupBox.set("")
        clientSocketIPv6.send(bytes(serverMessage, "utf8")) 

def handleExitProtocol():
    if tkinter.messagebox.askyesnocancel(title= "Exit the chat server", message= "Are you sure you want to exit the chat application?"):
       # close the application
       send("/quit")
       top.destroy()


topFrame = tkinter.Frame(top,bg="black")
topFrame.pack()
# Right frame, packed
rightFrame = tkinter.Frame(top,bg="white")
rightFrame.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Right frame, receiverGroupFrame
receiverGroupFrame = tkinter.Frame(rightFrame)
receiverGroupFrame.pack()

stringVarReceiverBox = tkinter.StringVar() 
stringVarReceiverBox.set("Receiver: ")
labelReceiverBox= tkinter.Label(receiverGroupFrame, textvariable=stringVarReceiverBox)
labelReceiverBox.grid(row=1, column=1)

receiverBox = tkinter.StringVar()
receiverEntry = tkinter.Entry(receiverGroupFrame, textvariable=receiverBox)
receiverEntry.grid(row=1,column=2)

stringVarGroupBox = tkinter.StringVar() 
stringVarGroupBox.set("Group: ")
labelGroupBox= tkinter.Label(receiverGroupFrame, textvariable=stringVarGroupBox)
labelGroupBox.grid(row=1, column=3)

groupBox = tkinter.StringVar()
groupEntry = tkinter.Entry(receiverGroupFrame, textvariable=groupBox)
groupEntry.grid(row=1,column=4)

# Right frame, receiveBoxFrame
receiveBoxFrame = tkinter.Frame(rightFrame)
receiveBoxFrame.pack()

scrollbar = tkinter.Scrollbar(receiveBoxFrame)  

# For the messages to be received.
receiveBox = tkinter.Text(receiveBoxFrame, height=20, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
receiveBox.pack(fill=tkinter.BOTH)

# Right frame, sendBoxFrame
sendBoxFrame = tkinter.Frame(rightFrame)
sendBoxFrame.pack()

stringVarSendBox= tkinter.StringVar() 
stringVarSendBox.set("Message: ")
labelSendBox= tkinter.Label(sendBoxFrame, textvariable=stringVarSendBox)
labelSendBox.grid(row=1, column=1)


sendBox = tkinter.StringVar()  # For the messages to be sent.
sendEntry = tkinter.Entry(sendBoxFrame, textvariable=sendBox, width=65)
sendEntry.grid(row=1,column=2)



sendPM_button = tkinter.Button(sendBoxFrame, text= "Send PM", command=lambda: send("/pm"))
sendGM_button = tkinter.Button(sendBoxFrame, text= "Send GM", command=lambda: send("/send"))

sendPM_button.grid(row=1,column=3)
sendGM_button.grid(row=1,column=4)


# Left frame, packed
leftFrame = tkinter.Frame(top,bg="white")
leftFrame.pack(side=tkinter.LEFT, fill=tkinter.Y)


# Left Frame, Register/Login/Quit Frame
RegLogQuitFrame = tkinter.Frame(leftFrame,bg="white")
RegLogQuitFrame.pack()


registerLogin_button = tkinter.Button(RegLogQuitFrame, text= "Register/Login", command=lambda: send(""))

registerLogin_button.grid(row=1,column=1)

registerLoginName = tkinter.StringVar()  # For the login
loginEntry = tkinter.Entry(RegLogQuitFrame, textvariable=registerLoginName, width=10)
loginEntry.grid(row=1,column=2)

quit_button = tkinter.Button(RegLogQuitFrame, text= "Quit", command=lambda: send("/quit"))
quit_button.grid(row=1,column=3)
# Left Frame, Information Frame
informationLabel = tkinter.Label(leftFrame, text="Information", width=20,height=3)
informationLabel.pack()

informationFrame = tkinter.Frame(leftFrame,bg="white")
informationFrame.pack()


serverStatus_button = tkinter.Button(informationFrame, text= "Server Status", command=lambda: send("/see"))
userStatus_button = tkinter.Button(informationFrame, text= "User Status", command=lambda: send("/status"))
help_button = tkinter.Button(informationFrame, text= "Help", command=lambda: send("/command"))

serverStatus_button.grid(row=1,column=1)
userStatus_button.grid(row=1,column=2)
help_button.grid(row=1,column=3)

# Left Frame, fileTransferFrame
fileTransferLabel = tkinter.Label(leftFrame, text="File Transfer", width=20,height=3)
fileTransferLabel.pack()

fileTransferFrame = tkinter.Frame(leftFrame,bg="white")
fileTransferFrame.pack()

sendFile_button = tkinter.Button(fileTransferFrame, text= "Send File", command=lambda: send("/file"))
saveFile_button = tkinter.Button(fileTransferFrame, text= "Save File", command=lambda: send("/receive"))
sendFile_button.grid(row=1,column=1)
saveFile_button.grid(row=1,column=2)

# Left Frame, groupManagementFrame
groupManagementFrameLabel = tkinter.Label(leftFrame, text="Group Management", width=20,height=3)
groupManagementFrameLabel.pack()

groupManagementFrame = tkinter.Frame(leftFrame,bg="white")
groupManagementFrame.pack()

createGroup_button = tkinter.Button(groupManagementFrame, text= " Create Group ", command=lambda: send("/create"))
renameGroup_button = tkinter.Button(groupManagementFrame, text= "Rename Group", command=lambda: send("/rename"))
deleteGroup_button = tkinter.Button(groupManagementFrame, text= " Delete Group ", command=lambda: send("/delete"))
viewMembers_button = tkinter.Button(groupManagementFrame, text= "View Members", command=lambda: send("/members"))
addMembers_button = tkinter.Button(groupManagementFrame, text= "Add Members ", command=lambda: send("/add"))
removeMembers_button = tkinter.Button(groupManagementFrame, text= "Remove Members", command=lambda: send("/remove"))
announce_button = tkinter.Button(groupManagementFrame, text= "  Announce  ", command=lambda: send("/all"))
joinGroup_button = tkinter.Button(groupManagementFrame, text= "  Join Group  ", command=lambda: send("/join"))
leaveGroup_button = tkinter.Button(groupManagementFrame, text= " Leave Group  ", command=lambda: send("/leave"))

createGroup_button.grid(row=1,column=1)
renameGroup_button.grid(row=1,column=2)
deleteGroup_button.grid(row=1,column=3)
viewMembers_button.grid(row=2,column=1)
addMembers_button.grid(row=2,column=2)
removeMembers_button.grid(row=2,column=3)
announce_button.grid(row=3,column=1)
joinGroup_button.grid(row=3,column=2)
leaveGroup_button.grid(row=3,column=3)

top.protocol("WM_DELETE_WINDOW", handleExitProtocol)


clientSocketIPv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
addressIPv6 = (localIPv6, portIPv6)
clientSocketIPv6.connect(addressIPv6)

def main():
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution

if __name__ == "__main__":
    main()