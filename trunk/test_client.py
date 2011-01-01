import enet
from hashlib import sha1
import random

SHUTDOWN_MSG = "SHUTDOWN"
MSG_NUMBER = 10

host = enet.Host(None, 1, 0, 0, 0)
peer = host.connect(enet.Address("localhost", 54301), 1)

counter = 0
run = True
while run:
    event = host.service(1000)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print "%s: CONNECT" % event.peer.address
    elif event.type == enet.EVENT_TYPE_DISCONNECT:
        print "%s: DISCONNECT" % event.peer.address
        run = False
        continue
    elif event.type == enet.EVENT_TYPE_RECEIVE:
        print "%s: IN:  %r" % (event.peer.address, event.packet.data)
        continue
    msg = sha1(str(random.random())).hexdigest()
    packet = enet.Packet(msg)
    peer.send(0, packet)

    counter += 1
    if counter >= MSG_NUMBER:
        msg = SHUTDOWN_MSG
        peer.send(0, enet.Packet(msg))
        host.service(0)
        peer.disconnect()

    print "%s: OUT: %r" % (peer.address, msg)
