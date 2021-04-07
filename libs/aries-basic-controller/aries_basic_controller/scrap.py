wallet_id = "1234"
empty_id = ""

def checker(wallet_id):
    try:
        if not wallet_id:
            raise TypeError("Empty string")
        print(wallet_id)
    except TypeError as err:
        print(err)

def other(wallet_id):
    if not wallet_id:
            raise TypeError("Empty string")
    print(wallet_id)

other(wallet_id)
other(empty_id)