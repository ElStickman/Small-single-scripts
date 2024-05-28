#!pip install qrcode[pil] pillow

import qrcode
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import tkinter as tk
from tkinter import filedialog

# Función para generar código QR
# Ejemplo de uso
#generar_qr('https://example.com', 'qrcode.png')
def generar_qr(data, box_size=10, border=4, filename=False):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    if(filename):
        save_img(img, filename)
    return img

#Separamos el save_img con tal de poder usar "generar_qr" sin guardar la imagen.
def save_img(img, filename):
    img.save(filename)



# Ejemplo de uso
#generar_qr_personalizado('https://example.com', 'logo.png', 'qrcode_personalizado.png')
def generar_qr_personalizado(data, logo_path, filename):
    
    # Generar el código QR básico
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Crear la imagen QR
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    logo = Image.open(logo_path)
    qr_width, qr_height = img.size
    logo_size = int(min(qr_width, qr_height) * 0.2)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Crear una máscara con esquinas redondeadas
    mask = Image.new("L", (logo_size, logo_size), 0)
    draw = ImageDraw.Draw(mask)
    radius = int(logo_size * 0.2)  # Radio para las esquinas redondeadas
    draw.rounded_rectangle([(0, 0), (logo_size, logo_size)], radius=radius, fill=255)
    
    logo_with_round_corners = Image.new("RGBA", (logo_size, logo_size))
    logo_with_round_corners.paste(logo, (0, 0), mask)

    # Centrar el logo en el QR
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    img.paste(logo_with_round_corners, pos, mask=logo_with_round_corners)

    img.save(filename)

def generar_qr_con_fondo(data, background_path, output_path, transparency=0.5):
    # Generar el código QR básico
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="transparent").convert('RGBA')
    qr_width, qr_height = qr_img.size
    
    # Abrir y redimensionar el fondo
    background = Image.open(background_path).convert('RGBA')
    background = background.resize((qr_width, qr_height), Image.Resampling.LANCZOS)
    
    # Ajustar la opacidad del fondo
    alpha = background.split()[3]  # Obtener el canal alfa
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)  # Ajustar la opacidad
    background.putalpha(alpha)
    
    # Crear una imagen blanca del mismo tamaño
    white_bg = Image.new("RGBA", (qr_width, qr_height), (255, 255, 255, 255))
    
    # Combinar el fondo blanco con la imagen de fondo semi-transparente
    combined_bg = Image.alpha_composite(white_bg, background)
    
    # Combinar el QR con el fondo combinado
    combined = Image.alpha_composite(combined_bg, qr_img)
    
    # Guardar la imagen final
    combined.save(output_path)


def crear_qr_desde_ui(data):

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Pedir al usuario que ingrese la URL o texto
    #data = simpledialog.askstring("Entrada", "Info del QR")

    # Pedir al usuario que seleccione el logo
    logo_path = filedialog.askopenfilename(title="Seleccione el logo")

    # Pedir al usuario que seleccione la carpeta de destino
    save_path = filedialog.asksaveasfilename(title="Guardar como", defaultextension=".png")

    if data and logo_path and save_path:
        generar_qr_personalizado(data, logo_path, save_path)
        aplicar_efectos(save_path, save_path.replace(".png", "_artistic.png"))
        print("QR generado y guardado en", save_path)



def delete_whites(img):
    # Convertir el fondo blanco a transparente
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):  # Encontrar color blanco
            new_data.append((255, 255, 255, 0))  # Cambiar a transparente
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

