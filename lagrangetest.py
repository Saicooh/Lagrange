from PIL import Image
import numpy as np
from numpy import poly1d

def lagrange(x, w):
    M = len(x)
    p = poly1d(0.0)
    for j in range(M):
        pt = poly1d(w[j])
        for k in range(M):
            if k == j:
                continue
            fac = x[j] - x[k]
            pt *= poly1d([1.0, -x[k]]) / fac
        p += pt
    return p

def repararPixelesDanadosConLagrange(matrizImagen):
    altura, ancho, canales = matrizImagen.shape
    imagenReparada = np.copy(matrizImagen)
    
    for fila in range(1, altura - 1):
        for columna in range(1, ancho - 1):
            for canal in range(canales): 
                if matrizImagen[fila, columna, canal] == 0 or matrizImagen[fila, columna, canal] == 255:
                    pixelesCircundantes = matrizImagen[fila - 1:fila + 2, columna - 1:columna + 2, canal].flatten()
                    x = np.array([i for i in range(9) if pixelesCircundantes[i] not in [0, 255]])
                    y = np.array([pixelesCircundantes[i] for i in range(9) if pixelesCircundantes[i] not in [0, 255]])
                    if len(x) >= 2:  # Necesitamos al menos dos puntos para interpolar
                        poly = lagrange(x, y)
                        valorReparado = poly(4)
                        imagenReparada[fila, columna, canal] = np.clip(valorReparado, 0, 255)
    return imagenReparada

def procesarImagen(rutaImagen, rutaSalida):
    # Cargar la imagen
    imagen = Image.open(rutaImagen)
    matrizImagen = np.array(imagen)

    # Reparar la imagen
    matrizImagenReparada = repararPixelesDanadosConLagrange(matrizImagen)

    # Convertir el arreglo de numpy de vuelta a una imagen de PIL
    imagenReparada = Image.fromarray(matrizImagenReparada.astype('uint8'))

    # Guardar la imagen restaurada
    imagenReparada.save(rutaSalida)

# Uso de la función con el nombre del archivo de entrada y el nombre del archivo de salida deseado
procesarImagen('FABIANPRUEBA1.jpg', 'FABIANPRUEBA1_restaurada.jpg')
