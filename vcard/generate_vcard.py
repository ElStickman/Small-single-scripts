import mainlib


#Changeme
background_path = 'background/profilepic.png'
profile_pic = 'background/profilepic.png'

# //TODO: Hacerlo comaptible con CSV.
# Información de la vCard
nombre = "ElStickman"
apellido = "Apellido"
nombre_completo = f"{nombre} {apellido}"
organizacion = False #"ElStickman codes"
titulo = ""
telefono_trabajo = False
telefono_personal = "+56912341234"
email = False #"Email@falso.cl"
direccion = False  # Calle Falsa 123;Springfield;SP;12345;EEUU
sitio_web = False
fecha_nacimiento = False  # 1995-03-21
aniversario = False  # 2005-04-02
nota = False  # Información adicional aquí
vcard_info = mainlib.create_vcard_object(nombre, apellido, organizacion,
                        titulo, telefono_trabajo, telefono_personal,
                        email, direccion, sitio_web,
                        fecha_nacimiento, aniversario,
                        nota)
titulo = "Programador"
# Lista de archivos a ejecutar
vcardtype = 3
print(f"Generando VcardV3 con template {vcardtype}")
print("Generando VCard QR")

qr = mainlib.generate_vcardV3(background_path, 
                          vcard_info, 
                          transparency=0)
print("Insertando en template")
vcard = mainlib.vcardtemplate_insert_qr(qr,
                                 f'./background/VCardTemplate{vcardtype}.png',
                                 size=482,
                                 position=(26, 1188)
                                 )
print("Insertando foto de perfil")
vcard = mainlib.vcardtemplate_insert_picture(profile_pic,
                                 vcard,
                                 size=624,
                                 position=(228, 215))
print("Agregando texto")
#El texto de contacto depende del tipo de template.
if (vcardtype == 1):
    y_phone = 1333
    y_email = 1405
    #page
    vcard = mainlib.add_text_to_image(vcard, 
                                        "222.www.333", 
                                        font_path="./ttf/Roboto-Regular.ttf",
                                        position=(666, 1485))
else:
    y_phone = 1373
    y_email = 1445
#Phone
vcard = mainlib.add_text_to_image(vcard, 

                                    "+569 1234 1234", 
                                    font_path="./ttf/Roboto-Regular.ttf",
                                    position=(666, y_phone))
#Email
vcard = mainlib.add_text_to_image(vcard, 
                                    "fake@email", 
                                    font_path="./ttf/Roboto-Regular.ttf",
                                    position=(666, y_email))
#Agregamos nombre.
name = nombre_completo
#revisamos que el nombre entre en la imagen.
font_size = mainlib.check_font_size(vcard, name, margin=20,
                                     font_path="./ttf/Roboto-Regular.ttf",
                                     initial_font_size=90)
print(font_size)
vcard = mainlib.add_text_to_image(vcard, 
                                   name, 
                                   font_path="./ttf/Roboto-Regular.ttf",
                                   position=(False, 902),
                                   font_size=font_size)
#Sub titulo / cargo
cargo = titulo
# Revisamos que el nombre del cargo entre en la imagen.
font_size = mainlib.check_font_size(vcard, cargo, margin=20,
                                     font_path="./ttf/Roboto-Regular.ttf",
                                     initial_font_size=90)
vcard = mainlib.add_text_to_image(vcard, 
                                   cargo, 
                                   font_path="./ttf/Roboto-Regular.ttf",
                                   position=(False, 1050),
                                   font_size=font_size*.8)
vcard.save('output/templateVcard.png')

print("Eliminando Caché")
mainlib.delete_pycache()