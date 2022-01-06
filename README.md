# Modbus Server

## Instalación

```bash
sudo pip install -r requirements.txt
```

## Configuración

Variables de ambientes definidos en archivo ```.env```.

| Variable | Descripción |
|---|---|
| ```MODBUS_PORT``` | Puerto del servidor Modbus |
| ```MONGO_PORT``` | Puerto de MongoDB |
| ```MONGO_USER``` | Usuario de MongoDB, sólo si se inicia con la opción --auth |
| ```MONGO_PASS``` | Contraseña de MongoDB, sólo si se inicia con la opción --auth |
| ```MONGO_POLL``` | Polling en minutos que se hace a la colección |
| ```LOG_LEVEL``` | Nivel de log: INFO|DEBUG |
| ```TIMESTAMP_GTE``` | Tiempo en minutos que se usa para buscar los registros más antiguos. |

Ejemplo de archivo .env

```
MODBUS_PORT=5020
MONGO_USER=test
MONGO_PASS=test
MONGO_PORT=27017
MONGO_POLL=10
LOG_LEVEL=DEBUG
TIMESTAMP_GTE=1
```

## Ejecución

Ejecución del servicio sin autenticación de Mongo DB.

```bash
$ python src/index.py
```

Ejecución del servicio con autenticación de Mongo DB.

```bash
$ python src/index.py --auth
```

## Administración MongoDB

```bash
sudo systemctl status|stop|restart|start|disable|enable mongodb
```

```bash
sudo systemctl status mongodb
```

## Referencias

- [Documentación Modbus](https://pymodbustcp.readthedocs.io)
- [Instalar MongoDB en Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/como-instalar-mongodb-en-ubuntu-18-04-es)
- [Instalar PostreSQL en Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/como-instalar-y-utilizar-postgresql-en-ubuntu-18-04-es)
