from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import os, random as r, requests as req

def gen_key(api_key):
    locations = [
        "36.49730589398675, -117.22675585914209",   #Valle de la Muerte, Estados Unidos
        "-55.98145103544396, -67.26786983189709",   #Cabo de Hornos
        ##############################################################
        "51.46280152761693, -0.11778792200646199",  #Brixton, Reino Unido
        "66.0471751751297, 20.68617902811258",      #Boden, Suecia
        "-2.7597841456107215, -78.88452457401387",  #Cojitambo, Ecuador
        "36.58750410085579, 128.82878848529248",    #Dogok-ri, Corea del Sur
        "13.421789700625325, -15.590211320433085",  #Jiffin, Gambia
        "-32.16673937006628, -55.94541234711305",   #Los Cuadrados, Uruguay
        "-41.03093506728019, -70.26564493257229",   #Comallo, Argentina
        "59.39643202336566, -101.32105941179255",   #Fort Hall, Canada
        "40.77184451702529, -73.96553439644595",    #Manhattan, Estados Unidos
        "19.59236710104776, -71.53759752310779",    #Las Ciruelas, Republica Dominicana
        "13.125653063877952, -59.435964333457974",  #Long Bay, Barbados
        "37.61822243867675, -0.9877360502544119",   #Cartagena, España
        "72.31833892218825, 79.54306078708255",     #Leskino, Rusia
        "32.69896257444341, -117.0773748999877",    #San Diego, Estados Unidos
        "2.2816284451424416, -68.08411592292512",   #Yavico, Colombia
        "-32.447493984878506, 118.86224596504645",  #Hyden, Australia
        "33.10182075107918, 132.9175673483396",     #Kobi, Japon
        "35.638016130417924, 40.7439898572587",     #Hasiba, Siria
        "64.54130033030947, -21.91619025773917",    #Borgarnes, Isnlandia
        "20.665535047125925, -100.23980756175784",  #La Griega, Mexico
        "-44.69393870892623, 169.13631788420045",   #Wanaka, Nueva Zelanda
        "-9.585507068158025, 161.39486720394544",   #Maka, Islas Salomon
        "-4.13858307109717, 153.62476192668763",    #Warambi, Feni Islands
        "-1.3274353640486336, 149.59225513482303",  #Bai, Mussau Island
        "-37.11393988010128, -12.285873645792435",  #Tristan da Cunha
        "-8.95755922830764, -46.851443554682014",   #Taboca, Brasil
        "40.35228666805593, 16.61384721946954",     #Caporotondo, Italia
        "80.16409932403616, 32.24300630718813",     #KvitØya
        "47.26851435543081, -88.42168080849027",    #Calumet, Estados Unidos
        "-17.48893452988811, 178.23670955835732",   #Barotu, Fiyi
    ]
    #Temperatura
    tcds = locations[0]
    tdato = req.get(f"https://api.tomorrow.io/v4/weather/forecast?location={tcds}&apikey={api_key}").json()
    tt = [i["values"]["temperature"] for i in tdato["timelines"]["hourly"]] 
    ta = tt[0]
    tm = sum(tt)/len(tt)
    tmax = max(tt)
    tmin = min(tt)
    tmmax = (tm+tmax)/2
    tmmin = (tm+tmin)/2
    if ta <= tmin: locates = locations[2:][:7]
    elif tmin < ta < tmmin: locates = "min"
    elif tmmin < ta < tm: locates = "minmed"
    elif tm < ta < tmmax: locates = "maxmed"
    elif tmmax < ta < tmax: locates = "max"
    elif tmax <= ta: locates = locations[-7:]
    # Viento
    vcds = locations[1]
    vdato = req.get(f"https://api.tomorrow.io/v4/weather/forecast?location={vcds}&apikey={api_key}").json()
    vt = [i["values"]["windSpeed"] for i in vdato["timelines"]["hourly"]] 
    va = vt[0] 
    vm = sum(vt)/len(vt)
    if type(locates) == str:
        if va <= vm:
            if locates == "min":  locates = locations[2:][:7]
            elif locates == "minmed": locates = locations[8:][:7]
            elif locates == "maxmed": locates = locations[16:][:7]
            elif locates == "max": locates = locations[24:][:7]
        elif va > vm:
            if locates == "min": locates = locations[3:][:7]
            elif locates == "minmed": locates = locations[9:][:7]
            elif locates == "maxmed": locates = locations[17:][:7]
            elif locates == "max": locates = locations[25:][:7]
    
    # Operacion
    operation = ""
    for loc in locates:
        dato = req.get(f"https://api.tomorrow.io/v4/weather/forecast?location={loc}&apikey={api_key}").json()
        print(dato)
        dt = [i["values"]["temperature"] for i in dato["timelines"]["hourly"]] 
        dta = dt[0]
        dtm = sum(dt)/len(dt)
        dtmax = max(dt)
        dtmin = min(dt)
        dtmmax = (dtm+dtmax)/2
        dtmmin = (dtm+dtmin)/2
        if locates.index(loc) == 1 or locates.index(loc) == 3 or locates.index(loc) == 5:
            if dta > dtm:
                if dta > dtmmax: operation += "*"
                else: operation += "+"
            elif dta < dtmmin: operation += "/"
            else: operation += "-"
        else: operation += str(dta)
    return str(eval(operation)).replace(".","")

