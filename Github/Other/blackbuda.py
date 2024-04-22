#Las comisiones se cobran en CLP.
#Para todos los cálculos utilizar el horario entre 12:00 y 13:00, ambos inclusive, considera la zona horaria GMT -03:00.
#Para todas las respuestas truncar en 2 decimales, ocupando un punto como separador de decimales.
#Recuerda que en un mercado del tipo Moneda_1-Moneda_2, la cantidad transada está en Moneda_1 y el precio en Moneda_2.


import requests # install requests with `pip install requests`
import json


market_id = 'btc-clp'

url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'


hora12pm = 1709305200000
hora13pm = 1709308800000
hora13pm2023 = 1677686400000
hora12pm2023 = 1677682800000
#NOTA. LA API funciona desde el timestamp hacia atrás. 

def get_trades(hora): #, horainicio) : comentado por que last_timestamp no parece funcionar correctamente.
    response = requests.get(url, params={
        #Timestamp in milliseconds??
        'timestamp': (hora), 
        #'last_timestamp': int(hora12pm), #Este campo no parece funcionar correctamente.
        #'limit' : 100 #Dado que last_timestamp no funciona correctamente (parece), traeremos el máximo que podamos.

    })
    return response.json()
#Suma de todas las transacciones ocurridas en el tiempo seleccionado
def evaluar_dinero_CLP(horafin, horainicio):
    total = 0
    while (horafin > horainicio):
        data = get_trades(horafin)
        horafin = int(data['trades']['last_timestamp'])
        entries = data['trades']['entries']
        for entrie in entries:
            if(int(entrie[0]) > int(horainicio)):
                #sumamos el precio * cantidad. Da lo mismo la dirección.
                total += (float(entrie[1])*float(entrie[2]))
    return int(total * 100) / 100.0
#suma de las comisiones por transacción.
def evaluar_comision_CLP(horafin, horainicio):
    total = 0
    while (horafin > horainicio):
        data = get_trades(horafin)
        horafin = int(data['trades']['last_timestamp'])
        entries = data['trades']['entries']
        for entrie in entries:
            if(int(entrie[0]) > int(horainicio)):
                #sumamos el precio * 0.8%. Da lo mismo la dirección.
                total += (float(entrie[1])*float(entrie[2]))*0.008
    return int(total * 100) / 100.0

#Suma de BTC transado.
def evaluar_dinero_BTC(horafin, horainicio):
    total = 0
    while (horafin > horainicio):
        data = get_trades(horafin)
        horafin = int(data['trades']['last_timestamp'])
        entries = data['trades']['entries']
        for entrie in entries:
            if(int(entrie[0]) > int(horainicio)):
                #sumamos la cantidad. Da lo mismo la dirección.
                total += (float(entrie[1]))
    return int(total * 100) / 100.0

print("Inicio:")
print()
dinerotransado2024 = evaluar_dinero_CLP(hora13pm, hora12pm)

print(f"Dinero transado 2024: {dinerotransado2024}")

#print("Nueva iteración, 2023 VS 2024.")
BTCtransado2024 = evaluar_dinero_BTC(hora13pm, hora12pm)
BTCtransado2023 = evaluar_dinero_BTC(hora13pm2023, hora12pm2023)

aumentopercentage = int((BTCtransado2024-BTCtransado2023)/BTCtransado2023*100 * 100) / 100.0
print(f"Comparación vs año pasado = {aumentopercentage}")

comisiones2024 = evaluar_comision_CLP(hora13pm, hora12pm)
print(f"Comisiones estimadas 2024: {comisiones2024}")
print()
print("end")
