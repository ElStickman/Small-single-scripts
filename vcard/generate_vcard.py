import mainlib
import params.vcardposinfo as vcardposinfo
import params.clientslist as clientslist

#Fondo del QR. 
background_path = 'background/profilepic.png'
transparency = 0.5 # 0 < transparency <1 

# Lista de parametros a ejecutar
vcardtypelist = vcardposinfo.vcardslist
vcardparams = vcardposinfo.params
clients = clientslist.clients
for clientinfo in clients:
    # Información de la vCard
    if clientinfo['nombre']:
        nombre = clientinfo['nombre']
    else:
        nombre = "addclientinfo"
    if clientinfo['apellido']:
        apellido = clientinfo['apellido']
    else:
        nombre = "addclientinfo"
    if clientinfo['titulo']:
        titulo = clientinfo['titulo']
    else:
        titulo = "ChangeMeNameTitulo"
    if clientinfo['phono']:
        telefono_personal = clientinfo['phono']
    else:
        telefono_personal = "ChangeMeNameTitulo"
    email = "Email@falso.cl"
    if clientinfo['email']:
        email = clientinfo['email']
    else:
        email = "ChangeMeNameTitulo"
    if clientinfo['sitioweb']:
        sitio_web = clientinfo['sitioweb']
    else:
        sitio_web = False
    telefono_trabajo = False
    organizacion = False #"ElStickman codes"
    nombre_completo = f"{nombre} {apellido}"
    direccion = False  # Calle Falsa 123;Springfield;SP;12345;EEUU
    fecha_nacimiento = False  # 1995-03-21
    aniversario = False  # 2005-04-02
    nota = False  # Información adicional aquí
    vcard_info = mainlib.create_vcard_object(nombre, apellido, organizacion,
                            titulo, telefono_trabajo, telefono_personal,
                            email, direccion, sitio_web,
                            fecha_nacimiento, aniversario,
                            nota)
    profile_pic = f'background/{clientinfo['profilepicname']}.png'
    #Generamos todas las Vcards de la lista.

    for vcardtype in vcardtypelist:
        #Si no hay sitioweb, omitimos los formatos que tengan "sitioweb"
        if(vcardtype[-1] == "0" and sitio_web == False):
            print(f"Omitiendo formato con sitio web. (No se encontró sitio web) {vcardtype}")
            continue
        print(f"Generando VcardV3 con template {vcardtype}")
        qr = mainlib.generate_vcardV3(background_path, 
                                vcard_info, 
                                transparency=transparency)
        print("Insertando en template")
        vcard = mainlib.vcardtemplate_insert_qr(qr,
                                        f'./VCardTemplates/VCardTemplate{vcardtype}.png',
                                        size=482,
                                        position=(vcardparams[vcardtype[0]]['qrposX'], vcardparams[vcardtype[0]]['qrposY'])
                                        )
        print("Insertando foto de perfil")
        vcard = mainlib.vcardtemplate_insert_picture(profile_pic,
                                        vcard,
                                        size=vcardparams[vcardtype[0]]['profilepixsize'],
                                        position=(vcardparams[vcardtype[0]]['profilepicposX'], vcardparams[vcardtype[0]]['profilepicposY']))
        print("Agregando texto")
        #El texto de contacto depende del tipo de template.
        if (vcardtype[-1] == 1):
            #page
            vcard = mainlib.add_text_to_image(vcard, 
                                                sitio_web, 
                                                font_path="./ttf/Roboto-Regular.ttf",
                                                position=(vcardparams[vcardtype[0]]['infoposX'], vcardparams[vcardtype[0]]['pageposY']),
                                                fill=vcardparams[vcardtype[0]]['textcolor'])
        #Phone
        vcard = mainlib.add_text_to_image(vcard, 
                                            telefono_personal, 
                                            font_path="./ttf/Roboto-Regular.ttf",
                                            font_size=vcardparams[vcardtype[0]]['phonefontsize'],
                                            position=(vcardparams[vcardtype[0]]['infoposX'], vcardparams[vcardtype[0]][f'phoneposY{vcardtype[-1]}']),
                                            fill=vcardparams[vcardtype[0]]['textcolor'])
        #Email
        if(email) : 
            vcard = mainlib.add_text_to_image(vcard, 
                                                email, 
                                                font_path="./ttf/Roboto-Regular.ttf",
                                                font_size=vcardparams[vcardtype[0]]['emailfontsize'],
                                                position=(vcardparams[vcardtype[0]]['infoposX'], vcardparams[vcardtype[0]][f'emailposY{vcardtype[-1]}']),
                                                fill=vcardparams[vcardtype[0]]['textcolor'])
        #Agregamos nombre.
        name = nombre_completo
        #revisamos que el nombre entre en la imagen.
        font_size = mainlib.check_font_size(vcard, name, margin=20,
                                            font_path="./ttf/Roboto-Regular.ttf",
                                            initial_font_size=90)
        vcard = mainlib.add_text_to_image(vcard, 
                                        name, 
                                        font_path="./ttf/Roboto-Regular.ttf",
                                        position=(False, vcardparams[vcardtype[0]]['nameposY']),
                                        font_size=font_size,
                                        fill=vcardparams[vcardtype[0]]['textcolor'])
        #Sub titulo / cargo
        cargo = titulo
        # Revisamos que el nombre del cargo entre en la imagen.
        font_size = mainlib.check_font_size(vcard, cargo, margin=20,
                                            font_path="./ttf/Roboto-Regular.ttf",
                                            initial_font_size=90)
        vcard = mainlib.add_text_to_image(vcard, 
                                        cargo, 
                                        font_path="./ttf/Roboto-Regular.ttf",
                                        position=(False, vcardparams[vcardtype[0]]['tittleposY']),
                                        font_size=font_size*.8,
                                        fill=vcardparams[vcardtype[0]]['textcolor'])
        vcard.save(f'output/{nombre}_{apellido}_Vcard{vcardtype}.png')

print("Eliminando Caché")
mainlib.delete_pycache()
