# this function takes a string message as a parameter,
# performs Run Length Encoding on the string,
# and returns a new string representing the compressed message.
def RLE_compress(message: str) -> None:
    compressed = ""
    i = 0
    while i < len(message):
        count = 1
        while i + count < len(message) and message[i + count] == message[i]:
            count += 1
        compressed += message[i] + str(count)
        i += count

    return compressed


def RLE_decompress(message: str) -> None:
    decompressed = ""
    i = 0
    while i < len(message):
        char = message[i]
        i += 1
        j = i
        while j < len(message) and message[j].isdigit():
            j += 1
        count = int(message[i:j])
        decompressed += char * count
        i = j
    return decompressed


print(RLE_decompress("B1R1E11A1K1 1W1E16!1"))

# TEST CODE:
print(RLE_compress("AABBBAAAABBBBBAAAAAABBBBBBB"))
print(RLE_compress("AACCCCBBBBBAAAAAAAXFFFFFFFF"))
print(RLE_compress("AACCCCBBBBBAAAAAAAXFFFFFFFFD"))
print(RLE_compress("AACCCCBBBBBAAAAAAAXFFFFFFFFDD"))
print(RLE_compress("AACCCCBBBBBAAAAAAAXFFFFFFFFDDD"))
print(
    RLE_compress("ABCDEF")
)  # as discussed, this one doesn't actually "compress", but it's a good test case
print(RLE_compress("FFFFFFFFFFFFFFFFFFF"))
print(RLE_compress("F"))
print(RLE_compress("F????"))
print(RLE_compress("Mmmmmmmmmm sooooo goooooood!"))
print(RLE_compress("Booooooooooooo, hisssssssss"))
