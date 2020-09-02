import os
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



def pdf_text(pdf_path):
    # open the pdf file
    pdf_file = open(pdf_path, 'rb')

    # read pdf
    read_pdf = PyPDF4.PdfFileReader(pdf_file)

    all_text = ""
    for num in range(0, read_pdf.numPages - 1):
        page = read_pdf.getPage(num)
        txt = page.extractText()
        all_text = all_text + txt

    all_text = all_text.replace("\n", "").replace("  "," ").split("DISPOSICIONES FINALES Y TRANSITORIAS")[0]
    return all_text

def parse_constitucion(constitucion_text):
    constitucion = Constitucion([])
    for it, titulo in enumerate(constitucion_text.split("TITULO")):
        if (it > 0):
            nombre_titulo = ""
            capitulos = []
            articulos = []
            if ("CAPITULO" in titulo):
                nombre_titulo = ("TITULO" + titulo.split("CAPITULO", 1)[0]).strip()
                for ic, capitulo in enumerate(titulo.split("CAPITULO")):
                    if (ic > 0):
                        nombre_capitulo = ("CAPITULO" + capitulo.split("Artículo", 1)[0]).strip()
                        articulos = []
                        for ia, articulo in enumerate(capitulo.split("Artículo")):
                            if (ia > 0):
                                articulos.append(Articulo("Artículo" + articulo))
                        capitulos.append(Capitulo(nombre_capitulo, articulos))
            else:
                nombre_titulo = ("TITULO" + titulo.split("Artículo", 1)[0]).strip()
                articulos = []
                for ia, articulo in enumerate(titulo.split("Artículo")):
                    if (ia > 0):
                        articulos.append(Articulo("Artículo" + articulo))
            constitucion.titulos.append(Titulo(nombre_titulo, capitulos, articulos))
    return constitucion

def write_constitucion(constitucion, constitucion_path):
    constitucion_file = open(constitucion_path + "/_index.md", "a")

    constitucion_file.write("---\n")
    constitucion_file.write("title: \"Constitucion de 1993\"\n")
    constitucion_file.write("date: 2019-03-26T08:47:11+01:00\n")
    constitucion_file.write("---\n\n")

    for titulo in constitucion.titulos:
        titulo_path = constitucion_path + "/titulo-" + titulo.numero.lower()
        try:
           os.makedirs(titulo_path)
        except OSError:
           print(titulo_path + " already exists")
        if (len(titulo.capitulos) > 0):
            titulo_file = open(titulo_path + "/_index.md", "a")
            titulo_file.write("---\n")
            titulo_file.write("title: \""+ titulo.nombre +"\"\n")
            titulo_file.write("date: 2019-03-26T08:47:11+01:00\n")
            titulo_file.write("constitucion: \"1993\"\n")
            titulo_file.write("type: \"titulo\"\n")
            titulo_file.write("---\n\n")
            for capitulo in titulo.capitulos:
                capitulo_path = titulo_path + "/capitulo-" + capitulo.numero.lower() + ".md"
                capitulo_file = open(capitulo_path, "a")
                capitulo_file.write("---\n")
                capitulo_file.write("title: \""+ capitulo.nombre +"\"\n")
                capitulo_file.write("date: 2019-03-26T08:47:11+01:00\n")
                capitulo_file.write("constitucion: \"1993\"\n")
                capitulo_file.write("type: \"capitulo\"\n")
                capitulo_file.write("---\n\n")
                for articulo in capitulo.articulos:
                    capitulo_file.write("## " + articulo.nombre + "\n" + "\n")
                    capitulo_file.write(articulo.texto + "\n" + "\n")
                capitulo_file.close()
            titulo_file.close()
        if (len(titulo.articulos) > 0):
            titulo_file = open(titulo_path + "/index.md", "a")
            titulo_file.write("---\n")
            titulo_file.write("title: \""+ titulo.nombre +"\"\n")
            titulo_file.write("date: 2019-03-26T08:47:11+01:00\n")
            titulo_file.write("constitucion: \"1993\"\n")
            titulo_file.write("type: \"titulo\"\n")
            titulo_file.write("---\n\n")
            for articulo in titulo.articulos:
                titulo_file.write("## " + articulo.nombre + "\n" + "\n")
                titulo_file.write(articulo.texto)
            titulo_file.close()
        constitucion_file.write("## " + titulo.nombre + "\n" + "\n")

    constitucion_file.close()

path = os.getcwd()
constitucion_path = path + "/content/docs/1993"
#os.rmdir(constitucion_path)
os.mkdir(constitucion_path)
constitucion_pdf_path = 'static/Texto_actualizado_CONS_1993.pdf'
constitucion_text = pdf_text(constitucion_pdf_path)
constitucion = parse_constitucion(constitucion_text)
write_constitucion(constitucion, constitucion_path)
