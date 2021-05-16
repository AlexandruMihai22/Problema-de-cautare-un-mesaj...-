
f = open("input_c.txt", "r")
continut_fisier = f.read()
siruriStari = continut_fisier.replace("suparati", ",").replace("ascultati:", ",") \
    .replace("mesaj:", ",").replace("->", " ").strip().split(",")
print(siruriStari[2])
sir = siruriStari[2]
listaAscultati = sir.replace("\n","").split(" ")
print(listaAscultati)
