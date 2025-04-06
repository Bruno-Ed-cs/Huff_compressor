"""
Para os arquivos compactados o padrao é o seguinte:
um header seguido da sequencia encriptada

header:
4 bytes --------- 4 bytes --------- histograma de frequencia -------- conteudo
^                 ^                                    ^
|                 |                                    |    
tamanho do header |                                    quatro bytes para o caracter
em bytes          |                                    quatro bytes para a frequencia
                  quantidade de bits do                nesta ordem
                  conteudo sem contar com
                  os bits de sobra do final
"""

from numpy._core.multiarray import unpackbits
from numpy._core.numerictypes import uint32
from encoding import *
import numpy as np


def construct_header(encoding_length: np.uint32, frequency_array: list) -> bytearray:

    header = bytearray()
    header.extend(encoding_length.tobytes())

    for char, freq in frequency_array:
        en_char = np.uint32(ord(char))
        en_freq = np.uint32(freq)

        header.extend(en_char.tobytes())
        header.extend(en_freq.tobytes())

    size = np.uint32(len(header) + 4)

    final = bytearray(size.tobytes()) + header

#    print(size)
#    print(final)

    return final

def read_header(encrypted_text: bytearray) -> dict:

    header_size = np.frombuffer(encrypted_text[0:4], dtype=np.uint32)[0]

    # Read content_size (next 4 bytes)
    content_size = np.frombuffer(encrypted_text[4:8], dtype=np.uint32)[0]    

#    print(header_size)
#    print(content_size)

    frequency_array = []

    for i in range(8, header_size, 8):

        char = str(bytearray(encrypted_text[i:i+4]), "utf-8", errors="replace").strip("\x00")

        freq = np.frombuffer(encrypted_text[i+4:i+8], dtype=np.uint32)[0]

        frequency_array.append([char, int(freq)])


    return {
        "header_size" : header_size,
        "content_size" : content_size,
        "frequency_array" : frequency_array
    }

def compress_file(file_path: str, destination_folder: str = "./"):
    file = open(file_path, "r")

    file_name = file.name

    file_string = file.read()

    frequency_array = char_counter(file_string)

    tree = generate_tree(frequency_array)

    encoded = encode(file_string, tree)

    header = construct_header(np.uint32(len(encoded)), frequency_array)

    body = bytearray(np.packbits(encoded))

    compressed = header + body

    file = open(destination_folder + file_name.removesuffix(".txt") + ".huff", "wb")

    file.write(compressed)

    file.close()

def decompress_file(file_path: str, destination_folder: str = "./"):

    file = open(file_path, "rb")

    file_name = file.name

    file_bytes = bytearray(file.read())

    info = read_header(file_bytes)
    header_size = info["header_size"]
    body_size = info["content_size"]
    frequency_array = info["frequency_array"]

    unpacked_bits = np.frombuffer(file_bytes[header_size:], np.uint8)
    file_bits = np.unpackbits(unpacked_bits)[:body_size]

    text = decode(generate_tree(frequency_array), file_bits)

    file.close()

    file = open(destination_folder + file_name.removesuffix(".huff") + "(decoded)" + ".txt", "w")

    file.write(text)

    file.close()