# Agregamos un fondo semi transparente y recortamos los bordes.
def render_background(img, background_path, transparency, width, height):
    
    # Abrir y redimensionar el fondo
    background_path = Image.open(background_path).convert('RGBA')
    background_path = background_path.resize((width, height), Image.Resampling.LANCZOS)

    # Ajustar la opacidad del fondo
    alpha = background_path.split()[3]  # Obtener el canal alfa
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)  # Ajustar la opacidad
    background_path.putalpha(alpha)

    # Crear una imagen blanca del mismo tamaño
    white_bg = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    # Combinar el fondo blanco con la imagen de fondo semi-transparente
    combined_bg = Image.alpha_composite(white_bg, background_path)

    # Combinar el QR con el fondo combinado
    combined = Image.alpha_composite(combined_bg, img)

    # Aplicar una máscara circular para recortar el fondo exterior al círculo
    mask_circle = Image.new('L', combined.size, 0)
    draw_circle = ImageDraw.Draw(mask_circle)
    draw_circle.ellipse((0, 0, combined.size[0], combined.size[1]), fill=255)
    combined.putalpha(mask_circle)
    return combined

def insert_logo(img, logo_path, width, height, size=12):
    logo_path = logo_path
    size = size/100 #%
    logo = Image.open(logo_path)
    logo_size = int(min(width, height) * size)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Crear una máscara con esquinas redondeadas
    mask = Image.new("L", (logo_size, logo_size), 0)
    draw = ImageDraw.Draw(mask)
    radius = int(logo_size * 0.2)  # Radio para las esquinas redondeadas
    draw.rounded_rectangle([(0, 0), (logo_size, logo_size)], radius=radius, fill=255)

    logo_round_corners = Image.new("RGBA", (logo_size, logo_size))
    logo_round_corners.paste(logo, (0, 0), mask)

    # Centrar el logo en el QR
    pos = ((width - logo_size) // 2, (height - logo_size) // 2)
    img.paste(logo_round_corners, pos, mask=logo_round_corners)
    return img


def vcardtemplate_insert_qr(qr, template_path, size=482, position=(26, 1188)):
    # Open the template and the QR code images
    template = Image.open(template_path)

    # Resize QR code to fit in the red circle area
    qr_code_resized = qr.resize((size, size))

    # Paste the QR code onto the template
    template.paste(qr_code_resized, position, qr_code_resized)

    return template

def vcardtemplate_insert_picture(pic_path, template, size=624, position=(228, 215)):
    # Open the picture
    pic = Image.open(pic_path).convert("RGBA")

    # Resize picture to fit the specified size
    pic_resized = pic.resize((size, size))

    pic_circular = image_circle_cut(pic_resized, size)

    # Paste the circular picture onto the template
    template.paste(pic_circular, position, pic_circular.split()[3])  # Use the alpha channel as the mask

    return template

def image_circle_cut(img, size):
    # Create a mask for the circular cropping
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Apply the mask to create a circular image
    pic_circular = Image.new("RGBA", (size, size))
    pic_circular.paste(img, (0, 0), mask)
    return pic_circular

def generate_vcardV3(background_path, vcard_info, transparency=0.3):
    import random

    # Tamaño de la imagen, se asume mismo tamaño para pixeles. Borde del QR.
    pixel_size = 20 # Este es el tamaño del pixel definido en box_size y hacemos el QR en torno a ese tamaño.

    borde = 0
    # Generar el código QR para la vCard
    img_qr = generar_qr(vcard_info.strip(), pixel_size, borde)

    # Ajustamos la imagen para que el QR sea 65% del tamaño.
    qr_width, qr_height = img_qr.size
    bg_width = int(qr_width // 0.65)
    bg_height = int(qr_height // 0.65)

    # Crear el fondo con puntos aleatorios del mismo tamaño que los píxeles del QR
    bg_img = Image.new('L', (bg_width, bg_height), 255)  # Fondo blanco en escala de grises
    draw = ImageDraw.Draw(bg_img)

    # Creamos patrón similar al QR de fondo.
    num_points = (bg_width * bg_height) // (pixel_size * pixel_size * 2)  # Ajustar la densidad de puntos según sea necesario
    for _ in range(num_points):
        x = random.randint(0, (bg_width // pixel_size) - 1) * pixel_size
        y = random.randint(0, (bg_height // pixel_size) - 1) * pixel_size
        draw.rectangle([x, y, x + pixel_size - 1, y + pixel_size - 1], fill=0)  # Dibujar puntos del tamaño de los píxeles del QR

    # Superponer el nuevo QR sobre el fondo con un espacio de 2 píxeles
    render = bg_img.copy()
    qr_center_x = (bg_width - img_qr.size[0]) // 2
    qr_center_y = (bg_height - img_qr.size[1]) // 2

    # Crear una imagen en blanco del tamaño del QR con un borde de 2 píxeles
    qr_with_gap = Image.new('L', (img_qr.size[0] + 4, img_qr.size[1] + 4), 255)
    qr_with_gap.paste(img_qr, (2, 2))

    # Incrustamos el QR sobre el patrón
    render.paste(qr_with_gap, (qr_center_x - 2, qr_center_y - 2))

    # Crear una imagen circular con el QR en el centro y el fondo de puntos aleatorios con un borde negro
    output = Image.new('L', (bg_width, bg_height), 255)  # Fondo blanco
    mask = Image.new('L', (bg_width, bg_height), 0)  # Máscara negra

    # Dibujar un círculo blanco en la máscara
    draw_mask = ImageDraw.Draw(mask)
    center_x, center_y = bg_width // 2, bg_height // 2
    radius = min(bg_width, bg_height) // 2 - 10  # Ajustar para agregar el borde negro
    draw_mask.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)

    # Aplicar la máscara circular a la imagen final
    output.paste(render, (0, 0), mask)

    # Dibujar el borde negro
    draw_final = ImageDraw.Draw(output)
    draw_final.ellipse((center_x - radius - 10, center_y - radius - 10, center_x + radius + 10, center_y + radius + 10), outline=0, width=20)

    # Convertir el fondo blanco a transparente
    output = delete_whites(output)

    output = render_background(output, background_path, transparency, bg_width, bg_height)

    path = 'output/VcardV3.png'
    output.save(path)
    return output

def add_text_to_image(img, text, position, font_path="./ttf/arial.ttf", font_size=35):
    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    if(position[0] == False):
        # Calculate the width of the text to be added
        text_width = draw.textlength(text, font=font)

        # Calculate X position of the text to be centered horizontally with margin
        x = (img.width - text_width) / 2
        position = (x, position[1])
    # Add text to the image
    draw.text(position, text, font=font, fill="black")  # You can change the fill color if needed

    return img

def check_font_size(img, text, margin, initial_font_size=35, font_path="arial.ttf"):
    draw = ImageDraw.Draw(img)
    font_size = initial_font_size
    max_width = img.width - 2 * margin  # Apply margin to both sides
    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textlength(text, font=font)
        if text_width <= max_width:
            break
        font_size -= 1  # Decrease font size until the text fits within max_width

    return font_size-5

def create_vcard_object(nombre="", apellido="", organizacion="",
                        titulo="", telefono_trabajo="", telefono_personal="",
                        email="", direccion="", sitio_web="",
                        fecha_nacimiento="", aniversario="",
                        nota=""):
    import vobject
    nombre_completo = f"{nombre} {apellido}"
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=apellido, given=nombre)
    vcard.add('fn')
    vcard.fn.value = nombre_completo
    vcard.add('org')
    vcard.org.value = [organizacion]
    vcard.add('title')
    vcard.title.value = titulo
    if telefono_trabajo:
        tel_work = vcard.add('tel')
        tel_work.type_param = 'WORK,VOICE'
        tel_work.value = telefono_trabajo
    if telefono_personal:
        tel_home = vcard.add('tel')
        tel_home.type_param = 'HOME,VOICE'
        tel_home.value = telefono_personal
    vcard.add('email')
    vcard.email.value = email
    if direccion:
        adr = vcard.add('adr')
        adr.type_param = 'WORK'
        adr.value = vobject.vcard.Address(street=direccion)
    if sitio_web:
        url = vcard.add('url')
        url.value = sitio_web
    if fecha_nacimiento:
        bday = vcard.add('bday')
        bday.value = fecha_nacimiento
    if aniversario:
        anniv = vcard.add('anniversary')
        anniv.value = aniversario
    if nota:
        note = vcard.add('note')
        note.value = nota

    # Generar el string vCard
    return vcard.serialize()
