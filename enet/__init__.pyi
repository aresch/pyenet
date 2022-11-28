from typing import Any, Callable, Union

PACKET_FLAG_RELIABLE: int
PACKET_FLAG_UNSEQUENCED: int
PACKET_FLAG_NO_ALLOCATE: int
PACKET_FLAG_UNRELIABLE_FRAGMENT: int

EVENT_TYPE_NONE: int
EVENT_TYPE_CONNECT: int
EVENT_TYPE_DISCONNECT: int
EVENT_TYPE_RECEIVE: int

PEER_STATE_DISCONNECTED: int
PEER_STATE_CONNECTING: int
PEER_STATE_ACKNOWLEDGING_CONNECT: int
PEER_STATE_CONNECTION_PENDING: int
PEER_STATE_CONNECTION_SUCCEEDED: int
PEER_STATE_CONNECTED: int
PEER_STATE_DISCONNECT_LATER: int
PEER_STATE_DISCONNECTING: int
PEER_STATE_ACKNOWLEDGING_DISCONNECT: int
PEER_STATE_ZOMBIE: int

ENET_CRC32: int

class Address:
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

    def __init__(self, host: Union[str, bytes], port: int) -> None: ...
    @property
    def host(self) -> str: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...

class Socket:
    """
    Socket (int socket)

    DESCRIPTION

        An ENet socket.

        Can be used with select and poll.
    """

    def send(self, address: Address, data: Any) -> int: ...
    def fileno(self) -> int: ...

