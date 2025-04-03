import numpy as np

string = "Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream. Let us understand prefix codes with a counter example. Let there be four characters a, b, c and d, and their corresponding variable length codes be 00, 01, 0 and 1. This coding leads to ambiguity because code assigned to c is the prefix of codes assigned to a and b. If the compressed bit stream is 0001, the de-compressed output may be “cccd” or “ccb” or “acd” or “ab”."

def char_counter(string):
    
    total = 0
    frequencies = []
    for char in string:
        total += 1

        if not any(char in tup for tup in frequencies):
            frequencies.append([char, 1])

        else:
            for tup in frequencies:
                if tup[0] == char:
                    tup[1] += 1
                    break

    frequencies.sort(key = lambda tup : tup[1])

    return frequencies
        
num =    np.uint8(255)
bits = bin(num) 

print(f"Numero original = {num}")
print(f"Valor em binário = {bits}")
print(f"histograma = {char_counter(string)}")
                    

