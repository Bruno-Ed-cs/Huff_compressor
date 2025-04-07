import numpy as np
import binarytree as btree

class NodeHuff(btree.Node):
    """
    Classe que representa um nó da árvore de Huffman, herdando de btree.Node
    Atributos:
        char: caractere armazenado no nó (None para nós internos)
        value: peso/frequência do nó
        left: filho esquerdo
        right: filho direito
    """
    def __init__(self, char=None, weight=None):
        self.char = char
        self.value = weight
        self.left = None
        self.right = None

def encode_char(node: NodeHuff, char, sequence = None):
    """
    Função recursiva para codificar um caractere em uma sequência de bits
    baseada na árvore de Huffman.
    
    Args:
        node (NodeHuff): Nó atual da árvore de Huffman
        char (str): Caractere a ser codificado
        sequence (list, optional): Lista acumulativa de bits. Defaults to None.
    
    Returns:
        list: Sequência de bits que representa o caractere ou None se não encontrado
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
    """
    Codifica uma string completa usando a árvore de Huffman.
    
    Args:
        string (str): Texto a ser codificado
        tree (NodeHuff): Árvore de Huffman para codificação
    
    Returns:
        list: Lista de bits representando a string codificada
    """
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
    Decodifica uma sequência de bits usando a árvore de Huffman.
    
    Args:
        tree (NodeHuff): Árvore de Huffman para decodificação
        code (list): Sequência de bits a ser decodificada
    
    Returns:
        str: Texto decodificado
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

def generate_tree(frequency_array) -> NodeHuff:
    """
    Gera a árvore de Huffman a partir de um array de frequências.
    
    Args:
        frequency_array (list): Lista de tuplas (caractere, frequência)
    
    Returns:
        NodeHuff: Raiz da árvore de Huffman gerada
    """
    node_array = []

    for tup in frequency_array:
        node_array.append(NodeHuff(tup[0], tup[1]))

    if len(node_array) == 1:
        temp = NodeHuff(weight= int(node_array[0].value))
        temp.left = node_array.pop()
        node_array.append(temp)

    while len(node_array) > 1:
        temp = NodeHuff(weight = node_array[0].value + node_array[1].value)

        temp.left = node_array.pop(0)
        temp.right = node_array.pop(0)

        node_array.append(temp)
        node_array.sort(key = lambda node : node.value)

    tree : NodeHuff = node_array[0]
    return tree

def char_counter(string) -> list:
    """
    Conta a frequência de cada caractere em uma string.
    
    Args:
        string (str): Texto a ser analisado
    
    Returns:
        list: Lista de tuplas (caractere, frequência) ordenada por frequência
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
