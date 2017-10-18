_CS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-"


def encode(n: int):
    def _cal(s: str):
        c = _CS[int(s[len(s) - 6:len(s)], 2)]
        if len(s) > 6:
            return _cal(s[0:len(s) - 6]) + c
        return c

    n_2 = bin(n)[2:]
    return _cal(n_2)


def decode(ss: str):
    n_2 = ""
    for s in ss:
        t = bin(_CS.index(s))[2:]
        for i in range(6 - len(t)):
            t = "0" + t
        n_2 = n_2 + t
    return int(n_2, 2)


if __name__ == "__main__":
    print(encode(128))
    print(decode("1-"))
