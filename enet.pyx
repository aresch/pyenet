import atexit

from cpython cimport bool

cdef extern from "enet/types.h":
    ctypedef unsigned char enet_uint8
    ctypedef unsigned short enet_uint16
    ctypedef unsigned int enet_uint32
    ctypedef unsigned int size_t

cdef extern from "enet/enet.h":

    ctypedef enet_uint32 ENetVersion

    cdef enum:
        ENET_HOST_ANY = 0
        ENET_HOST_BROADCAST = 0xFFFFFFFF
        ENET_PORT_ANY = 0

    ctypedef int ENetSocket

    ctypedef struct ENetAddress:
        enet_uint32 host
        enet_uint16 port

    ctypedef enum ENetPacketFlag:
        ENET_PACKET_FLAG_RELIABLE = (1 << 0)
        ENET_PACKET_FLAG_UNSEQUENCED = (1 << 1)
        ENET_PACKET_FLAG_NO_ALLOCATE = (1 << 2)

    ctypedef struct ENetPacket:
        size_t referenceCount
        enet_uint32 flags
        enet_uint8 *data
        size_t dataLength

    ctypedef enum ENetPeerState:
        ENET_PEER_STATE_DISCONNECTED = 0
        ENET_PEER_STATE_CONNECTING = 1
        ENET_PEER_STATE_ACKNOWLEDGING_CONNECT = 2
        ENET_PEER_STATE_CONNECTION_PENDING = 3
        ENET_PEER_STATE_CONNECTION_SUCCEEDED = 4
        ENET_PEER_STATE_CONNECTED = 5
        ENET_PEER_STATE_DISCONNECT_LATER = 6
        ENET_PEER_STATE_DISCONNECTING = 7
        ENET_PEER_STATE_ACKNOWLEDGING_DISCONNECT = 8
        ENET_PEER_STATE_ZOMBIE = 9

    ctypedef struct ENetPeer:
        ENetAddress address
        ENetPeerState state
        enet_uint32 packetLoss
        enet_uint32 packetThrottleAcceleration
        enet_uint32 packetThrottleDeceleration
        enet_uint32 packetThrottleInterval
        enet_uint32 roundTripTime
        enet_uint16 incomingPeerID
        enet_uint16 outgoingPeerID
        char *data

    ctypedef struct ENetHost:
        ENetSocket socket
        ENetAddress address

    ctypedef enum ENetEventType:
        ENET_EVENT_TYPE_NONE = 0
        ENET_EVENT_TYPE_CONNECT = 1
        ENET_EVENT_TYPE_DISCONNECT = 2
        ENET_EVENT_TYPE_RECEIVE = 3

    ctypedef struct ENetEvent:
        ENetEventType type
        ENetPeer *peer
        enet_uint8 channelID
        enet_uint32 data
        ENetPacket *packet

    # Initalization
    int enet_initialize()
    void enet_deinitialize()

    # Address functions
    int enet_address_set_host(ENetAddress *address, char *hostName)
    int enet_address_get_host_ip(ENetAddress *address, char *hostName, size_t nameLength)
    int enet_address_get_host(ENetAddress *address, char *hostName, size_t nameLength)

    # Packet functions
    ENetPacket* enet_packet_create(char *dataContents, size_t dataLength, enet_uint32 flags)
    void enet_packet_destroy(ENetPacket *packet)
    int  enet_packet_resize(ENetPacket *packet, size_t dataLength)

    # Host functions
    ENetHost* enet_host_create(ENetAddress *address, size_t peerCount, size_t channelLimit, enet_uint32 incomingBandwidth, enet_uint32 outgoingBandwidth)
    void enet_host_destroy(ENetHost *host)
    ENetPeer* enet_host_connect(ENetHost *host, ENetAddress *address, size_t channelCount, enet_uint32 data)
    int enet_host_check_events(ENetHost *host, ENetEvent *event)
    int enet_host_service(ENetHost *host, ENetEvent *event, enet_uint32 timeout)
    void enet_host_flush(ENetHost *host)
    void enet_host_broadcast(ENetHost *host, enet_uint8 channelID, ENetPacket *packet)
    void enet_host_channel_limit(ENetHost *host, size_t channelLimit)
    void enet_host_bandwidth_limit(ENetHost *host, enet_uint32 incomingBandwidth, enet_uint32 outgoingBandwidth)

    int enet_peer_send(ENetPeer *peer, enet_uint8 channelID, ENetPacket *packet)
    ENetPacket* enet_peer_receive(ENetPeer *peer, enet_uint8 *channelID)
    void enet_peer_ping(ENetPeer *peer)
    void enet_peer_reset(ENetPeer *peer)
    void enet_peer_disconnect(ENetPeer *peer, enet_uint32 data)
    void enet_peer_disconnect_now(ENetPeer *peer, enet_uint32 data)
    void enet_peer_disconnect_later(ENetPeer *peer, enet_uint32 data)
    void enet_peer_throttle_configure(ENetPeer *peer, enet_uint32 interval, enet_uint32 acceleration, enet_uint32 deacceleration)

