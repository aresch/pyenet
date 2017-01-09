import enet
print enet
SHUTDOWN_MSG = "SHUTDOWN"
    # else:
        # protocol.receive_callback(self, address, data)

host = enet.Host(enet.Address(b"localhost", 54301), 10, 0, 0, 0)
def receive_callback(address, data):
    print address, "%r"%data
    if data and data == "SEND QUERY":
        global host
        host.socket.send(address, "RETURN DATA")

host.intercept = receive_callback

connect_count = 0
run = True
shutdown_recv = False

# def handleQuery(self, challenge):
#     options = {'gamename' : 'Ace of Spades', 'fs_game' : 'pysnip'}
#     chall = makeValid(challenge)
#     if len(chall) > 0:
#         options['challenge'] = chall
#     options['sv_hostname'] = makeValid(self.name)
#     options['version'] = makeValid(self.server_version)
#     options['mapname'] = makeValid(self.map_info.name)
#     options['gametype'] = makeValid(self.get_mode_name())
#     options['sv_maxclients'] = self.max_players
#     players = []
#     for p in self.players.values():
#         players.append({ 'score' : p.kills, 'ping' : p.latency, 'name' : makeValid(p.name), 'team' : getTeamId(p.team.id) })
#     options['clients'] = len(players)
#     return (options, players);

while run:
    # Wait 1 second for an event
    event = host.service(1000)
    # def f(self, address, data): print(self, address, data)

    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: S CONNECT" % event.peer.address)
        connect_count += 1
    elif event.type == enet.EVENT_TYPE_DISCONNECT:
        print("%s: S DISCONNECT" % event.peer.address)
        connect_count -= 1
        if connect_count <= 0 and shutdown_recv:
            run = False
    elif event.type == enet.EVENT_TYPE_RECEIVE:
        print("%s: S IN:  %r" % (event.peer.address, event.packet.data))
        msg = event.packet.data
        if event.peer.send(0, enet.Packet(msg)) < 0:
            print("%s: S Error sending echo packet!" % event.peer.address)
        else:
            print("%s: S OUT: %r" % (event.peer.address, msg))
        if event.packet.data == "SHUTDOWN":
            shutdown_recv = True
