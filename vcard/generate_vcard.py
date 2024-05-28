import vcardlib


#Changeme
background_path = 'background/plants.jpg'
profile_pic = 'background/profilepic.png'

# //TODO: Hacerlo comaptible con CSV.
# Información de la vCard
nombre = "ElStickman NOMBRE GIGANTE"
apellido = "Testeo Apellido"
nombre_completo = f"{nombre} {apellido}"
organizacion = "ElStickman codes"
titulo = "Programador"
telefono_trabajo = ""
telefono_personal = "+56912341234"
email = "Email@falso.cl"
direccion = ""  # Calle Falsa 123;Springfield;SP;12345;EEUU
sitio_web = ""
fecha_nacimiento = ""  # 1995-03-21
aniversario = ""  # 2005-04-02
nota = ""  # Información adicional aquí
vcard_info = vcardlib.create_vcard_object(nombre, apellido, organizacion,
                        titulo, telefono_trabajo, telefono_personal,
                        email, direccion, sitio_web,
                        fecha_nacimiento, aniversario,
                        nota)

# Lista de archivos a ejecutar
vcardtype = 1
print(f"Generando VcardV3 con template {vcardtype}")
print("Generando VCard QR")
qr = vcardlib.generate_vcardV3(background_path, 
                          vcard_info, 
                          transparency=0.2)
print("Insertando en template")
vcard = vcardlib.vcardtemplate_insert_qr(qr,
                                 f'./background/VCardTemplate{vcardtype}.png',
                                 size=482,
                                 position=(26, 1188)
                                 )
print("Insertando foto de perfil")
vcard = vcardlib.vcardtemplate_insert_picture(profile_pic,
                                 vcard,
                                 size=624,
                                 position=(228, 215))
print("Agregando texto")
#El texto de contacto depende del tipo de template.
if (vcardtype == 1):
    y_phone = 1333
    y_email = 1405
    #page
    vcard = vcardlib.add_text_to_image(vcard, 
                                        "-------", 
                                        position=(666, 1485))
else:
    y_phone = 1373
    y_email = 1445
#Phone
vcard = vcardlib.add_text_to_image(vcard, 
                                    "---+569 1234 1234", 
                                    position=(666, y_phone))
#Email
vcard = vcardlib.add_text_to_image(vcard, 
                                    "---fake@email", 
                                    position=(666, y_email))
#Agregamos nombre.
name = nombre_completo
font_size = vcardlib.check_font_size(vcard, name, margin=20,
                                     initial_font_size=90)
vcard = vcardlib.add_text_to_image(vcard, 
                                   name, 
                                   position=(False, 902),
                                   font_size=font_size)
#Sub titulo / cargo
cargo = titulo
font_size = vcardlib.check_font_size(vcard, cargo, margin=20,
                                     initial_font_size=90)
vcard = vcardlib.add_text_to_image(vcard, 
                                   cargo, 
                                   position=(False, 1050),
                                   font_size=font_size*.8)
vcard.save('output/templateVcard.png')