cdef enum:
    MAXHOSTNAME = 257

PACKET_FLAG_RELIABLE = ENET_PACKET_FLAG_RELIABLE
PACKET_FLAG_UNSEQUENCED = ENET_PACKET_FLAG_UNSEQUENCED
PACKET_FLAG_NO_ALLOCATE = ENET_PACKET_FLAG_NO_ALLOCATE

EVENT_TYPE_NONE = ENET_EVENT_TYPE_NONE
EVENT_TYPE_CONNECT = ENET_EVENT_TYPE_CONNECT
EVENT_TYPE_DISCONNECT = ENET_EVENT_TYPE_DISCONNECT
EVENT_TYPE_RECEIVE = ENET_EVENT_TYPE_RECEIVE

PEER_STATE_DISCONNECTED = ENET_PEER_STATE_DISCONNECTED
PEER_STATE_CONNECTING = ENET_PEER_STATE_CONNECTING
PEER_STATE_ACKNOWLEDGING_CONNECT = ENET_PEER_STATE_ACKNOWLEDGING_CONNECT
PEER_STATE_CONNECTION_PENDING = ENET_PEER_STATE_CONNECTION_PENDING
PEER_STATE_CONNECTION_SUCCEEDED = ENET_PEER_STATE_CONNECTION_SUCCEEDED
PEER_STATE_CONNECTED = ENET_PEER_STATE_CONNECTED
PEER_STATE_DISCONNECT_LATER = ENET_PEER_STATE_DISCONNECT_LATER
PEER_STATE_DISCONNECTING = ENET_PEER_STATE_DISCONNECTING
PEER_STATE_ACKNOWLEDGING_DISCONNECT = ENET_PEER_STATE_ACKNOWLEDGING_DISCONNECT
PEER_STATE_ZOMBIE = ENET_PEER_STATE_ZOMBIE

cdef class Socket:
    """
    Socket (int socket)

    DESCRIPTION

        An ENet socket.

        Can be used with select and poll.
    """

    cdef ENetSocket _enet_socket

    def fileno(self):
        return self._enet_socket

