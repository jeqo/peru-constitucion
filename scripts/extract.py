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

def write_constitucion(year, constitucion, constitucion_path):
    summary = "- [Constitución Política de " + year +"](./" + year + "/README.md)\n"

    constitucion_file = open(constitucion_path + "/README.md", "a")

    for titulo in constitucion.titulos:
        titulo_dir = "titulo-" + titulo.numero.lower()
        summary = summary + "  - [" + titulo.nombre + "](./" + year + "/" + titulo_dir + "/README.md)\n"
        titulo_path = constitucion_path + "/" + titulo_dir
        try:
           os.makedirs(titulo_path)
        except OSError:
           print(titulo_path + " already exists")
        if (len(titulo.capitulos) > 0):
            titulo_file = open(titulo_path + "/README.md", "a")
            titulo_file.write("# "+ titulo.nombre )
            for capitulo in titulo.capitulos:
                capitulo_filename = "capitulo-" + capitulo.numero.lower() + ".md"
                summary = summary + "    - [" + capitulo.nombre + "](./" + year + "/" + titulo_dir + "/" + capitulo_filename + ")\n"
                capitulo_path = titulo_path + "/" + capitulo_filename
                capitulo_file = open(capitulo_path, "a")
                capitulo_file.write("# " + capitulo.nombre)
                for articulo in capitulo.articulos:
                    capitulo_file.write("\n" + "## " + articulo.nombre + "\n")
                    capitulo_file.write(articulo.texto + "\n" + "\n")
                capitulo_file.close()
            titulo_file.close()
        if (len(titulo.articulos) > 0):
            titulo_file = open(titulo_path + "/README.md", "a")
            titulo_file.write("# "+ titulo.nombre)
            for articulo in titulo.articulos:
                titulo_file.write("\n" + "## " + articulo.nombre +  "\n")
                titulo_file.write(articulo.texto)
            titulo_file.close()

    constitucion_file.close()
    return summary

path = os.getcwd()
constitucion_year = "1993"
constitucion_path = path + "/src/" + constitucion_year
os.mkdir(constitucion_path)
constitucion_pdf_path = 'static/Texto_actualizado_CONS_1993.pdf'
constitucion_text = pdf_text(constitucion_pdf_path)
constitucion = parse_constitucion(constitucion_text)
summary = write_constitucion(constitucion_year, constitucion, constitucion_path)
print(summary)