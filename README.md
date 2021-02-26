# mercadolibre-stock-monitor
Script en Python 3.x que verifica constantemente el estado de una publicacion de MercadoLibre por medio de una id
Emitira un sonido si la publicacion no esta pausada (por eso hice este scriptxd)
Muestra que tanto cambia la publicacion su precio y cantidad de stock cada vez que consulta la pagina (cada 60 segundos)

## Pre-requisitos 📋
Python 3.7.x, Colorama, playsound
```
pip install colorama
pip install playsound
```

## Uso ⚙️
```
python stockmonitor.py <id>
```
Ej: id puede ser 'demo' (a base de numeros random) o 'MLM792351232'
_Los argumentos son requeridos_

## Screenshot 📷
![img1](https://i.imgur.com/DeKNL11.png)
