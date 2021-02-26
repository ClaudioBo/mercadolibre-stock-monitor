from playsound import playsound
from colorama import Fore, init
init()
import requests, sys, time, json, datetime, random

API_URL = "https://api.mercadolibre.com/items/"
demo = False

i = 0
j = 5
up = True

try:
    if(len(sys.argv) == 2):
        if(sys.argv[1].lower() != 'demo'):
            API_URL += sys.argv[1]
        else:
            demo = True
    else:
        raise Exception()
except Exception as e:
    print("Uso correcto: python stockmonitor.py <id-publicacion>")
    exit()

precio = None
stock_disponible = None
diferencia_precio = None
while(True):
    now = datetime.datetime.now().strftime("%X")

    webdata = None
    try:
        if(demo):
            #Probar sin api
            pricerand = i+random.randrange(2,10) if up else i-random.randrange(2,10)
            stockrand = i-random.randrange(10,20) if up else i+random.randrange(10,20)
            webdata = {
                'price':pricerand,
                'available_quantity':stockrand,
                'status':'live'
            }
            i = webdata['price']
            j-=1
            if(j <= 0):
                j = random.randrange(3,6)
                up = not up
        else:
            req = requests.get(API_URL,timeout=5).text;
            webdata = json.loads(req)
            if('error' in webdata):
                raise Exception("La API retorno el siguiente error: "+webdata['error'])
    except Exception as e:
        print(f"[{now}]: Error:")
        print("  "+str(e))
        time.sleep(10)
        continue
    
    precio_now = webdata['price']
    stock_disponible_now = webdata['available_quantity']

    #inicializar
    if(precio == None):
        precio = precio_now
    if(stock_disponible == None):
        stock_disponible = stock_disponible_now
    
    #comparar precio
    precio_texto = None
    if(precio - precio_now != 0):
        diferencia_precio = ((precio_now-precio)/precio * 100); #obtener diferencia de precio en %
        if(diferencia_precio > 0):
            precio_texto = f'{Fore.GREEN}${precio} [{diferencia_precio}% ▲]{Fore.WHITE}'
        else:
            precio_texto = f'{Fore.RED}${precio} [{diferencia_precio}% ▼]{Fore.WHITE}'
    else:
        precio_texto = f"${precio} [    ]"
    
    #comprobar estados
    status_texto = None
    status = webdata['status']
    if(status != 'paused'):
        status_texto = f'{Fore.GREEN}{status}{Fore.WHITE}'
        playsound('sound.wav')
    else:
        status_texto = f'{Fore.YELLOW}{status}{Fore.WHITE}'
        pass

    #comprobar stock
    stock_texto = None
    if(stock_disponible - stock_disponible_now != 0):
        diferencia_stock = stock_disponible_now - stock_disponible;
        if(diferencia_stock > 0):
            stock_texto = f'{Fore.GREEN}{stock_disponible_now} [+{diferencia_stock} ▲]{Fore.WHITE}'
        else:
            stock_texto = f'{Fore.RED}{stock_disponible_now} [{diferencia_stock} ▼]{Fore.WHITE}'
    else:
        stock_texto = f'{stock_disponible_now} [    ]'

    print(f'[{now}] {status_texto}\t | Stock: {stock_texto}\t | Precio: {precio_texto}')

    #actualizar
    precio = precio_now
    stock_disponible = stock_disponible_now
    
    time.sleep(60)

