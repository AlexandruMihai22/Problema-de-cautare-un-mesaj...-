import copy


class NodParcurgere:
    gr = None

    def __init__(self, numeElev, pozitieBilet, pozitieProfesor, parinte, mutari,cost=0, h=0):
        self.numeElev = numeElev
        self.pozitieBilet = pozitieBilet
        self.pozitieProfesor = pozitieProfesor
        self.parinte = parinte
        self.mutari = mutari
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        print("Cost: ", self.g)
        print("Lungime: ", len(l))

    def contineInDrum(self, pozitieBiletNodNou):
        nodDrum = self
        while nodDrum is not None:
            if pozitieBiletNodNou == nodDrum.pozitieBilet:
                return True
            nodDrum = nodDrum.parinte
        return False

    def __repr__(self):
        # TODO:implement
        sir = ""
        sir += str(self.numeElev)
        sir += self.obtineDirectie()
        return sir

    def __str__(self):
        sir = ""
        sir += self.obtineDirectie()
        sir += str(self.numeElev)
        return sir

    def obtineDirectie(self):
        sir = ""
        if self.parinte is None:
            return sir
        if self.parinte.pozitieBilet[0] > self.pozitieBilet[0]:
            sir += " ^ "
        elif self.parinte.pozitieBilet[0] < self.pozitieBilet[0]:
            sir += " v "
        elif self.parinte.pozitieBilet[1] < self.pozitieBilet[1]:
            if self.pozitieBilet[1] %2 == 1:
                sir += " > "
            else:
                sir+= " >> "
        elif self.parinte.pozitieBilet[1] > self.pozitieBilet[1]:
            if self.pozitieBilet[1] %2 == 1:
                sir += " << "
            else:
                sir+= " < "
        return sir
        pass


