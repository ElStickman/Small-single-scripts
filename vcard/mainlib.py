#!pip install qrcode[pil] pillow
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

def generar_qr(data, box_size=10, border=1, filename=False):
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import CircleModuleDrawer
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Use CircleModuleDrawer for circular modules
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=CircleModuleDrawer())
    if filename:
        img.save(filename)
    return img

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
    template.paste(pic_circular, position, pic_circular.split()[3])

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

    pixel_size = 20
    borde = 0
    img_qr = generar_qr(vcard_info.strip(), pixel_size, borde)

    qr_width, qr_height = img_qr.size
    percentage_size = .68
    bg_width = int(qr_width // percentage_size)
    bg_height = int(qr_height // percentage_size)

    bg_img = Image.new('L', (bg_width, bg_height), 255)
    draw = ImageDraw.Draw(bg_img)
    colorcode = 50

    qr_center_x = (bg_width - img_qr.size[0]) // 2
    qr_center_y = (bg_height - img_qr.size[1]) // 2
    # We create an artificial border, so dots don't collide
    qr_area = (qr_center_x - 15, qr_center_y - 15, qr_center_x + qr_width+6, qr_center_y + qr_height + 6)
    for x in range(0, bg_width, pixel_size):
        for y in range(0, bg_height, pixel_size):
            if random.random() < 0.7:
                if not (qr_area[0] <= x <= qr_area[2] and qr_area[1] <= y <= qr_area[3]):
                    draw.ellipse([x, y, x + pixel_size - 1, y + pixel_size - 1], fill=colorcode+random.randint(0,200))

    render = bg_img.copy()
    
    qr_with_gap = Image.new('L', (img_qr.size[0], img_qr.size[1]), 255)
    qr_with_gap.paste(img_qr, (0, 0))

    render.paste(qr_with_gap, (qr_center_x, qr_center_y))

    output = Image.new('L', (bg_width, bg_height), 255)
    mask = Image.new('L', (bg_width, bg_height), 0)

    draw_mask = ImageDraw.Draw(mask)
    center_x, center_y = bg_width // 2, bg_height // 2
    radius = min(bg_width, bg_height) // 2 - 10
    draw_mask.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)

    output.paste(render, (0, 0), mask)

    draw_final = ImageDraw.Draw(output)
    draw_final.ellipse((center_x - radius - 10, center_y - radius - 10, center_x + radius + 10, center_y + radius + 10), outline=0, width=20)

    output = delete_whites(output)

    output = render_background(output, background_path, transparency, bg_width, bg_height)

    #path = 'output/VcardV3.png'
    #output.save(path)
    return output

def add_text_to_image(img, text, position, font_path="./ttf/arial.ttf", font_size=35, fill="black"):
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
    draw.text(position, text, font=font, fill=fill)  # You can change the fill color if needed

    return img

# Función para revisar el texto entrará en la imagen. No queremos que el nombre salga de la imagen.
def check_font_size(img, text, margin, initial_font_size=35, font_path="./ttf/arial.ttf"):
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

# nota: perfectamente se puede hacer un string.
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
    if organizacion:
        vcard.add('org')
        vcard.org.value = [organizacion]
    if titulo:
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
    if email:
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

def delete_pycache():
    import shutil
    import os
    pycache_dir = '__pycache__'
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir)
        print(f"Deleted {pycache_dir} directory")
    else:
        print(f"{pycache_dir} directory does not exist")