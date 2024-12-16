# LuxuryStay: Sistema de Gestión Centralizada para una Cadena Hotelera

## **Descripción del Proyecto**
LuxuryStay es una cadena hotelera que busca implementar un sistema centralizado para gestionar la disponibilidad de habitaciones, reservas y el inventario de manera eficiente. Este proyecto consta de tres servicios independientes:

1. **Servicio SOAP**: Consulta la disponibilidad de habitaciones por tipo, fechas y estado.
2. **API REST**: Permite crear, consultar y cancelar reservas.
3. **Microservicio de Inventario**: Administra las habitaciones disponibles y actualiza su estado.

Cada servicio cuenta con su propia base de datos y está implementado siguiendo el patrón de invocación remota.

---

## **Arquitectura del Proyecto**

### Servicios Implementados:
1. **Servicio SOAP**:
   - Permite consultar la disponibilidad de habitaciones.
   - Responde en formato XML.
   - Entrada: Fecha de inicio, fecha de fin, tipo de habitación.
   - Salida: Lista de habitaciones disponibles.

2. **API REST**:
   - Endpoints:
     - Crear reserva: `POST /reservations`.
     - Consultar reserva: `GET /reservations/{id}`.
     - Cancelar reserva: `DELETE /reservations/{id}`.

3. **Microservicio de Inventario**:
   - Endpoints:
     - Registrar habitación: `POST /rooms`.
     - Actualizar estado de habitación: `PATCH /rooms/{id}`.

### Bases de Datos:
Cada servicio tiene su propia base de datos:

- **SOAP**: Tabla `availability`.
  - Columnas: `room_id`, `room_type`, `available_date`, `status`.
- **REST**: Tabla `reservations`.
  - Columnas: `reservation_id`, `room_number`, `customer_name`, `start_date`, `end_date`, `status`.
- **Inventario**: Tabla `rooms`.
  - Columnas: `room_id`, `room_number`, `room_type`, `status`.

---

## **Requisitos del Sistema**

### **Pre-requisitos**
1. **Software**:
   - Docker y Docker Compose.
   - Python 3.10 o superior (opcional si no usas Docker).
   - SQL Server 2022 (ejecutado en un contenedor).

2. **Configuración de Red**:
   - Puertos:
     - SOAP: 8000
     - REST: 5000
     - Inventario: 5001
     - SQL Server: 1433

### **Tecnologías Usadas**
- Lenguaje: Python.
- Bases de datos: SQL Server.
- Orquestación: Docker Compose.
- Frameworks:
  - SOAP: Spyne.
  - REST e Inventario: Flask.

---

## **Estructura del Proyecto**
```
project/
|
|-- SOAP/
|   |-- soap_service.py
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- REST/
|   |-- rest_service.py
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- Inventory/
|   |-- inventory_service.py
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- docker-compose.yml
|-- README.md
```

---

## **Configuración del Proyecto**

### **Paso 1: Clonar el Repositorio**
```bash
git clone https://github.com/usuario/luxurystay.git
cd luxurystay
```

### **Paso 2: Configurar Docker Compose**
Levantar los servicios utilizando Docker Compose:
```bash
docker-compose up --build
```
Esto iniciará los contenedores para los tres servicios y la base de datos SQL Server.

### **Paso 3: Verificar la Ejecución**
Asegúrate de que los servicios estén activos:

- SOAP: `http://localhost:8000`
- REST: `http://localhost:5000`
- Inventario: `http://localhost:5001`

### **Paso 4: Conexión a SQL Server (Opcional)**
Puedes conectarte a la base de datos para verificar datos usando un cliente SQL como SQL Server Management Studio (SSMS):

- Servidor: `localhost,1433`
- Usuario: `sa`
- Contraseña: `StrongPassword123!`

---

## **Pruebas**

### **Servicio SOAP**
#### Endpoint: Consultar Disponibilidad
Enviar una consulta SOAP para disponibilidad:
```bash
curl -X POST http://localhost:8000 \
-H "Content-Type: text/xml" \
-d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lux="luxurystay.soap">
       <soapenv:Header/>
       <soapenv:Body>
          <lux:check_availability>
             <start_date>2024-12-20</start_date>
             <end_date>2024-12-22</end_date>
             <room_type>Single</room_type>
          </lux:check_availability>
       </soapenv:Body>
    </soapenv:Envelope>'
```
Respuesta esperada:
```xml
<Availability>
    <Room>
        <ID>1</ID>
        <Type>Single</Type>
        <Date>2024-12-20</Date>
        <Status>Disponible</Status>
    </Room>
</Availability>
```

### **API REST**
#### Endpoint: Crear Reserva
```bash
curl -X POST http://localhost:5000/reservations \
-H "Content-Type: application/json" \
-d '{
      "room_type": "Single",
      "start_date": "2024-12-20",
      "end_date": "2024-12-22",
      "customer_name": "John Doe"
   }'
```
Respuesta esperada:
```json
{
    "message": "Reservation created"
}
```

#### Endpoint: Consultar Reserva
```bash
curl -X GET http://localhost:5000/reservations/1
```
Respuesta esperada:
```json
{
    "reservation_id": 1,
    "room_number": 101,
    "customer_name": "John Doe",
    "start_date": "2024-12-20",
    "end_date": "2024-12-22",
    "status": "Activa"
}
```

#### Endpoint: Cancelar Reserva
```bash
curl -X DELETE http://localhost:5000/reservations/1
```
Respuesta esperada:
```json
{
    "message": "Reservation cancelled"
}
```

### **Microservicio de Inventario**
#### Endpoint: Registrar Habitación
```bash
curl -X POST http://localhost:5001/rooms \
-H "Content-Type: application/json" \
-d '{
      "room_number": 103,
      "room_type": "Suite",
      "status": "Disponible"
   }'
```
Respuesta esperada:
```json
{
    "message": "Room created"
}
```

#### Endpoint: Actualizar Estado de Habitación
```bash
curl -X PATCH http://localhost:5001/rooms/1 \
-H "Content-Type: application/json" \
-d '{"status": "Mantenimiento"}'
```
Respuesta esperada:
```json
{
    "message": "Room status updated"
}
```

---

## **Notas Adicionales**

1. **Docker Compose**:
   - Los contenedores de los servicios SOAP, REST e Inventario interactúan con la base de datos SQL Server mediante su propia configuración.

2. **Pruebas Automáticas**:
   - Puedes crear pruebas automatizadas usando herramientas como Postman o pytest.

3. **Escalabilidad**:
   - Cada servicio puede escalarse de manera independiente en función de las necesidades de la cadena hotelera.

---

## **Contacto**
- Autor: [Tu Nombre]
- Email: [Tu Email]
- GitHub: [Tu Perfil]

