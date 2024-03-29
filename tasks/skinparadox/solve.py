import subprocess


def generate_purplesyringa_key(token):
    arr = [ord(c) for c in token]
    for x in range(999, 0, -1):
        i = (x * 743893 >> 16) % 16
        j = (x * 433 >> 4) % 16
        if i != j:
            arr[i] = (arr[i] - arr[j]) % 256
    for i in range(16):
        arr[i] = arr[i] or 256
    for i in range(15, 0, -1):
        arr[i] = arr[i] * pow(arr[i - 1], -1, 257) % 257
    for i in range(16):
        arr[i] = arr[i] % 256
    return arr


token = input("Token: ")
purplesyringa_key = bytes(generate_purplesyringa_key(token)).hex()

subprocess.run(["attachments/keygen"], input=f"{token}\n{purplesyringa_key}\n".encode())