def create_key(algoritmo, dato='', longitud=256, name=f"clave_{len(os.listdir('tray/'))}"):
    if algoritmo == 'RSA':
        key = RSA.generate(longitud)
        pub_key = key.publickey().export_key()
        priv_key = key.export_key()
        with open(f"tray/{name}.pub.pem", "wb") as f:
            f.write(pub_key)
        with open(f"tray/{name}.pri.pem", "wb") as f:
            f.write(priv_key)
        print("Claves RSA creadas correctamente.")
    elif algoritmo == 'AES':
        key = os.urandom(longitud // 8)
        with open(f"data/secrets/{name}_{dato}.bin", "wb") as f:
            f.write(key)
        print("Clave AES creada correctamente.")
    else:
        print("Algoritmo no válido.")

def get_key(tipo, algoritmo, name, dato):
    try: 
        if algoritmo == 'RSA':
            if tipo == 'pub': 
                with open(f'tray/{name}.pub.pem', 'rb') as pkp: 
                    key = RSA.import_key(pkp.read())
                pkp.close()
            else: 
                with open(f'tray/{name}.pri.pem', 'rb') as pkp:
                    key = RSA.import_key(pkp.read())
                pkp.close()
        elif algoritmo == 'AES':
            with open(f"data/secrets/{name}_{dato}.bin", "rb") as f:
                key = f.read()
    except FileNotFoundError:
        create_key(algoritmo, int(input("Tamaño para la clave. ej: 1024, 4096 >> ")))
        key = get_key(tipo, algoritmo)
    return key

def cifrar(algoritmo, clave, data, dato=''):
    key = get_key('pub', algoritmo, clave, dato)
    if algoritmo == 'RSA':
        data = data.encode()
        cipher_rsa = PKCS1_OAEP.new(key)
        ciphertext = cipher_rsa.encrypt(data)
        return ciphertext
    elif algoritmo == 'AES':
        with open(data, 'rb') as file:
            filepath = data
            data = file.read()
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length
        ciphertext = cipher.encrypt(data)
        with open(f'{filepath}', 'wb') as file_out:
            file_out.write(iv)  
            file_out.write(ciphertext)
    else:
        print("Algoritmo no válido.")
        return None
    
def descifrar(algoritmo, clave, data, dato=''):
    key = get_key('pri', algoritmo, clave, dato)
    if algoritmo == 'RSA':
        cipher_rsa = PKCS1_OAEP.new(key)
        plaintext = cipher_rsa.decrypt(data)
        return plaintext.decode()
    elif algoritmo == 'AES':
        with open(data, 'rb') as file:
            iv = file.read(16)
            ciphertext = file.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]
        with open(data, 'wb') as file_out:
            file_out.write(plaintext)
    else:
        print("Algoritmo no válido.")
        return None