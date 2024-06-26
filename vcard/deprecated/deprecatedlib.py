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


def crear_qr_desde_ui(data):
    import tkinter as tk
    from tkinter import filedialog

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