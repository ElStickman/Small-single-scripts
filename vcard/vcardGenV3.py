from PIL import Image, ImageDraw
import random
import vcardparams
import vcardlib

#pip install qrcode[pil] vobject
background_path = vcardparams.background_path
logo_path = vcardparams.logo_path
transparency = 0.6
# Información de la vCard
vcard_info = vcardparams.vcard_info

# Tamaño de la imagen, se asume mismo tamaño para pixeles. Borde del QR.
pixel_size = 20 # Este es el tamaño del pixel definido en box_size y hacemos el QR en torno a ese tamaño.

borde = 0
# Generar el código QR para la vCard
img_qr = vcardlib.generar_qr(vcard_info.strip(), pixel_size, borde)

# Crear el fondo con puntos aleatorios del mismo tamaño que los píxeles del QR
bg_width = img_qr.size[0] * (pixel_size // 10)
bg_height = img_qr.size[1] * (pixel_size // 10)
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
output = vcardlib.delete_whites(output)

output = vcardlib.render_background(output, background_path, transparency, bg_width, bg_height)

path = 'output/VcardV3.png'
output.save(path)


#Generamos mismo QR pero con logo al centro.
output = vcardlib.insert_logo(output, logo_path, bg_width, bg_height, size=12)
print("Generando Vcard 3.1")
output.save('output/VcardV3logo.png')