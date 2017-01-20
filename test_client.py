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
        msg = SHUTDOWN_MSG
        peer.send(0, enet.Packet(msg))
        host.service(0)
        peer.disconnect()

    print("%s: OUT: %r" % (peer.address, msg))


# Part of the test to do with intercept callback and socket.send
peer = host.connect(enet.Address(b"localhost", 54301), 1)

def receive_callback(address, data):
    if data != b"\xff\xff\xff\xffstatusResponse\n":
        # error messages are not propagating
        # through cython
        print("data != statusResponse")
        assert(False)

    # if the test gets to this point, it means it has passed. Disconnect is a clean up
    msg = SHUTDOWN_MSG
    peer.send(0, enet.Packet(msg))
    host.service(0)
    peer.disconnect()
    host.intercept = None

run = True
while run:
    event = host.service(1000)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: CONNECT" % event.peer.address)
        msg = os.urandom(40)
        packet = enet.Packet(msg)
        peer.send(0, packet)

        host.intercept = receive_callback
    elif event.type == enet.EVENT_TYPE_DISCONNECT:
        print("%s: DISCONNECT" % event.peer.address)
        run = False
        continue
    elif event.type == enet.EVENT_TYPE_RECEIVE:
        print("%s: IN:  %r" % (event.peer.address, event.packet.data))
        continue

    host.socket.send(peer.address, b"\xff\xff\xff\xffgetstatus\x00")
