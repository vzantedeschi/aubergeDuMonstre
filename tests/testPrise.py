import socket

hote = '134.214.106.23'
port = 5000

syncBytes = "A55A"
h_seq_length = "6B"
org = "05"
dataBytes = "70000000"
idBytes = "FF9F1E04"
status = "30"
checksum = hex(int(org,16)+int(status,16)+int(h_seq_length,16)+int(idBytes[0:2],16)+int(idBytes[2:4],16)+int(idBytes[4:6],16)+int(idBytes[6:8],16) + int(dataBytes[0:2],16))

checksum = checksum[3:5].upper()
trame = syncBytes + h_seq_length + org + dataBytes + idBytes + status + checksum
print trame
connexionProxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexionProxy.connect((hote,port))

trame = trame.encode()
connexionProxy.send(trame)


connexionProxy.close()
