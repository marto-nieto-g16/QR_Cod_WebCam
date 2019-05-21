"""
    Programa en Python para leer codigos QR.
    Muestra sus dimensiones en la pantalla, 
    Mensaje y Rotacion en grados.
"""
 
import zbar
import numpy as np
import cv2

capture = cv2.VideoCapture(0) #Inicializar la camara
font = cv2.FONT_HERSHEY_SIMPLEX #Cargar la fuente 
 
while 1:
    val, frame = capture.read() #Capturar un frame
    if val:
        #Capturar un frame con la camara y guardar sus dimensiones
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dimensiones = frame_gris.shape #'dimensiones' sera un array que contendra el alto, el ancho y los canales de la imagen en este orden.
 
        imagen_zbar = zbar.Image(dimensiones[1], dimensiones[0], 'Y800', frame_gris.tobytes()) #Convertir la imagen de OpenCV a una imagen que la libreria ZBAR pueda entender
        escaner = zbar.ImageScanner()  #Construir un objeto de tipo scaner, que permitira escanear la imagen en busca de codigos QR
        escaner.scan(imagen_zbar) #Escanear la imagen y guardar todos los codigos QR que se encuentren
 
        for codigo_qr in imagen_zbar:
            loc = codigo_qr.location #Guardar las coordenadas de las esquinas
            dat = codigo_qr.data[:-2] #Guardar el mensaje del codigo QR. Los ultimos dos caracteres son saltos de linea que hay que eliminar
 
            #Dibuja el contorno del codigo QR
            localizacion = np.array(loc, np.int32)
 
            #Dibuja el contorno del codigo QR en azul sobre la imagen
            cv2.polylines(frame, [localizacion], True, (255,0,0), 2)
 
            #Dibuja las cuatro esquinas del codigo QR
            cv2.circle(frame, loc[0], 3, (0,0,255), -1) #Rojo - esquina superior izquierda
            cv2.circle(frame, loc[1], 3, (0,255,255), -1) #Amarillo - esquina inferior izquierda
            cv2.circle(frame, loc[2], 3, (255,100,255), -1) #Rosa -esquina inferior derecha
            cv2.circle(frame, loc[3], 3, (0,255,0), -1) #Verde - esquina superior derecha
 
            #Buscar el centro del rectangulo del codigo QR
            cx = (loc[0][0]+loc[2][0])/2
            cy = (loc[0][1]+loc[2][1])/2
 
            #Escribir el mensaje del codigo QR.
            cv2.putText(frame,dat,(cx,cy), font, 0.7,(0,255,0), 2)
 
            #Calcular el angulo de rotacion del codigo QR. Supondremos que el angulo es la pendiente de la recta que une el vertice loc[0] (rojo) con loc[3] (verde)
            vector_director = [loc[3][0]-loc[0][0], loc[3][1]-loc[0][1]]
            angulo = (np.arctan2(float(vector_director[1]),vector_director[0])*57.29)%360 #Calculo de la tangente y conversion de radianes a grados
            #Correccion debida al orden de las coordenadas en la pantalla
            angulo += -360
            angulo *= -1
 
            #Escribir el angulo sobre la imagen con dos decimales
            cv2.putText(frame,str("%.2f" % angulo),(cx,cy+30), font, 0.7,(255,255,255))
 
        #Mostrar la imagen
        cv2.imshow('QR-Code WebCam', frame)
    
    #Salir con 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

 
cv2.destroyAllWindows()