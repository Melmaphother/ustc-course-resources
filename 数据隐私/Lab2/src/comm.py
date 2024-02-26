import pickle
import socket
import struct


class ActiveSocket:
    def __init__(self, active_ip, active_port):
        self.active_ip = active_ip
        self.active_port = active_port

        sock_daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_daemon.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_daemon.bind((self.active_ip, self.active_port))
        sock_daemon.listen(1)

        self.sock_daemon = sock_daemon

        print(f"Waiting for passive party to connect...")
        conn, addr = self.sock_daemon.accept()
        messenger = _Messenger(conn=conn)
        messenger.set_ip_port(active_ip, active_port, passive_ip=addr[0])
        assert messenger.recv() is True
        self.messenger = messenger
        print(f"Accept connection from {addr}")

    def get_messenger(self):
        return self.messenger

    def close(self):
        self.messenger.close()
        self.sock_daemon.close()


class PassiveSocket:
    def __init__(self, active_ip, active_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((active_ip, active_port))
        messenger = _Messenger(conn=sock)
        self_ip = sock.getsockname()[0]
        print(f"self_ip is: {self_ip}")
        messenger.set_ip_port(active_ip, active_port, passive_ip=self_ip)
        messenger.send(True)

        self.messenger = messenger

    def get_messenger(self):
        return self.messenger

    def close(self):
        self.messenger.close()


class _Messenger:
    def __init__(self, conn):
        self.conn = conn

    def close(self):
        self.conn.close()

    def set_ip_port(self, active_ip, active_port, passive_ip):
        self.active_ip = active_ip
        self.active_port = active_port
        self.passive_ip = passive_ip

    def send(self, msg):
        msg_binary = pickle.dumps(msg)
        msglen_prefix = _Messenger._msglen_prefix(len(msg_binary))
        msg_send = msglen_prefix + msg_binary
        self.conn.sendall(msg_send)

    def recv(self):
        msglen = self._recv_prefixes()
        binary_data = self._recvall(msglen)
        msg = pickle.loads(binary_data)
        return msg

    @staticmethod
    def _msglen_prefix(msg_len):
        """Prefix each message with its length

        Args:
            msg_len: length of binary message
            '>I': `>` means Big Endian(networking order), `I` means 4
                 bytes unsigned integer

        Returns:
            4 bytes data representing length of a binary message, so maximum
            message size if 4GB
        """
        try:
            pack = struct.pack(">I", msg_len)
            return pack
        except Exception:
            raise RuntimeError(
                "The maximum length of a single message is 4GB, please consider"
                " splitting the message and sending it multiple times"
            )

    def _recv_prefixes(self):
        # The first 4 bytes indicate the message length
        raw_msglen = self._recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]  # unpack always returns a tuple

        return msglen

    def _recvall(self, n_bytes):
        """Receive specific number of bytes from socket connection.

        Args:
            n_bytes: number of bytes to be received.

        Returns:
            Raw data which is a bytearray.
        """
        raw_data = bytearray()
        while len(raw_data) < n_bytes:
            packet = self.conn.recv(n_bytes - len(raw_data))
            if not packet:
                break
            raw_data.extend(packet)

        return raw_data