cdef class Address:
    """
    Address (str address, int port)

    ATTRIBUTES

        str host    Hostname referred to by the Address.
        int port    Port referred to by the Address.

    DESCRIPTION

        An ENet address and port pair.

        When instantiated, performs a resolution upon 'address'. However, if
        'address' is None, enet.HOST_ANY is assumed.
    """

    cdef ENetAddress _enet_address

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __str__(self):
        return "%s:%u" % (self.host, self.port)

    def __richcmp__(self, obj, op):
        if isinstance(obj, Address):
            if op == 2:
                # This is a '==' operation
                return (obj.host == self.host) and (obj.port == self.port)
            elif op == 3:
                # This is a '!=' operation
                return (obj.host != self.host) or (obj.port != self.port)

        raise NotImplementedError

    property host:
        def __get__(self):
            cdef char host[MAXHOSTNAME]

            if self._enet_address.host == ENET_HOST_ANY:
                return "*"
            elif self._enet_address.host:
                if enet_address_get_host_ip(&self._enet_address, host, MAXHOSTNAME):
                    raise IOError("Resolution failure!")
                return host

        def __set__(self, value):
            if not value or value == "*":
                self._enet_address.host = ENET_HOST_ANY
            else:
                if enet_address_set_host(&self._enet_address, value):
                    raise IOError("Resolution failure!")

    property hostname:
        def __get__(self):
            cdef char host[MAXHOSTNAME]

            if self._enet_address.host == ENET_HOST_ANY:
                return "*"
            elif self._enet_address.host:
                if enet_address_get_host(&self._enet_address, host, MAXHOSTNAME):
                    raise IOError("Resolution failure!")
                return host

    property port:
        def __get__(self):
            return self._enet_address.port

        def __set__(self, value):
            self._enet_address.port = value

cdef class Packet:
    """
    Packet (str dataContents, int flags)

    ATTRIBUTES

        str data        Contains the data for the packet.
        int flags       Flags modifying delivery of the Packet:

            enet.PACKET_FLAG_RELIABLE Packet must be received by the target peer
                                      and resend attempts should be made until
                                      the packet is delivered.

            enet.PACKET_FLAG_UNSEQUENCED Packet will not be sequenced with other
                                         packets not supported for reliable
                                         packets.

            enet.PACKET_FLAG_NO_ALLOCATE Packet will not allocate data and user
                                         must supply it instead.

    DESCRIPTION

        An ENet data packet that may be sent to or received from a peer.

    """

    cdef ENetPacket *_enet_packet
    cdef bool sent

    def __init__(self, data=None, flags=0):
        if data is not None:
            self._enet_packet = enet_packet_create(data, len(data), flags)

        # This will get set to True when a peer.send() is called with the Packet
        # to ensure we don't try to destroy this packet as ENET will handle that
        # for us.
        self.sent = False

    def __dealloc__(self):
        if self.is_valid() and not self.sent:
            enet_packet_destroy(self._enet_packet)

    def is_valid(self):
        if self._enet_packet:
            return True
        else:
            return False

    property data:
        def __get__(self):
            if self.is_valid():
                return (<char *>self._enet_packet.data)[:self._enet_packet.dataLength]
            else:
                raise MemoryError("Packet has not been initiliazed properly!")

    property dataLength:
        def __get__(self):
            if self.is_valid():
                return self._enet_packet.dataLength
            else:
                raise MemoryError("Packet has not been initiliazed properly!")

    property flags:
        def __get__(self):
            if self.is_valid():
                return self._enet_packet.flags
            else:
                raise MemoryError("Packet has not been initiliazed properly!")

    property sent:
        def __get__(self):
            return self.sent
        def __set__(self, value):
            self.sent = value

