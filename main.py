import copy
import os
import time
import stopit


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

    def afisDrum(self, cale_output):
        f = open(cale_output, "a")
        l = self.obtineDrum()
        f.write("\n")
        for nod in l:
            f.write(str(nod))
        f.write("\nCost: " + str(self.g))
        f.write("\nLungime: " + str(len(l)))
        f.close()

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
        listaAscultati = sir.replace("\n", " ").split()
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

    def profesor(self, pozitieProfesor, pozitieBiletNodNou):
        if pozitieProfesor is None:
            return False
        if abs(pozitieProfesor[0] - pozitieBiletNodNou[0]) < 2:
            if pozitieProfesor[1] % 2 == 0:
                if pozitieProfesor[1] - pozitieBiletNodNou[1] in range(0, 3) \
                        or pozitieProfesor[1] - pozitieBiletNodNou[1] in range(-3, 0):
                    return True
            if pozitieProfesor[1] % 2 == 1:
                if pozitieProfesor[1] - pozitieBiletNodNou[1] in range(0, 4) \
                        or pozitieProfesor[1] - pozitieBiletNodNou[1] in range(-2, 0):
                    return True
        return False

    def pozitieProfesor(self, mutari):
        index = int(mutari / self.timpAscultare)
        if index > len(self.listaAscultati) - 1:
            return None
        elev = self.listaAscultati[index]
        pozitieProfesor = self.find(elev, self.banci)
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
                        or self.profesor(nodCurent.pozitieProfesor, pozitieBiletNodNou) or not self.existaElev(pozitieBiletNodNou):
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
            j_1, j_2 = ((j_curent, j_scop), (j_scop, j_curent))[j_curent > j_scop]
            if j_1 % 2 == 1:
                euristica += 1
            if j_2 % 2 == 1:
                euristica -= 1
            return euristica

        elif tip_euristica == "euristica nebanala2":
            euristica = 0
            i_curent, j_curent = pozitieBilet
            i_scop, j_scop = self.scop
            euristica += abs(i_curent - i_scop)
            return euristica

        elif tip_euristica == "euristica neadmisibila":
            euristica = 0
            i_curent, j_curent = pozitieBilet
            i_scop, j_scop = self.scop
            euristica += (i_curent - i_scop)**2 + (j_curent - j_scop)**2
            return euristica

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star(gr, cale_output, nrSolutiiCautate, tip_euristica):
    start_time = time.time()
    nrSolutie=1
    i, j = gr.start
    c = [
        NodParcurgere(  # pozitieBilet, pozitieProfesor, parinte, mutari, g, h
            gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0, gr.calculeaza_h(gr.start, tip_euristica)
        )
    ]
    maxNoduri=0

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        if len(c) > maxNoduri:
            maxNoduri = len(c)
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            f = open(cale_output, "a")
            f.write("\nSolutie: "+str(nrSolutie))
            f.close()
            nodCurent.afisDrum(cale_output)
            f = open(cale_output, "a")
            f.write("\nNumarul maxim de noduri este: "+ str(maxNoduri))
            f.write("\n--- %s seconds ---" % (time.time() - start_time))
            f.write("\n----------------\n")
            f.close()
            nrSolutiiCautate -= 1
            nrSolutie+=1
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


@stopit.threading_timeoutable(default="intrat in timeout")
def uniform_cost(gr, cale_output, nrSolutiiCautate=1):
    start_time = time.time()
    nrSolutie=1
    i, j = gr.start
    c = [
        NodParcurgere(  # pozitieBilet, pozitieProfesor, parinte, mutari, g, h
            gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0
        )
    ]
    maxNoduri = 0

    while len(c) > 0:
        maxNoduri = max(maxNoduri, len(c))
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            f = open(cale_output, "a")
            f.write("\nSolutie: "+str(nrSolutie))
            f.close()
            nodCurent.afisDrum(cale_output)
            f = open(cale_output, "a")
            f.write("\nNumarul maxim de noduri este: " + str(maxNoduri))
            f.write("\n--- %s seconds ---" % (time.time() - start_time))
            f.write("\n----------------\n")
            f.close()
            nrSolutiiCautate -= 1
            nrSolutie += 1
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

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star_optimizat(gr, cale_output, tip_euristica):
    start_time = time.time()
    i, j = gr.start
    # coada open
    c = [
        NodParcurgere(
            gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0, gr.calculeaza_h(gr.start, tip_euristica)
        )
    ]
    closed = []
    maxNoduri=0
    while len(c) > 0:
        maxNoduri = max(maxNoduri, len(c)+len(closed))
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            f = open(cale_output, "a")
            f.write("\nSolutie: ")
            f.close()
            nodCurent.afisDrum(cale_output)
            f = open(cale_output, "a")
            f.write("\nNumarul maxim de noduri este: " + str(maxNoduri))
            f.write("\n--- %s seconds ---" % (time.time() - start_time))
            f.write("\n----------------\n")
            f.close()
            return

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        lSuccesoriCopy = lSuccesori.copy()
        for s in lSuccesoriCopy:
            gasitOpen = False
            for elem in c:
                if elem.numeElev == s.numeElev:
                    gasitOpen = True
                    if elem.f > s.f:
                        c.remove(elem)
                    else:
                        lSuccesori.remove(s)
                    break

            if not gasitOpen:
                for elem in closed:
                    if elem.info == s.info:
                        if elem.f > s.f:
                            closed.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break

        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)

