import numpy as np
import binarytree as btree

class NodeHuff(btree.Node):
    def __init__(self, char=None, weight=None):
        self.char = char
        self.value = weight
        self.left = None
        self.right = None

def encode_char(node: NodeHuff, char, sequence = None):

    """
    Funçao para codificar recursivamente um caractere
    :param node: arvore de codificação Huffman
    :param char: caractere a ser codificado
    :param sequence: array de bits a ser criado
    """
    if sequence is None:
        sequence = []

    if node.char == char:
        return sequence.copy()
    elif node.char != None and node.char != char:
        return None


    if node.left != None:
        sequence.append(0)
        seq = encode_char(node.left, char, sequence)
        if seq != None:
            return seq
        sequence.pop()

    if node.right != None:
        sequence.append(1)
        seq = encode_char(node.right, char, sequence)
        if seq != None:
            return seq
        sequence.pop()


    return None

def encode(string: str, tree: NodeHuff) -> list:

    encoded_sequence = []

    for char in string:

        sequence = encode_char(tree, char)
        if sequence is None:
            print(f"ERROR: The character '{char}' cannot be found in the encoding tree")

        else:
            encoded_sequence.extend(sequence)

    return encoded_sequence


def decode(tree: NodeHuff, code) -> str:

    """
    Função para decodificar uma sequencia de Huffman
    :param tree: arvore codificadora da sequencia
    :param code: sequencia de bits codificado
    """

    root = tree
    text = ""

    for bit in code:
        if bit == 1:
            if tree.right != None:
                tree = tree.right
        else:
            if tree.left != None:
                tree = tree.left

        if tree.char != None:
            text += tree.char
            tree = root

    return text




    
#
#def bit_iterator(bits):
#
#    bit_array = []
#
#    while bits > 0:
#
#        bit_array.append(bits & 1) 
#        bits >>= 1
#
#    for bit in reversed(bit_array):
#        yield bit
#        
#

def generate_tree(frequency_array) -> NodeHuff:

    """
    Função de geracao da arvore codificadora
    :param frequency_array: array de pares com o caractere e a frequencia na ordem descrita
    """

    node_array = []

    for tup in frequency_array:
        node_array.append(NodeHuff(tup[0], tup[1]))

    if len(node_array) == 1:
        temp = NodeHuff(weight= int(node_array[0].value))
        temp.left = node_array.pop()
        node_array.append(temp)

    while len(node_array) > 1:
        #print(len(node_array))
        temp = NodeHuff(weight = node_array[0].value + node_array[1].value)


        temp.left = node_array.pop(0)
        temp.right = node_array.pop(0)

        node_array.append(temp)

        node_array.sort(key = lambda node : node.value)

    

    tree : NodeHuff = node_array[0]

    return tree


def char_counter(string) -> list:

    """
    Função para gerar o histograma da frequencia dos caracteres
    :param string: texto em forma de string
    """
    
    frequencies = []
    for char in string:

        if not any(char in tup for tup in frequencies):
            frequencies.append([char, 1])

        else:
            for tup in frequencies:
                if tup[0] == char:
                    tup[1] += 1
                    break


    frequencies.sort(key = lambda tup : tup[1])

    return frequencies
        