cdef class Peer:
    """
    Peer ()

    ATTRIBUTES

        Address address
        int     state       The peer's current state which is one of
                            enet.PEER_STATE_*
        int     packetLoss  Mean packet loss of reliable packets as a ratio with
                            respect to the constant enet.PEER_PACKET_LOSS_SCALE.
        int     packetThrottleAcceleration
        int     packetThrottleDeceleration
        int     packetThrottleInterval
        int     roundTripTime Mean round trip time (RTT), in milliseconds,
                              between sending a reliable packet and receiving
                              its acknowledgement.
        int     incomingPeerID

    DESCRIPTION

        An ENet peer which data packets may be sent or received from.

        This class should never be instantiated directly, but rather via
        enet.Host.connect or enet.Event.Peer.  If you try to access any members
        of a Peer without being properly instantiated from a Host or Event
        object then a MemoryError will be raised.

    """

    cdef ENetPeer *_enet_peer

    def __richcmp__(self, obj, op):
        if isinstance(obj, Peer):
            if op == 2:
                return self.address == obj.address
            elif op == 3:
                return self.address != obj.address
        raise NotImplementedError

    def send(self, channelID, Packet packet):
        """
        send (int channelID, Packet packet)

        Queues a packet to be sent.

        returns 0 on sucess, < 0 on failure
        """

        if self.check_valid() and packet.is_valid():
            packet.sent = True
            return enet_peer_send(self._enet_peer, channelID, packet._enet_packet)

    def receive(self, unsigned char channelID):
        """
        receive (int channelID)

        Attempts to dequeue any incoming queued packet.
        """

        if self.check_valid():
            packet = Packet()
            (<Packet> packet)._enet_packet = enet_peer_receive(self._enet_peer, &channelID)

            if packet._enet_packet:
                return packet
            else:
                return None

    def reset(self):
        """
        reset ()

        Forcefully disconnects a peer.
        """

        if self.check_valid():
            enet_peer_reset(self._enet_peer)

    def ping(self):
        """
        ping ()

        Sends a ping request to a peer.
        """

        if self.check_valid():
            enet_peer_ping(self._enet_peer)

    def disconnect(self):
        """
        disconnect ()

        Request a disconnection from a peer.
        """

        if self.check_valid():
            enet_peer_disconnect(self._enet_peer, 0)

    def disconnect_later(self):
        """
        disconnect_later ()

        Request a disconnection from a peer, but only after all queued outgoing
        packets are sent.
        """

        if self.check_valid():
            enet_peer_disconnect_later(self._enet_peer, 0)

    def check_valid(self):
        """
        check_valid ()

        Returns True if there is a valid enet_peer set
        Raises a Memory error if not

        """
        if self._enet_peer:
            return True
        else:
            raise MemoryError("Empty Peer object accessed!")

    property address:
        def __get__(self):
            if self.check_valid():
                a = Address(None, 0)
                (<Address> a)._enet_address = self._enet_peer.address
                return a

    property state:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.state

    property packetLoss:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.packetLoss

    property packetThrottleInterval:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.packetThrottleInterval

        def __set__(self, value):
            if self.check_valid():
                enet_peer_throttle_configure(
                    self._enet_peer, value, self.packetThrottleAcceleration,
                    self.packetThrottleDeceleration)

    property packetThrottleAcceleration:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.packetThrottleAcceleration

        def __set__(self, value):
            if self.check_valid():
                enet_peer_throttle_configure(self._enet_peer,
                    self.packetThrottleInterval, value,
                    self.packetThrottleDeceleration)

    property packetThrottleDeceleration:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.packetThrottleDeceleration

        def __set__(self, value):
            if self.check_valid():
                enet_peer_throttle_configure(self._enet_peer,
                    self.packetThrottleInterval,
                    self.packetThrottleAcceleration, value)

    property roundTripTime:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.roundTripTime

    property incomingPeerID:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.incomingPeerID

    property data:
        def __get__(self):
            if self.check_valid():
                return self._enet_peer.data

        def __set__(self, value):
            if self.check_valid():
                self._enet_peer.data = value

cdef class Event:
    """
    Event ()

    ATTRIBUTES

        int     type        Type of the event.  Will be enet.EVENT_TYPE_*.
        Peer    peer        Peer that generated the event.
        int     channelID
        Packet  packet

    DESCRIPTION

        An ENet event as returned by enet.Host.service.

        This class should never be instantiated directly.
    """

    cdef ENetEvent _enet_event
    cdef Packet _packet

    def __init__(self):
        self._packet = None

    property type:
        def __get__(self):
            return self._enet_event.type

    property peer:
        def __get__(self):
            peer = Peer()
            (<Peer> peer)._enet_peer = self._enet_event.peer
            return peer

    property channelID:
        def __get__(self):
            return self._enet_event.channelID

    property packet:
        def __get__(self):
            if not self._packet:
                self._packet = Packet()
                (<Packet> self._packet)._enet_packet = self._enet_event.packet
            return self._packet

