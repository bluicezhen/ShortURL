_CS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-"


def encode(n: int):
    n_2 = bin(n)[2:]
    n_64 = ""
    for i in range(len(n_2), -1, -6):
        n_64 = _CS[int(n_2[i - 5 if i - 5 >= 0 else 0:i], 2)] + n_64
    return n_64


def decode(ss: str):
    n_2 = ""
    for s in ss:
        t = bin(_CS.index(s))[2:]
        for i in range(6 - len(t)):
            t = "0" + t
        n_2 = n_2 + t
    return int(n_2, 2)


if __name__ == "__main__":
    encode(4096)
    decode("100")
