import numpy as np
from encoding import *
from file_handler import *

def tests():

    string = """
    aaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbcccccccccccccccc"""
#A lobotomia foi um dos procedimentos cirúrgicos mais cruéis da história da medicina moderna. A ideia parecia simples, mas gerava efeitos colaterais permanentes nos pacientes. Esse vídeo conta a história da lobotomia, o que acontecia com os pacientes e o porquê de termos inventado (e aplicado) uma cirurgia tão bizarra.
#
#Se você quer se aventurar no mundo tech ou dar um upgrade na sua carreira, eu recomendo a Alura!
#Com o meu link, você tem 15% de desconto na sua matrícula, que te dá acesso a todos os cursos!
#https://alura.tv/cienciatododia
#
#Seja membro do nosso canal para ajudar a manter os vídeos no ar! http://youtube.com/cienciatododia/join
#
#E-mail comercial: pedro@play9.com.br
#
#Minhas redes sociais:
#  / pedroloos  
#  / pedroloos  
#  / opedroloos  
#
#Nosso podcast: https://open.spotify.com/show/59fUC0C...
#
#Capítulos
#0:00 - 0:56 Introdução
#0:56 - 5:10 A origem da lobotomia
#5:10 - 7:03 As mudanças nas técnicas das lobotomias
#7:03 - 8:53 A febre da lobotomia
#8:53 - 12:08 Lobotomia social
#12:08 - 14:22 Os casos mais famosos
#14:22 - 16:34 O declínio das lobotomias
#
#
#Fontes e Leitura Adicional:
#
#Imagens e Fotografias
#
#Acervo de Fotografias digitalizadas do material do Freeman: https://searcharchives.library.gwu.ed...
#
#Imagem do equipamento: https://www.flickr.com/photos/gwgelma...
#
#Freeman Operando cercado de pessoas: https://historypsychiatry.com/wp-cont...
#
#
#Fotos do Paciente Dulley: Antes, durante e depois
#https://storycorpsorg-staging.s3.amaz...
#
#https://storycorpsorg-staging.s3.amaz...
#
#https://storycorpsorg-staging.s3.amaz...
#
#Fontes:
#
#https://archive.org/details/mylobotom...
#
#https://www.bookey.app/pt/book/minha-...
#
#https://archive.org/details/lobotomis...
#
#https://pt.wikipedia.org/wiki/Lobotomia
#
#https://pt.wikipedia.org/wiki/Ant%C3%...
#
#https://pt.wikipedia.org/wiki/Walter_...
#
#https://www.bbc.com/portuguese/notici...
#
#https://g1.globo.com/ciencia-e-saude/...
#
#https://super.abril.com.br/ciencia/lo...
#
#https://ppghcs.coc.fiocruz.br/todas-a...
#    """


    num =    np.uint8(255)
    bits = bin(num) 

    print(f"Numero original = {num}")
    print(f"Valor em binário = {bits}")
    print(f"histograma = {char_counter(string)}")
    tree = generate_tree(char_counter(string))

    print(tree)

    print(f"A = {(encode_char(tree, "a"))}")
    print(f"B = {(encode_char(tree, "B"))}")
    print(f"C = {(encode_char(tree, "C"))}")
    print(f"D = {(encode_char(tree, "D"))}")

    encoded = encode(string, tree)
    n = np.packbits(encoded)
    print(n)
    print(encoded)


    u: int = 0
    for num in n:
        u = u << 8 | num

    print(bin(u))



    #test = bin(encode_char(tree, "D"))

    print()
    print(string)
    print(decode(tree, encoded))

    file = open("./requirements.txt", "rb")
    cont = file.read()
    bits = np.unpackbits(np.frombuffer(cont, np.uint8))
#    for bit in cont:
#        bits.append(bit)
#
    print(bits)
    print(str(np.packbits(bits), encoding="utf-8"))

    bytis = bytearray(np.packbits(bits))
    num = np.uint32(0)

    for by in range(4):
        print(by)
        print(bin(num))
        print(bin(bytis[by]))
        num = num << 8 | bytis[by]

    print(num)
    print(bin(num))

    fa = char_counter(string)
    header = construct_header(uint32(len(bits)), fa)
    body = bytearray(np.packbits(encoded))
    
    print(f"header = {header}")
    print(f"body = {body}")
    header.extend(body)
    print(header)

    print(read_header(header))

    compress_file("hello.txt")

    decompress_file("hello.huff")