cdef class Host:
    """
    Host (Address address, int peerCount, int channelLimit,
        int incomingBandwidth, int outgoingBandwidth)

    ATTRIBUTES

        Address address             Internet address of the host.
        Socket  socket              The socket the host services.
        int     incomingBandwidth   Downstream bandwidth of the host.
        int     outgoingBandwidth   Upstream bandwidth of the host.

    DESCRIPTION

        An ENet host for communicating with peers.

        If 'address' is None, then the Host will be client only.
    """

    cdef ENetHost *_enet_host
    cdef enet_uint32 _enet_incomingBandwidth
    cdef enet_uint32 _enet_outgoingBandwidth

    def __init__ (self, Address address=None, peerCount=0, channelLimit=0,
        incomingBandwidth=0, outgoingBandwidth=0):

        (self._enet_incomingBandwidth, self._enet_outgoingBandwidth) = (incomingBandwidth, outgoingBandwidth)

        if address:
            self._enet_host = enet_host_create(&address._enet_address, peerCount, channelLimit, incomingBandwidth, outgoingBandwidth)
        else:
            self._enet_host = enet_host_create(NULL, peerCount, channelLimit, incomingBandwidth, outgoingBandwidth)

        if not self._enet_host:
            raise MemoryError("Unable to create host structure!")

    def __dealloc__(self):
        if self._enet_host:
            enet_host_destroy(self._enet_host)

    def connect(self, Address address, channelCount, data=0):
        """
        Peer connect (Address address, int channelCount, int data)

        Initiates a connection to a foreign host and returns a Peer.
        """

        if self._enet_host:
            peer = Peer()
            (<Peer> peer)._enet_peer = enet_host_connect(
                self._enet_host, &address._enet_address, channelCount, data)

            if not (<Peer> peer)._enet_peer:
                raise IOError("Connection failure!")

            return peer

    def service(self, timeout):
        """
        Event service (int timeout)

        Waits for events on the host specified and shuttles packets between
        the host and its peers. The timeout is in milliseconds.
        """

        if self._enet_host:
            event = Event()
            result = enet_host_service(
                self._enet_host, &(<Event> event)._enet_event, timeout)

            if result < 0:
                raise IOError("Servicing error - probably disconnected.")
            else:
                return event

    def flush(self):
        """
        flush ()

        Sends any queued packets on the host specified to its designated peers.
        """

        if self._enet_host:
            enet_host_flush(self._enet_host)

    def broadcast(self, channelID, Packet packet):
        """
        broadcast (int channelID, Packet packet)

        Queues a packet to be sent to all peers associated with the host.
        """

        if self._enet_host:
            if packet.is_valid():
                packet.sent = True
                enet_host_broadcast(self._enet_host, channelID, packet._enet_packet)

    property address:
        def __get__(self):
            if self._enet_host:
                a = Address(None, 0)
                (<Address> a)._enet_address = self._enet_host.address
                return a

    property incomingBandwidth:
        def __get__(self):
            return self._enet_incomingBandwidth

        def __set__(self, value):
            self._enet_incomingBandwidth = value
            enet_host_bandwidth_limit(self._enet_host,
                self._enet_incomingBandwidth, self._enet_outgoingBandwidth)

    property outgoingBandwidth:
        def __get__(self):
            return self._enet_outgoingBandwidth

        def __set__(self, value):
            self._enet_outgoingBandwidth = value
            enet_host_bandwidth_limit(self._enet_host,
                self._enet_incomingBandwidth, self._enet_outgoingBandwidth)

    property socket:
        def __get__(self):
            socket = Socket()
            (<Socket> socket)._enet_socket = self._enet_host.socket
            return socket

def _enet_atexit():
    enet_deinitialize()

enet_initialize()
atexit.register(_enet_atexit)
