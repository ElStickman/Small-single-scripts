#We ask for a string, we start creating random SHA256 until we get a hash that has the string.
#Mode of use:
#String inserted: "test"
#Return : "El hash SHA256 que contenga {String Ingresado} es: {String Generado}' y el hash es {Hash generado que contenga el string ingresado.}'
import hashlib
import random
import string


stringToSearch = input(f"String to create in a Hash: ")
#stringToSearch = "b00da"
def crear_hash_sha256(texto):
    # Crear un objeto hash SHA256
    hash_objeto = hashlib.sha256()
    # Codificar el texto a bytes y actualizar el objeto hash
    hash_objeto.update(texto.encode('utf-8'))
    # Obtener el hash en formato hexadecimal
    hash_hexadecimal = hash_objeto.hexdigest()
    return hash_hexadecimal

def generarate_random_string(longitud):
    # Caracteres que estarán en el string
    caracteres = string.ascii_letters + string.digits
    # string aleatorio dependiendo del largo deseado
    random_string = ''.join(random.choice(caracteres) for _ in range(longitud))
    return random_string

found = False
#Tomar en cuenta que el único motivo del porqué no deje un "parar a los X intentos" es porque demoraba muy poco.
while (not found):
    #Por qué 3? No hay razón. Si hubiera demorado más, habría usado otra función para aumentar el n°
    randomString = "buda"+generarate_random_string(3)
    hash = crear_hash_sha256(randomString)
    if(stringToSearch in hash):
        found = True
        print(f"El hash SHA256 que contenga '{stringToSearch}' es: '{randomString}' y el hash es '{hash}'")