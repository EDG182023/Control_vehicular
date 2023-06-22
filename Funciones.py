import pyodbc
import cv2
import matplotlib.pyplot as plt
import io
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from datetime import datetime



# Establecer la conexión a la base de datos
connection = pyodbc.connect('Driver={SQL Server};Server=DESKTOP-8AO7HCU;Database=CONTROL_VEIHCULAR;uid=sa;pwd=kncb0405')

# Solicitar el DNI al usuario
#dni = input("Ingrese el DNI: ")

# Función para la validación de existencia de DNI
def dni_control(dni, Dialog):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT dni_fletero FROM fletero WHERE dni_fletero = ?", dni)
        results = cursor.fetchall()

        if not results:
            print("DNI " + dni + " inexistente en el sistema")
            cursor.close()
            import Ingreso_Dni_Pantalla #import Ui_Dialog
            return Ingreso_Dni_Pantalla.abrir_dialogo2(Dialog)#dni_carga(dni)
        else:
            cursor.close()
            print("El DNI " + dni + " se encuentra dado de alta")
            return 1 #patente_control(patente=input("Ingrese patente de vehículo: "))
        

    except Exception as e:
        print("Error en la consulta de validación de DNI:", e)

# Alta del fletero
def dni_carga(dni):
    try:
        cursor = connection.cursor()
        print("Procederemos a dar de alta este nuevo fletero, por favor cargue la información: ")
        nombre = input("Ingrese el nombre del fletero: ")
        apellido = input("Ingrese el apellido del fletero: ")

        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        if ret:
            # Convertir la imagen a escala de grises para la detección de rostros
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Cargar el clasificador de cascada Haar para la detección de rostros
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Detectar rostros en la imagen
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Dibujar un rectángulo alrededor de cada rostro detectado
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Cerrar la cámara
                camera.release()

                # Mostrar la imagen con los rostros detectados
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                plt.imshow(image)
                plt.axis('off')
                plt.show()

                # Almacenar la imagen con los rostros detectados en la base de datos
                image_data = cv2.imencode('.jpg', frame)[1].tobytes()

                cursor.execute("INSERT INTO fletero VALUES (?, ?, ?, ?)", dni, nombre, apellido, image_data)
                connection.commit()
                cursor.close()
                print("El fletero " + nombre + " de DNI: " + dni + " y Apellido: " + apellido + ", fue dado de alta correctamente!")
                return patente_control(patente=input("Ingrese patente de vehículo: "))
            else:
                 # Cerrar la cámara
                camera.release()
                # Mostrar la imagen con los rostros detectados
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                plt.imshow(image)
                plt.axis('off')
                plt.show()
                print("No se detectaron rostros en la imagen capturada, vuelve a registrar los datos")
                return dni_carga(dni)
        else:
            return "No se pudo capturar la foto del fletero"
    except Exception as e:
        print("Error en el alta del fletero:", e)
'''
# Función para la validación de existencia de PATENTE
def patente_control(patente):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT patente_veh FROM vehiculo WHERE patente_veh = ?", patente)
        results = cursor.fetchall()

        if not results:
            cursor.close()
            print("¡La patente " + patente + " no existe!")
            return patente_carga(patente)
        else:
            cursor.close()
            f"¡La patente " + patente + " se encuentra dada de alta!"
            return  ingreso_veh(dni,patente)
    except Exception as e:
        print("Error en la consulta de validación de patente:", e)

# Alta de patentes/vehículos
def patente_carga(patente):
    try:
        cursor = connection.cursor()
        print("Procederemos a dar de alta este nuevo vehículo, por favor cargue la información: ")
        patente_trac = input("Ingrese la patente del tractor: ")
        marca = input("Ingrese la marca del vehículo: ")
        seguro_vto = input("Ingrese la fecha de vencimiento del seguro: ")
        registro_vto = input("Ingrese la fecha de vencimiento del registro: ")
        art_vto = input("Ingrese la fecha de vencimiento de la ART: ")

        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        image_data = cv2.imencode('.jpg', frame)[1].tobytes()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        plt.axis('off')
        plt.show()

        cursor.execute("INSERT INTO vehiculo VALUES (?, ?, ?, ?, ?, ?)", patente, patente_trac, marca, seguro_vto, registro_vto, art_vto)
        connection.commit()
        cursor.close()
        f"¡El vehículo " + patente + " fue dado de alta correctamente!" 
        return  ingreso_veh(dni,patente)
    except Exception as e:
        print("Error en el alta del vehículo:", e)
        patente_carga(patente)

# Motivos
def motivos ():
    opciones = ["Opción 1", "Opción 2", "Opción 3", "Opción 4"]

    # Mostrar las opciones al usuario
    print("Selecciona una opción:")
    for i, opcion in enumerate(opciones):
        print(f"{i+1}. {opcion}")

    # Pedir al usuario que ingrese su elección
    eleccion = int(input("Ingresa el número de la opción elegida: "))

    # Verificar si la elección es válida
    if 1 <= eleccion <= len(opciones):
        opcion_elegida = opciones[eleccion - 1]
        print(f"Elegiste la opción: {opcion_elegida}")
    else:
        print("Opción inválida. Por favor, elige un número válido de opción.")

    return 0

# Ingreso de mercaderia
def ingreso_veh(dni,patente):
    try:
        cursor = connection.cursor()
        print("Procederemos a dar de alta un nuevo ingreso: ")
        motivo=motivos ()
        cliente=input("El nombre del cliente: ")        
        nro_puerta = input("Ingrese el numero de puerta: ")
        nro_contenedor = input("Ingrese el numero de contenedor: ")
        obs=input("Ingrese una observacion: ")
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()
        cursor.execute("INSERT INTO principal VALUES (?, ?,'', ?, ?, ?,?,?,?,'')",dni, patente, cliente, motivo, nro_contenedor, nro_puerta, obs, fecha_hora_actual)
        connection.commit()
        cursor.close()
        return "¡El vehículo " + patente + " fue ingresado correctamente!"
    except Exception as e:
        print("Error en el alta del vehículo:", e)
        ingreso_veh(dni,patente)

    return 0



try:
    print(dni_control(dni))
except Exception as e:
    print("Error general:", e)

# Cerrar la conexión a la base de datos
connection.close()'''