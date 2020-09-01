import PyPDF4

class Constitucion:
    def __init__(self, titulos):
        self.titulos = titulos
        
    def __str__(self):
        txt = ""
        for i in self.titulos:
            txt = txt + str(i) + "\n"
        return txt

class Titulo:
    def __init__(self, nombre, capitulos, articulos):
        self.nombre = nombre
        self.numero = nombre.split(" ")[1]
        self.capitulos = capitulos
        if (len(capitulos) == 0):
            self.articulos = articulos
        else:
            self.articulos = []

    def __str__(self):
        txt = self.nombre + "\n"
        for i in self.capitulos:
            txt = txt + str(i) + "\n"
        for i in self.articulos:
            txt = txt + str(i) + "\n"
        return txt

class Capitulo:
    def __init__(self, nombre, articulos):
        self.nombre = nombre
        self.numero = nombre.split(" ")[1]
        self.articulos = articulos
    
    def __str__(self):
        txt = self.nombre + "\n"
        for i in self.articulos:
            txt = txt + str(i) + "\n"
        return txt

class Articulo:
    def __init__(self, texto):
        parts = texto.split(" ", 2)
        self.nombre = (parts[0] + " " + parts[1]).replace(".-", "")
        self.numero = self.nombre.split(" ")[1]
        self.texto = parts[2]

    def __str__(self):
        return self.texto

# open the pdf file
pdf_file = open('static/Texto_actualizado_CONS_1993.pdf', 'rb')

# read pdf
read_pdf = PyPDF4.PdfFileReader(pdf_file)

# print(read_pdf.numPages)
isTitulo = True
constitucion = Constitucion([])
allText = ""
for num in range(0, read_pdf.numPages - 1):
    page = read_pdf.getPage(num)
    txt = page.extractText()
    allText = allText + txt

allText = allText.replace("\n", "").replace("  "," ").split("DISPOSICIONES FINALES Y TRANSITORIAS")[0]
# print(allText)

for it, titulo in enumerate(allText.split("TITULO")):
    if (it > 0):
        nombreTitulo = ""
        capitulos = []
        articulos = []
        if ("CAPITULO" in titulo):
            nombreTitulo = ("TITULO" + titulo.split("CAPITULO", 1)[0]).strip()
            for ic, capitulo in enumerate(titulo.split("CAPITULO")):
                if (ic > 0):
                    nombreCapitulo = ("CAPITULO" + capitulo.split("Artículo", 1)[0]).strip()
                    articulos = []
                    for ia, articulo in enumerate(capitulo.split("Artículo")):
                        if (ia > 0):
                            articulos.append(Articulo("Artículo" + articulo))
                    capitulos.append(Capitulo(nombreCapitulo, articulos))
        else:
            nombreTitulo = ("TITULO" + titulo.split("Artículo", 1)[0]).strip()
            articulos = []
            for ia, articulo in enumerate(titulo.split("Artículo")):
                if (ia > 0):
                    articulos.append(Articulo("Artículo" + articulo))
        constitucion.titulos.append(Titulo(nombreTitulo, capitulos, articulos))

import os

path = os.getcwd()

for titulo in constitucion.titulos:
    tituloPath = path + "/content/constituciones/1993/titulo-" + titulo.numero.lower()
    try:
        os.makedirs(tituloPath)
    except OSError:
        print(tituloPath + " already exists")
    tituloMain = open(tituloPath + "/index.md", "a")
    tituloMain.write("# " + titulo.nombre + "\n" + "\n")
    for capitulo in titulo.capitulos:
        capituloPath = tituloPath + "/capitulo-" + capitulo.numero.lower()
        try:
            os.makedirs(capituloPath)
        except OSError:
            print(capituloPath + " already exists")
        capituloMain = open(capituloPath + "/index.md", "a")
        capituloMain.write("# " + capitulo.nombre + "\n" + "\n")
        for articulo in capitulo.articulos:
            print(articulo.nombre)
            capituloMain.write("## " + articulo.nombre + "\n" + "\n")
            capituloMain.write(articulo.texto + "\n" + "\n")
        capituloMain.close()
        tituloMain.write("## " + capitulo.nombre + "\n" + "\n")

    for articulo in titulo.articulos:
        print(articulo.nombre)
        tituloMain.write("## " + articulo.nombre + "\n" + "\n")
        tituloMain.write(articulo.texto)
    tituloMain.close()