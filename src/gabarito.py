# This Python file uses the following encoding: utf-8


class Questao:

    def __init__(self, lstMarcacoes, gabarito):
        self.marcacoes = lstMarcacoes
        self.nota = 0
        self.gabarito = gabarito

    def avalia(self):
        self.nota = 0
        if self.gabarito.tipo == 1:  # marcação única - Tipo C
            if len(self.marcacoes) != 1:
                return
            elif self.marcacoes[0] == self.gabarito.resp[0]:
                self.nota = self.gabarito.valor
                return
            else:
                return

        elif self.gabarito.tipo == 2:  # múltiplas marcações - Tipo C
            for r in self.marcacoes:
                if r in self.gabarito.resp:
                    self.nota += self.gabarito.valor
        return


class Gabarito:

    def __init__(self, valorQuestao, tipoQuestao, respostas):
        if tipoQuestao == 1:  # marcação única - Tipo C
            self.valor = valorQuestao
        elif tipoQuestao == 2:  # múltiplas marcações - Tipo C
            self.valor = valorQuestao / len(respostas)

        self.resp = respostas
        self.tipo = tipoQuestao


class Prova:

    def __init__(self, gabaritos, lstMarcacoes):
        self.nota = 0
        self.respostas = []
        for i, r in enumerate(gabaritos):
            self.respostas.append(Questao(lstMarcacoes[i], r))

    def avalia(self):
        self.nota = 0
        for r in self.respostas:
            r.avalia()
            self.nota += r.nota


def main():
    print("Bem-vindo ao Gerenciador de Gabarito!")
    print("Trabalhamos com 2 tipos de questões:")
    print("1 - Questões tipo C com uma única alternativa")
    print("2 - Questões tipo C com múltiplas alternativas")
    i = 1
    a = int(raw_input("Forneça o tipo da questão %d: (ou 0 (zero) caso a questão não exista)" %i))
    gabarito = []

    while(a != 0):
        if(a == 1):
            a



if __name__ == '__main__':
    main()
