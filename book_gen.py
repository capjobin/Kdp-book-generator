
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from PIL import Image

def generate_book(title, out_zip):
    c = canvas.Canvas("interior.pdf", pagesize=LETTER)
    c.setFont("Helvetica", 20)
    c.drawString(100, 700, title)
    c.showPage()
    c.save()
    img = Image.new("RGB", (1000,1500), "blue")
    img.save("cover.jpg")

    import zipfile
    with zipfile.ZipFile(out_zip, "w") as z:
        z.write("interior.pdf")
        z.write("cover.jpg")
