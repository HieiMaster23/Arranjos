"""Prévia rápida em PDF de um MusicXML (Verovio + CairoSVG), sem precisar do Sibelius.

Uso: python3 ferramentas/previa_pdf.py entrada.musicxml saida.pdf
Requer: pip install verovio cairosvg pypdf
A gravação/diagramação final é sempre a do Sibelius; isto serve só para conferir notas,
letra e cifras.
"""
import io
import re
import sys

import cairosvg
import pypdf
import verovio

# glifos SMuFL que a fonte do Cairo não tem (acidentes das cifras e figura do metrônomo)
SUB = {"": "b", "": "#", "": "", "": "♩"}


def main(src, out):
    tk = verovio.toolkit()
    tk.setOptions({"pageWidth": 2100, "pageHeight": 2970, "scale": 40, "adjustPageHeight": False,
                   "footer": "none", "breaks": "auto", "lyricSize": 4.0, "spacingSystem": 10})
    if not tk.loadFile(src):
        sys.exit(f"não consegui ler {src}")
    w = pypdf.PdfWriter()
    for i in range(1, tk.getPageCount() + 1):
        svg = tk.renderToSVG(i)
        svg = re.sub(r'<tspan font-family="Leipzig" font-size="(\d+)px">([^<]*)</tspan>',
                     lambda m: '<tspan font-size="405px">' + "".join(SUB.get(c, c) for c in m.group(2)) + '</tspan>',
                     svg)
        # cifras: o Verovio repete os <degree> já contidos no nome do acorde
        svg = svg.replace("sus4(4no3)", "sus4").replace("6/9(9)", "6/9")
        pdf = cairosvg.svg2pdf(bytestring=svg.encode())
        for pg in pypdf.PdfReader(io.BytesIO(pdf)).pages:
            w.add_page(pg)
    w.write(out)
    print(f"{out}: {tk.getPageCount()} páginas")


if __name__ == "__main__":
    main(*sys.argv[1:3])
