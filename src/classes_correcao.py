# This Python file uses the following encoding: utf-8


class Questao:
    def __init__(self, lst_marcacoes, gabarito):
        self.marcacoes = lst_marcacoes
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
            self.nota = self.gabarito.valor
            item = self.gabarito.valor/self.gabarito.num_item
            for i in xrange(0, self.gabarito.num_item):
                if bool(i in self.marcacoes) ^ bool(i in self.gabarito.resp):
                    self.nota -= item


class Gabarito:
    def __init__(self, valor_questao, tipo_questao, respostas, num_item):
        self.valor = valor_questao
        self.num_item = num_item
        self.resp = respostas
        self.tipo = tipo_questao


class Prova:
    def __init__(self, gabaritos, lst_marcacoes):
        self.nota = 0
        self.respostas = []
        for i, r in enumerate(gabaritos):
            self.respostas.append(Questao(lst_marcacoes[i], r))

    def avalia(self):
        self.nota = 0
        for r in self.respostas:
            r.avalia()
            self.nota += r.nota
