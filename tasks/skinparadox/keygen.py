import sys


def validate_purplesyringa_key(token, arr):
    if len(arr) != 16:
        return False
    for i in range(16):
        arr[i] = arr[i] or 256
    for i in range(1, 16):
        arr[i] = arr[i] * arr[i - 1] % 257
    for x in range(1, 1000):
        i = (x * 743893 >> 16) % 16
        j = (x * 433 >> 4) % 16
        if i != j:
            arr[i] = (arr[i] + arr[j]) % 256
    for i in range(16):
        if arr[i] != ord(token[i]):
            return False
    return True


def generate_ucucuga_key(token, purplesyringa_key):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
    for c in purplesyringa_key:
        i = c % len(token)
        tmp = token[i:] + token[:i]
        token = ""
        for i in range(len(tmp)):
            token += ALPHABET[(sum(map(ord, tmp[:i + 1])) + i) % len(ALPHABET)]
    return token


def parse_hex(s):
    if len(s) % 2 != 0:
        print("Invalid hex format")
        sys.exit(0)
    return [
        "0123456789abcdef".find(s[i]) * 16 + "0123456789abcdef".find(s[i + 1])
        for i in range(0, len(s), 2)
    ]


def main():
    print("UCUCUGA PRO KEYGEN by xXx_HACKERNAME_xXx")

    print("Enter token: ", end="")
    sys.stdout.flush()
    token = input()

    print("You need to obtain a key from me to use this keygen.")
    print("Please mail purplesyringa@example.com. We will agree on the payment.")
    print("Enter key from purplesyringa: ", end="")
    sys.stdout.flush()
    purplesyringa_key = parse_hex(input())

    if validate_purplesyringa_key(token, purplesyringa_key[:]):
        ucucuga_key = generate_ucucuga_key(token, purplesyringa_key)
        print("UCUCUGA Pro key: " + ucucuga_key)
    else:
        print("The key is invalid.")


main()
