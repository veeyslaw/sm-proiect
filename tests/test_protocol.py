from shared.protocol import Command


def test_protocol():
    msg1 = Command(0, 1, 2)
    print(msg1)
    bytes1 = msg1.to_bytes()
    print(bytes1)
    msg2 = Command.from_bytes(bytes1)
    print(msg2)


if __name__ == "__main__":
    test_protocol()