@stopit.threading_timeoutable(default="intrat in timeout")
def ida_star(gr, cale_output, nrSolutiiCautate = 0, tip_euristica = "euristica banala"):
    i, j = gr.start
    limita = gr.calculeaza_h(gr.start)
    nodStart = NodParcurgere(
        gr.banci[i][j], gr.start, gr.pozitieProfesor(0), None, 0, 0, gr.calculeaza_h(gr.start, tip_euristica)
    )
    while True:

        nrSolutiiCautate, rez = construieste_drum(
            gr, cale_output, nodStart, limita, nrSolutiiCautate
        )
        if rez == "gata":
            break
        if rez == float("inf"):
            f = open(cale_output, "a")
            f.write("\nNu exista suficiente solutii!")
            f.close()
            break
        limita = rez


def construieste_drum(gr, cale_output, nodCurent, limita, nrSolutiiCautate):
    start_time = time.time()
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        f = open(cale_output, "a")
        f.write("\nSolutie: ")
        f.close()
        nodCurent.afisDrum(cale_output)
        f = open(cale_output, "a")
        f.write("\n--- %s seconds ---" % (time.time() - start_time))
        f.write("\n----------------\n")
        f.close()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    minim = float("inf")
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, cale_output, s, limita, nrSolutiiCautate)
        if rez == "gata":
            return nrSolutiiCautate, "gata"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim


def util(cale_input, cale_output, nrSolutiiCautate, timeout):
    gr = Graph(cale_input)
    NodParcurgere.gr = gr
    f = open(cale_output, "w")
    f.write("\nSolutie " + cale_input)
    f.close()
    euristici = ['euristica banala', 'euristica nebanala1', 'euristica nebanala2', 'euristica neadmisibila']
    for tip_euristica in euristici:
        f = open(cale_output, "a")
        f.write("\n\n##################\nSolutii obtinute cu A* " + tip_euristica)
        f.close()
        a_star(gr, cale_output, nrSolutiiCautate, tip_euristica, timeout=timeout)
    for tip_euristica in euristici:
        f = open(cale_output, "a")
        f.write("\n\n##################\nSolutii obtinute cu A* optimizat " + tip_euristica)
        f.close()
        a_star_optimizat(gr, cale_output, tip_euristica, timeout=timeout)
    for tip_euristica in euristici:
        f = open(cale_output, "a")
        f.write("\n\n##################\nSolutii obtinute cu IDA* " + tip_euristica)
        f.close()
        ida_star(gr, cale_output, nrSolutiiCautate, tip_euristica, timeout=timeout)
    f = open(cale_output, "a")
    f.write("\n\n##################\nSolutii obtinute cu UCS ")
    f.close()
    uniform_cost(gr, cale_output, nrSolutiiCautate, timeout=timeout)


def main():

    nrSolutiiCautate = int(input('Introduceti numarul de solutii:'))
    folder_input = str(input('Introduceti calea de input'))
    folder_output = str(input('Introduceti calea de output'))
    timeout = int(input('Introduceti timpul de timeout'))
    entries = os.listdir(folder_input)
    for entry in entries:
        cale_input = os.path.join(folder_input, entry)
        cale_output = os.path.join(folder_output, "output_"+entry)
        util(cale_input, cale_output, nrSolutiiCautate, timeout)


if __name__ == '__main__':
    main()