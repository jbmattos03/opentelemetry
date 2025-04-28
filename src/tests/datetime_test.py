import datetime

def test_datetime():
    print(f"{datetime.datetime.now()}")
    print(f"{datetime.datetime.now().isoformat()}")
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}")



if __name__ == "__main__":
    test_datetime()