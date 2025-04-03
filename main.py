import numpy as np
import binarytree as btree

string = "entenda meu dilema, espero que este algorítimo funcione" 


class NodeHuff(btree.Node):
    def __init__(self, char=None, weight=None):
        self.char = char
        self.value = weight
        self.left = None
        self.right = None

def encode(node: NodeHuff, char , sequence = None):

    if sequence is None:
        sequence = []

    if node.char == char:
        return sequence.copy()
    elif node.char != None and node.char != char:
        return None


    if node.left != None:
        sequence.append(0)
        seq = encode(node.left, char, sequence)
        if seq != None:
            return seq
        sequence.pop()

    if node.right != None:
        sequence.append(1)
        seq = encode(node.right, char, sequence)
        if seq != None:
            return seq
        sequence.pop()


    return None

def decode(tree: NodeHuff, code):

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

def generate_tree(frequency_array):

    node_array = []

    for tup in frequency_array:
        node_array.append(NodeHuff(tup[0], tup[1]))


    while len(node_array) > 1:
        print(len(node_array))
        temp = NodeHuff(weight = node_array[0].value + node_array[1].value)


        temp.left = node_array.pop(0)
        temp.right = node_array.pop(0)

        node_array.append(temp)

        node_array.sort(key = lambda node : node.value)


    tree : NodeHuff = node_array[0]

    return tree


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
tree = generate_tree(char_counter(string))

print(tree)

print(f"A = {(encode(tree, "a"))}")
print(f"B = {(encode(tree, "B"))}")
print(f"C = {(encode(tree, "C"))}")
print(f"D = {(encode(tree, "D"))}")

encoded = []

for x in string:
    
    result = encode(tree, x)
#    print(result)
    if result == None:
        break
    #print(gap)
    encoded += result

                    

n = np.packbits(encoded)
print(n)
print(encoded)


u: int = 0
for num in n:
    u = u << 8 | num

print(bin(u))



#test = bin(encode(tree, "D"))

print()
print(string)
print(decode(tree, encoded))
