#!/usr/bin/env python
# coding: utf-8

# Uploaded by ElStickman; Used on Jupyter Computers

# in [1]:
#!pip3 install pillow qrcode numpy

# in [2]:
import numpy as np
from PIL import Image, ImageDraw
import qrcode

# Información de la vCard
nombre = "Alejandro"
apellido = "Donoso"
nombre_completo = f"{nombre} {apellido}"
organizacion = "ElStickman codes"
titulo = "Dueño"
telefono_trabajo = ""
telefono_personal = "+569"
email = "Email@falso.cl"
direccion = "" #Calle Falsa 123;Springfield;SP;12345;EEUU"
sitio_web = ""
fecha_nacimiento = "" #"1995-03-21"
aniversario = "" #2005-04-02"
nota = "" #"Información adicional aquí"

vcard_info = f"""
BEGIN:VCARD
VERSION:3.0
N:{apellido};{nombre};;;
FN:{nombre_completo}
ORG:{organizacion}
TITLE:{titulo}
TEL;TYPE=WORK,VOICE:{telefono_trabajo}
{f'TEL;TYPE=HOME,VOICE:{telefono_personal}' if telefono_personal else ''}
EMAIL:{email}
ADR;TYPE=WORK:{direccion}
URL:{sitio_web}
BDAY:{fecha_nacimiento}
ANNIVERSARY:{aniversario}
NOTE:{nota}
END:VCARD
""".strip()

print(vcard_info)

# Parámetros para el diseño
radio_qr = 350
radio_exterior = radio_qr *2
radio_total = radio_exterior + 2
grosor_borde = 2
color_borde = 'black'

# Generación del código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=1,
)
qr.add_data(vcard_info)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Creación de la imagen de fondo
img_fondo = Image.new('RGB', (radio_total * 2, radio_total * 2), 'white')
dibujo_fondo = ImageDraw.Draw(img_fondo)

for i in range(20000):
    angle = .2*i
    r = angle
    point_x = int(radio_total + r * np.cos(angle))
    point_y = int(radio_total + r * np.sin(angle))
    dot = 4*3 #* np.random.uniform(1, 3)
    dibujo_fondo.rectangle([point_x, point_y, point_x + dot, point_y + dot], fill='black')

# Añadir el borde
dibujo_fondo.ellipse(
    [2, 2, radio_total * 2 - 2, radio_total * 2 - 2],
    outline=color_borde,
    width=grosor_borde*2
)

# Colocar el QR en la imagen
img_fondo.paste(qr_img, (radio_total - qr_img.size[0] // 2, radio_total - qr_img.size[1] // 2))

# Aplicar la máscara circular
mask_circular = Image.new('L', (radio_total * 2, radio_total * 2), 0)
dibujo_mask = ImageDraw.Draw(mask_circular)
dibujo_mask.ellipse((0, 0, radio_total * 2, radio_total * 2), fill=255)

img_final = Image.new('RGB', (radio_total * 2, radio_total * 2), (255, 255, 255))
img_final.paste(img_fondo, mask=mask_circular)

# Guardar la imagen
img_final_path = "VCard.png"
img_final.save(img_final_path)
print(f"Imagen guardada como {img_final_path}")