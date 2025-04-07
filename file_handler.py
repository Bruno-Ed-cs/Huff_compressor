"""
Para os arquivos compactados o padrão é o seguinte:
um header seguido da sequência encriptada

header:
4 bytes --------- 4 bytes --------- histograma de frequência -------- conteúdo
^                 ^                                    ^
|                 |                                    |    
tamanho do header |                                    quatro bytes para o caracter
em bytes          |                                    quatro bytes para a frequência
                  quantidade de bits do                nesta ordem
                  conteúdo sem contar com
                  os bits de sobra do final
"""

from encoding import *
import numpy as np
import os

def construct_header(encoding_length: np.uint32, frequency_array: list) -> bytearray:
    """
    Constrói o cabeçalho do arquivo compactado.
    
    Args:
        encoding_length (np.uint32): Tamanho da sequência codificada em bits
        frequency_array (list): Lista de tuplas (caractere, frequência)
    
    Returns:
        bytearray: Cabeçalho pronto para ser escrito no arquivo
    """
    header = bytearray()
    header.extend(encoding_length.tobytes())

    for char, freq in frequency_array:
        en_char = np.uint32(ord(char))
        en_freq = np.uint32(freq)

        header.extend(en_char.tobytes())
        header.extend(en_freq.tobytes())

    size = np.uint32(len(header) + 4)

    final = bytearray(size.tobytes()) + header

    return final

def read_header(encrypted_text: bytearray) -> dict:
    """
    Lê e interpreta o cabeçalho de um arquivo compactado.
    
    Args:
        encrypted_text (bytearray): Bytes do arquivo compactado
    
    Returns:
        dict: Dicionário com as informações do cabeçalho:
            - header_size: Tamanho do cabeçalho
            - content_size: Tamanho do conteúdo em bits
            - frequency_array: Lista de frequências dos caracteres
    """
    header_size = np.frombuffer(encrypted_text[0:4], dtype=np.uint32)[0]
    content_size = np.frombuffer(encrypted_text[4:8], dtype=np.uint32)[0]    

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
    """
    Comprime um arquivo de texto usando codificação de Huffman.
    
    Args:
        file_path (str): Caminho do arquivo a ser comprimido
        destination_folder (str, optional): Pasta de destino. Defaults to "./".
    
    Imprime estatísticas da compressão e salva o arquivo .huff
    """
    file = open(file_path, "r")
    file_name = file.name
    initial_size = os.path.getsize(file_path)
    file_string = file.read()

    frequency_array = char_counter(file_string)

    tree = generate_tree(frequency_array)

    encoded = encode(file_string, tree)
    header = construct_header(np.uint32(len(encoded)), frequency_array)
    body = bytearray(np.packbits(encoded))
    compressed = header + body

    file.close()

    compressed_name = destination_folder + file_name.removesuffix(".txt") + ".huff"
    file = open(compressed_name, "wb")
    file.write(compressed)
    file.close()

    final_size = os.path.getsize(compressed_name)

    print(f"Histograma de frequência: {frequency_array}")
    print(f"Árvore geradora:\n{tree}")

    print(f"Tamanho original = {initial_size} bytes")
    print(f"Tamanho comprimido = {final_size} bytes")
    print(f"Taxa de compressão = {(100 - (final_size/initial_size) * 100):.2f} %")

def decompress_file(file_path: str, destination_folder: str = "./"):
    """
    Descomprime um arquivo .huff usando decodificação de Huffman.
    
    Args:
        file_path (str): Caminho do arquivo .huff
        destination_folder (str, optional): Pasta de destino. Defaults to "./".
    
    Imprime estatísticas da descompressão e salva o arquivo decodificado
    """
    file = open(file_path, "rb")
    file_name = file.name
    file_bytes = bytearray(file.read())

    info = read_header(file_bytes)
    header_size = info["header_size"]
    body_size = info["content_size"]
    frequency_array = info["frequency_array"]

    unpacked_bits = np.frombuffer(file_bytes[header_size:], np.uint8)
    file_bits = np.unpackbits(unpacked_bits)[:body_size]

    tree = generate_tree(frequency_array)
    text = decode(tree, file_bits)

    file.close()

    decompress_name = destination_folder + file_name.removesuffix(".huff") + "_decoded_" + ".txt"
    file = open(decompress_name, "w")
    file.write(text)
    file.close()

    initial_size = os.path.getsize(file_path)
    final_size = os.path.getsize(decompress_name)

    print(f"Histograma de frequência: {frequency_array}")
    print(f"Árvore geradora:\n{tree}")

    print(f"Tamanho comprimido = {initial_size} bytes")
    print(f"Tamanho final = {final_size} bytes")
    print(f"Taxa de compressão = {(100 - (initial_size/final_size) * 100):.2f} %")