class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        continut_fisier = f.read()

        siruriStari = continut_fisier.replace("suparati", ",").replace("ascultati:", ",") \
            .replace("mesaj:", ",").replace("->", " ").strip().split(",")
        self.banci, \
        self.numarLinii, \
        self.numarColoane = self.obtineBanci(siruriStari[0])
        self.listaSuparati = self.obtineSuparati(siruriStari[1])
        self.listaAscultati, \
        self.timpAscultare = self.obtineAscultati(siruriStari[2])
        self.start,\
        self.scop = self.obtineMesaj(siruriStari[3])

    def find(self, element, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == element:
                    return (i, j)

    def obtineBanci(self, sir):
        listaLinii = sir.strip().split("\n")
        banci = [linie.strip().split(" ") for linie in listaLinii]
        nlines = len(banci)
        ncolums = len(banci[0])
        return banci, nlines, ncolums

    def obtineSuparati(self, sir):
        listaSuparati = {}
        listaLinii = sir.strip().split("\n")
        for linie in listaLinii:
            elev1, elev2 = (str(z) for z in linie.split())
            pozitie1 = self.find(elev1, self.banci)
            pozitie2 = self.find(elev2, self.banci)
            if pozitie1 in listaSuparati.keys():
                listaSuparati[pozitie1].append(pozitie2)
            else:
                listaSuparati[pozitie1] = [pozitie2]
            if pozitie2 in listaSuparati.keys():
                listaSuparati[pozitie2].append(pozitie1)
            else:
                listaSuparati[pozitie2] = [pozitie1]
        return listaSuparati

    def obtineAscultati(self, sir):
        listaAscultati = sir.replace("\n","").split(" ")
        timpAscultare = listaAscultati[0]
        listaAscultati.pop(0)
        return listaAscultati, int(timpAscultare)

    def obtineMesaj(self, sir):
        elevStart, elevScop = (str(elev) for elev in sir.split())
        start = self.find(elevStart,self.banci)
        scop = self.find(elevScop, self.banci)
        return start, scop

    def eleviSuparati(self, pozitieBiletNodNou, pozitieBilet):
        if pozitieBilet in self.listaSuparati.keys():
            if pozitieBiletNodNou in self.listaSuparati[pozitieBilet]:
                return 1
        return 0

    def existaElev(self, pozitieBiletNodNou):
        x, y = pozitieBiletNodNou
        if self.banci[x][y] != "liber":
            return 1
        return 0

    def profesor(self, nodCurent, pozitieBiletNodNou):
        if nodCurent.pozitieProfesor is None:
            return False
        if abs(nodCurent.pozitieProfesor[0] - pozitieBiletNodNou[0]) < 2:
            if nodCurent.pozitieProfesor[1] % 2 == 0:
                if nodCurent.pozitieProfesor[1] - pozitieBiletNodNou[1] < 3 \
                        or nodCurent.pozitieProfesor[1] - pozitieBiletNodNou[1] > -4:
                    return True
            if nodCurent.pozitieProfesor[1] % 2 == 1:
                if nodCurent.pozitieProfesor[1] - pozitieBiletNodNou[1] < 4 \
                        or nodCurent.pozitieProfesor[1] - pozitieBiletNodNou[1] > -3:
                    return True
        return False

    def pozitieProfesor(self, mutari):
        index = int(mutari / self.timpAscultare)
        if index > len(self.listaAscultati) - 1:
            return None
        elev = self.listaAscultati[index]
        pozitieProfesor = self.find(elev,self.banci)
        return pozitieProfesor

    def calculeazaCost(self, pozitieBilet, pozitieBiletNodNou):
        if pozitieBilet[0] != pozitieBiletNodNou[0]:
            return 1
        if pozitieBilet[1] > pozitieBiletNodNou[1] and pozitieBilet[1] % 2 == 0:
            return 2
        if pozitieBilet[1] < pozitieBiletNodNou[1] and pozitieBilet[1] % 2 == 1:
            return 2
        return 0

    def testeaza_scop(self, nodCurent):
        return nodCurent.pozitieBilet == self.scop

    def verificaExistentaSolutie(self, infoNod):
        # TODO: implement
        return True

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        directii = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        linieCurenta, coloanaCurenta = nodCurent.pozitieBilet[0], nodCurent.pozitieBilet[1]
        for dl, dc in directii:
            linieVecin = linieCurenta + dl
            coloanaVecin = coloanaCurenta + dc
            pozitieBiletNodNou = (linieVecin, coloanaVecin)
            pozitieProfesor = self.pozitieProfesor(nodCurent.mutari)
            try:
                if linieVecin < 0 or coloanaVecin < 0 or linieVecin >= self.numarColoane \
                        or coloanaVecin >= self.numarLinii or \
                        self.eleviSuparati(pozitieBiletNodNou, nodCurent.pozitieBilet) \
                        or self.profesor(nodCurent, pozitieBiletNodNou) or not self.existaElev(pozitieBiletNodNou):
                    continue
                if not nodCurent.contineInDrum(pozitieBiletNodNou):
                    listaSuccesori.append(
                        NodParcurgere(  # pozitieBilet, pozitieProfesor, parinte, mutari, g, h
                            self.banci[linieVecin][coloanaVecin],
                            pozitieBiletNodNou,
                            pozitieProfesor,
                            nodCurent, nodCurent.mutari + 1,
                            nodCurent.g + self.calculeazaCost(nodCurent.pozitieBilet, pozitieBiletNodNou),
                            self.calculeaza_h(pozitieBiletNodNou, tip_euristica)
                        )
                    )
            except IndexError:
                pass
        return listaSuccesori

    def calculeaza_h(self, pozitieBilet, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if pozitieBilet != self.scop:
                return 1
            return 0
        elif tip_euristica == "euristica nebanala1":
            euristica = 0
            i_curent, j_curent = pozitieBilet
            i_scop, j_scop = self.scop
            euristica += abs(i_curent - i_scop) + abs(j_curent - j_scop)
            return euristica

        elif tip_euristica == "euristica nebanala2":
            pass

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def a_star(gr, nrSolutiiCautate, tip_euristica):
    if not gr.verificaExistentaSolutie(gr.start):
        print("Nu avem solutii")
        return
    i, j = gr.start
    c = [
        NodParcurgere(  # pozitieBilet, pozitieProfesor, parinte, mutari, g, h
            gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0, gr.calculeaza_h(gr.start, tip_euristica)
        )
    ]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum()
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)


def uniform_cost(gr, nrSolutiiCautate=1):
    i, j = gr.start
    c = [
        NodParcurgere(  # pozitieBilet, pozitieProfesor, parinte, mutari, g, h
            gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0, gr.calculeaza_h(gr.start, tip_euristica)
        )
    ]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i, s)

def main():
    gr = Graph("input_c.txt")
    NodParcurgere.gr = gr
    nrSolutiiCautate = int(input('Introduceti nuumarul de solutii:'))
    print("\n\n##################\nSolutii obtinute cu A*:")
    a_star(gr, nrSolutiiCautate,"euristica banala")
   # uniform_cost(gr, nrSolutiiCautate)

if __name__ == '__main__':
    main()