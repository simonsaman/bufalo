# Prueba de Simón Samán (©2021)
from copy import deepcopy
import multiprocessing as mp

path = 'example.txt'
bombillo = "💡"
piso = "⬜"
pared = "⬛"
datos = []
barra = "____________________________________"
minBombillos = -1
mejorCaso = 0
datosCargados = False
opcionMenu = -1


def cargarDatos():
  global datos
  contenido = []
  with open(path, 'r') as archivo:
    contenido = archivo.readlines()
  salida = []
  for filaContenido in contenido:
    fila = []
    for caracter in filaContenido:
      if caracter == '0':
        fila.append(piso)
      elif caracter == '1':
        fila.append(pared)
      elif caracter == '\n':
        salida.append(fila)
  datos = salida


def imprimirMatrizEmoji(matriz):
  for fila in matriz:
    for celda in fila:
      if celda == 0:
        print (piso,end='')
      else:
        print (celda,end='')
    print ('')

def puntuacionCelda(matriz, i,j):
  #Cada bombillo alumbra su propia celda
  puntos = 1
  #Recorrido Norte
  for y in reversed(range(0,i)):
    if matriz[y][j] == pared :
      break
    if matriz[y][j] == piso:
      puntos += 1
      continue
    if matriz[y][j] == bombillo:
      return 0
    if matriz[y][j] == 0 :
      continue
    puntos+= 1

  #Recorrido Este
  for x in reversed(range(len(datos[i])-1, j, -1)):
    if matriz[i][x] == pared :
      break
    if matriz[i][x] == bombillo:
      return 0
    if matriz[i][x] == piso:
      puntos+= 1
      continue
    if matriz[i][x] == 0 :
      continue
    puntos+= 1
  
  #Recorrido Sur
  for y in reversed(range(len(datos)-1,i,-1)):
    if matriz[y][j] == pared:
      break
    if matriz[y][j] == bombillo:
      return 0
    if matriz[y][j] == piso:
      puntos += 1
      continue
    if matriz[y][j] == 0 :
      continue
    puntos += 1
  
  #Recorrido Oeste
  for x in reversed(range(0,j)):
    if matriz[i][x] == pared:
      break
    if matriz[i][x] == bombillo:
      return 0
    if matriz[i][x] == piso:
      puntos += 1
      continue
    if matriz[i][x] == 0:
      continue
    puntos += 1
  
  return puntos


def determinarPuntuaciones(matriz):
  puntuaciones = []
  for i in range (0,len(matriz)):
    fila = []
    for j in range (0, len(matriz[0])):
      if (matriz[i][j] == pared ) or (matriz[i][j] == bombillo):
        fila.append(matriz[i][j])
        continue
      fila.append(puntuacionCelda(matriz, i, j))
    puntuaciones.append(fila)
  return puntuaciones

def generarPrioridad(matriz):
  prioridad = []
  for i in range(len(matriz)):
    for j in range(len(matriz[0])):
      if matriz[i][j] == bombillo or matriz[i][j] == pared or matriz[i][j] <= 0 :
        continue
      prioridad.append((matriz[i][j],i,j))
  prioridad.sort(reverse=True,key=lambda x: x[0])
  return prioridad

def siguienteObjetivo(matriz):
  max = 0
  siguienteI = -1
  siguienteJ = -1
  for i in range(len(matriz)):
    for j in range(len(matriz[0])):
      if matriz[i][j] == bombillo or matriz[i][j] == pared or matriz[i][j] <= 0 :
        continue
      if matriz[i][j] > max:
        max = matriz[i][j]
        siguienteI = i
        siguienteJ = j
  return (max, siguienteI, siguienteJ)

#Búsqueda usando DFS
def buscarSolucion(i, j, conteoBombillos, datos, listaResultados, minBombillos):
  # Podando soluciones inviables
  if (minBombillos != -1 and conteoBombillos >= minBombillos):
    return -1
  datos[i][j] = bombillo
  puntuaciones = determinarPuntuaciones(datos)
  siguientePrioridad = siguienteObjetivo(puntuaciones)
  (valor, x, y) = siguientePrioridad
  #Condicion de parada
  if valor == 0:
    # Nuevo minimo
    if (conteoBombillos < minBombillos or minBombillos == -1): 
      listaResultados.append((conteoBombillos, deepcopy(puntuaciones)))
  else:
    # Paso en profundidad
    return buscarSolucion(x, y, conteoBombillos + 1, puntuaciones, listaResultados, minBombillos)

def lote(lista, paquete):
  largo = len(lista)
  for i in range(0, largo, paquete):
    yield lista[i:min(i + paquete, largo )]


def menu():
  print (barra)
  if datosCargados:
    print("(3) Mostrar solución")
    print("(2) Mostrar habitación")
  else:
    print("(1) Cargar datos desde example.txt ")
  print("(0) Salir")
  print (barra)

def main():
  global datosCargados, minBombillos, mejorCaso,opcionMenu
  procesadores =  mp.cpu_count()

  menu()
  opcionMenu = input("")

  while opcionMenu != "0":
    if opcionMenu == "1":
      cargarDatos()
      datosCargados = True
    elif opcionMenu == "2":
      imprimirMatrizEmoji(datos)
    elif opcionMenu == "3":
    # Ciclo de búsqueda
      puntuaciones = determinarPuntuaciones(datos)
      listaPrioridad = generarPrioridad(puntuaciones)
      # Encolar en baches para cada procesador
      for bache in lote(listaPrioridad, procesadores):
        manager = mp.Manager()
        listaResultados = manager.list()
        procesos = []
        for candidato in bache:
          (_ ,i,j) = candidato 
          if candidato == pared:
              continue
          nuevosDatos = deepcopy(datos)
          proceso = mp.Process(target = buscarSolucion, args=[i, j, 1, nuevosDatos, listaResultados, minBombillos])
          procesos.append(proceso)
          proceso.start()
          
        for proceso in procesos:
          proceso.join()

        for resultado in listaResultados:
            (valor, solucion) = resultado
            if minBombillos == -1 or  valor < minBombillos:
              minBombillos = valor
              mejorCaso = deepcopy(solucion)
      imprimirMatrizEmoji(mejorCaso)
      print("Numero mínimo de bombillos: ", minBombillos)
    else:
      print("Opción no reconocida")
    menu()
    opcionMenu = input("")
    print (barra)

if __name__ == "__main__":
  main()