class Packet:
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

            enet.PACKET_FLAG_UNRELIABLE_FRAGMENT Packet will be fragmented using
                                                 unreliable (instead of reliable)
                                                 sends if it exceeds the MTU...

    DESCRIPTION

        An ENet data packet that may be sent to or received from a peer.

    """

    def __init__(self, data: Union[bytes, None] = None, flags: int = 0) -> None: ...
    def is_valid(self) -> bool: ...
    @property
    def sent(self) -> bool: ...
    @property
    def data(self) -> bytes: ...
    @property
    def dataLength(self) -> int: ...
    @property
    def flags(self) -> int: ...

class Peer:
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

    def send(self, channelID: int, packet: Packet) -> int:
        """
        send (int channelID, Packet packet)

        Queues a packet to be sent.

        returns 0 on success, < 0 on failure
        """
    def receive(self, channelID: int) -> Union[Packet, None]:
        """
        receive (int channelID)

        Attempts to dequeue any incoming queued packet.
        """
    def reset(self) -> None:
        """
        reset ()

        Forcefully disconnects a peer.
        """
    def ping(self) -> None:
        """
        ping ()

        Sends a ping request to a peer.
        """
    def disconnect(self, data: int = 0) -> None:
        """
        disconnect ()

        Request a disconnection from a peer.
        """
    def disconnect_later(self, data: int = 0) -> None:
        """
        disconnect_later ()

        Request a disconnection from a peer, but only after all queued outgoing
        packets are sent.
        """
    def disconnect_now(self, data: int = 0) -> None:
        """
        disconnect_now ()

        Force an immediate disconnection from a peer.
        """
    def check_valid(self) -> bool:
        """
        check_valid ()

        Returns True if there is a valid enet_peer set
        Raises a Memory error if not

        """
    @property
    def host(self) -> Host: ...
    @property
    def outgoingPeerID(self) -> int: ...
    @property
    def incomingPeerID(self) -> int: ...
    @property
    def connectID(self) -> int: ...
    @property
    def outgoingSessionID(self) -> int: ...
    @property
    def incomingSessionID(self) -> int: ...
    @property
    def address(self) -> Address: ...
    @property
    def data(self) -> Any: ...
    @property
    def state(self) -> int: ...
    @property
    def channelCount(self) -> int: ...
    @property
    def incomingBandwidth(self) -> int: ...
    @property
    def outgoingBandwidth(self) -> int: ...
    @property
    def incomingBandwidthThrottleEpoch(self) -> int: ...
    @property
    def outgoingBandwidthThrottleEpoch(self) -> int: ...
    @property
    def incomingDataTotal(self) -> int: ...
    @property
    def outgoingDataTotal(self) -> int: ...
    @property
    def lastSendTime(self) -> int: ...
    @property
    def lastReceiveTime(self) -> int: ...
    @property
    def nextTimeout(self) -> int: ...
    @property
    def earliestTimeout(self) -> int: ...
    @property
    def packetLossEpoch(self) -> int: ...
    @property
    def packetsSent(self) -> int: ...
    @property
    def packetsLost(self) -> int: ...
    @property
    def packetLoss(self) -> int: ...
    @property
    def packetLossVariance(self) -> int: ...
    @property
    def packetThrottle(self) -> int: ...
    @property
    def packetThrottleLimit(self) -> int: ...
    @property
    def packetThrottleCounter(self) -> int: ...
    @property
    def packetThrottleEpoch(self) -> int: ...
    @property
    def packetThrottleAcceleration(self) -> int: ...
    @property
    def packetThrottleDeceleration(self) -> int: ...
    @property
    def packetThrottleInterval(self) -> int: ...
    @property
    def lastRoundTripTime(self) -> int: ...
    @property
    def lowestRoundTripTime(self) -> int: ...
    @property
    def lastRoundTripTimeVariance(self) -> int: ...
    @property
    def highestRoundTripTimeVariance(self) -> int: ...
    @property
    def roundTripTime(self) -> int: ...
    @property
    def roundTripTimeVariance(self) -> int: ...
    @property
    def mtu(self) -> int: ...
    @property
    def windowSize(self) -> int: ...
    @property
    def reliableDataInTransit(self) -> int: ...
    @property
    def outgoingReliableSequenceNumber(self) -> int: ...
    @property
    def flags(self) -> int: ...
    @property
    def incomingUnsequencedGroup(self) -> int: ...
    @property
    def outgoingUnsequencedGroup(self) -> int: ...
    @property
    def eventData(self) -> int: ...

class Event:
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

    def __init__(self) -> None: ...
    @property
    def type(self) -> int: ...
    @property
    def peer(self) -> Peer: ...
    @property
    def channelID(self) -> int: ...
    @property
    def data(self) -> int: ...
    @property
    def packet(self) -> Packet: ...

class Host:
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

    def __init__(
        self,
        address: Union[Address, None] = None,
        peerCount: int = 0,
        channelLimit: int = 0,
        incomingBandwidth: int = 0,
        outgoingBandwidth: int = 0,
    ) -> None: ...
    def connect(self, address: Address, channelCount: int, data: int = 0) -> Peer:
        """
        Peer connect (Address address, int channelCount, int data)

        Initiates a connection to a foreign host and returns a Peer.
        """
    def check_events(self) -> Event:
        """
        Checks for any queued events on the host and dispatches one if available
        """
    def service(self, timeout: int, fast_drop: bool = False) -> Event:
        """
        Event service (int timeout)

        Waits for events on the host specified and shuttles packets between
        the host and its peers. The timeout is in milliseconds.

        if fast_drop is set, None can be returned instead
        """
    def flush(self) -> None:
        """
        flush ()

        Sends any queued packets on the host specified to its designated peers.
        """
    def broadcast(self, channelID: int, packet: Packet) -> None:
        """
        broadcast (int channelID, Packet packet)

        Queues a packet to be sent to all peers associated with the host.
        """
    def compress_with_range_coder(self) -> None:
        """
        Sets the packet compressor the host should use to the default range coder
        """
    @property
    def socket(self) -> Socket: ...
    @property
    def address(self) -> Address: ...
    @property
    def incomingBandwidth(self) -> int: ...
    @property
    def outgoingBandwidth(self) -> int: ...
    @property
    def peers(self) -> list[Peer]: ...
    @property
    def peerCount(self) -> int: ...
    @property
    def channelLimit(self) -> int: ...
    @property
    def totalSentData(self) -> int: ...
    @property
    def totalSentPackets(self) -> int: ...
    @property
    def totalReceivedData(self) -> int: ...
    @property
    def totalReceivedPackets(self) -> int: ...
    @property
    def intercept(self) -> Union[Callable, None]: ...
    @property
    def checksum(self) -> int: ...
