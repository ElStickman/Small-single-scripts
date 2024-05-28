import vobject

#Fondo de la imagen para el QR
background_path = 'background/profilepic.png'
logo_path = background_path

# Información de la vCard
nombre = "ElStickman"
apellido = "Apellido1 Apellido2"
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


# Creación objeto VCARD
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
vcard_info = vcard.serialize()
