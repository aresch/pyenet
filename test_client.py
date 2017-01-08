import enet
import os

SHUTDOWN_MSG = b"SHUTDOWN"
MSG_NUMBER = 10

host = enet.Host(None, 1, 0, 0, 0)
peer = host.connect(enet.Address(b"localhost", 54301), 1)

counter = 0
run = True
while run:
    event = host.service(1000)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: CONNECT" % event.peer.address)
    elif event.type == enet.EVENT_TYPE_DISCONNECT:
        print("%s: DISCONNECT" % event.peer.address)
        run = False
        continue
    elif event.type == enet.EVENT_TYPE_RECEIVE:
        print("%s: IN:  %r" % (event.peer.address, event.packet.data))
        continue

    msg = os.urandom(40)
    packet = enet.Packet(msg)
    peer.send(0, packet)

    counter += 1
    if counter >= MSG_NUMBER:
        packet = enet.Packet("SEND QUERY")
        peer.send(0, packet)
        event = host.service(1000)
        assert(event.type == enet.EVENT_TYPE_RECEIVE)
        assert(event.packet.data == "RETURN DATA")


        msg = SHUTDOWN_MSG
        peer.send(0, enet.Packet(msg))
        host.service(0)
        peer.disconnect()

    print("%s: OUT: %r" % (peer.address, msg))
