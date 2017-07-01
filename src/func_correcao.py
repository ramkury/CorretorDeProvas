# This Python file uses the following encoding: utf-8
from classes_correcao import *

    
def cria_gabarito():
    print("Bem-vindo ao Gerenciador de Gabarito!")
    print("Trabalhamos com 2 tipos de questões:")
    print("1 - Questões tipo C com uma única alternativa")
    print("2 - Questões tipo C com múltiplas alternativas \n")
    i = 1
    a = int(raw_input("Forneça o tipo da questão %d: (ou 0 (zero) caso a questão não exista) " %i))
    gabarito = []

    while a != 0:
        resp = []

        while (a!=1) and (a!=2):
            print("Trabalhamos com 2 tipos de questões:")
            print("1 - Questões tipo C com uma única alternativa")
            print("2 - Questões tipo C com múltiplas alternativas \n")
            a = int(raw_input("Forneça o tipo da questão %d: (ou 0 (zero) caso a questão não exista) " % i))

        if a == 1:
            letra = raw_input("Forneça a letra referente a resposta correta: ")
            letra = letra.lower()
            resp.append(ord(letra)-ord('a'))
        elif a == 2:
            letras = raw_input("Forneça todas as letras que devem ser marcadas separadas apenas por espaços: ")
            letras = letras.lower()
            op = letras.split()
            for r in op:
                resp.append(ord(r)-ord('a'))

        val = float(raw_input("Forneça o valor total da questão: "))

        gabarito.append(Gabarito(val, a, resp))
        i += 1
        a = int(raw_input("Forneça o tipo da questão %d: (ou 0 (zero) caso a questão não exista) " % i))

    return gabarito


def corrige_prova(gabaritos, lst_marcacoes):
    prova = Prova(gabaritos, lst_marcacoes)
    prova.avalia()
    # print("A nota é: %f" % prova.nota)
    return prova.nota


def write_from_zero(fileName, text):
    file = open(fileName, 'w')
    sizeText = file.write(text)
    fechou = file.close()
    return fechou and (sizeText == text.len())  # retorna true se houve sucesso na escrita


def read_all(fileName): #  eh um problema se o arquivo for maior que a memoria da maquina
    file = open(fileName, 'r')  # modo pode ser ocultado, pois read eh default
    text = file.read()  # quando o parametro eh omitido tudo que tem no arquivo eh lido
    file.close()
    return text


def salva_gabarito_txt(full_path, gabarito):
    text = ""
    for r in gabarito:
        text_questao = "%d %f" %(r.tipo, r.valor)
        for y in r.resp:
            text_questao = text_questao + " %d" %(y)
        text += text_questao + "\n"

    write_from_zero(full_path, text)


def le_gabarito_txt(full_path):
    text = read_all(full_path)
    gabarito = []
    text_line = text.splitlines()
    for r in text_line:
        elementos = r.split()
        tipo = int(elementos[0])
        val = float(elementos[1])
        resp = []
        for i in xrange(2, len(elementos)):
            resp.append(int(elementos[i]))
        gabarito.append(Gabarito(val, tipo, resp))
    return gabarito

# if __name__ == '__main__':
#     main()
