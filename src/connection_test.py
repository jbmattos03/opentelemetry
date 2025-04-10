import socket

def test_connection():
    s = socket.socket()

    try:
        s.connect(('localhost', 4318))
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")

test_connection()