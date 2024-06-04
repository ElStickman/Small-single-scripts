import mainlib
import vcardparams

#pip install qrcode[pil] vobject
background = vcardparams.background_path
# Información de la vCard
vcard_info = vcardparams.vcard_info


# Generar el QR de la vCard
mainlib.generar_qr(vcard_info, filename='output/qrcode.png')

# Opcional: Generar QR personalizado con logo
mainlib.generar_qr_personalizado(vcard_info, background, 'output/VcardV2Logo.png')

#Generar vcard con selector de archivos.
#vcardlib.crear_qr_desde_ui(vcard_string)

mainlib.generar_qr_con_fondo(vcard_info, background, "output/VCardV2bg.png", transparency=0.5)