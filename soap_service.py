from flask import Flask, request, Response
from lxml import etree
import pyodbc

app = Flask(__name__)

# Función de conexión para SQL Server
def conectar_sql_server():
    try:
        servidor = 'MSI'  # Reemplazar con tu servidor
        base_datos = 'SOAPServiceDB'  # Reemplazar con tu base de datos

        conexion_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"Trusted_Connection=Yes;"
            f"TrustServerCertificate=Yes;"
        )

        conexion = pyodbc.connect(conexion_str)
        print("Conexión exitosa a la base de datos.")
        return conexion
    except pyodbc.Error as e:
        print("Error al conectar con SQL Server:", e)
        return None

# Servicio SOAP
@app.route('/soap', methods=['POST'])
def soap_service():
    # Parsear el request SOAP
    try:
        xml_request = etree.fromstring(request.data)
        ns = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'}

        # Extraer parámetros del cuerpo SOAP
        body = xml_request.find('soapenv:Body', ns)
        check_availability = body.find('.//check_availability')

        start_date = check_availability.find('start_date').text
        end_date = check_availability.find('end_date').text
        room_type = check_availability.find('room_type').text

        # Consultar disponibilidad en la base de datos
        conn = conectar_sql_server()
        if conn is None:
            return generate_soap_response("<Error>Problema de conexión con la base de datos</Error>")

        cursor = conn.cursor()
        query = """
            SELECT room_id, room_type, available_date, status
            FROM availability
            WHERE room_type = ? AND available_date BETWEEN ? AND ? AND status = 'Disponible'
        """
        cursor.execute(query, room_type, start_date, end_date)
        rows = cursor.fetchall()
        conn.close()

        # Generar respuesta SOAP
        availability = "<Availability>"
        for row in rows:
            availability += f"<Room><ID>{row.room_id}</ID><Type>{row.room_type}</Type><Date>{row.available_date}</Date><Status>{row.status}</Status></Room>"
        availability += "</Availability>"

        return generate_soap_response(availability)
    except Exception as e:
        return generate_soap_response(f"<Error>{str(e)}</Error>")

# Generador de respuesta SOAP
def generate_soap_response(content):
    response = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>{content}</soapenv:Body>
    </soapenv:Envelope>
    """
    return Response(response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
