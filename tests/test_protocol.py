from shared.protocol import Message


def test_protocol():
    msg1 = Message(0, 1, 2)
    print(msg1)
    bytes1 = msg1.to_bytes()
    print(bytes1)
    msg2 = Message.from_bytes(bytes1)
    print(msg2)


if __name__ == "__main__":
    test_protocol()
