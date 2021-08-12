# Prueba de Simón Samán (©2021)
from copy import deepcopy
path = 'example.txt'
bombillo = "💡"
piso = "⬜"
pared = "⬛"
datos = []
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
    if matriz[y][j] <= 1 :
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
    if matriz[i][x] <= 1 :
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
    if matriz[y][j] <= 1 :
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
    if matriz[i][x] <= 1:
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

#Búsqueda usando DFS
def buscarSolucion(i,j,conteoBombillos, datos):
  global minBombillos, mejorCaso
  # Podando soluciones inviables
  if (minBombillos != -1 and conteoBombillos >= minBombillos):
    return
  datos[i][j] = bombillo
  puntuaciones = determinarPuntuaciones(datos)
  listaPrioridad = generarPrioridad(puntuaciones)
  #Condicion de parada
  if len(listaPrioridad) == 0:
    # Nuevo minimo
    if (conteoBombillos < minBombillos or minBombillos == -1):
      minBombillos = conteoBombillos
      mejorCaso = deepcopy(puntuaciones)
    return
  else:
    # Paso en profundidad
    (valor, k, l) = listaPrioridad[0]
    buscarSolucion(k, l, conteoBombillos + 1, datos)
    return

def menu():
  print ("____________________________________")
  if datosCargados:
    print("(3) Mostar solución")
    print("(2) Mostrar habitación")
  else:
    print("(1) Cargar datos desde example.txt ")
  print("(0) Salir")
  print ("____________________________________")

menu()
opcionMenu = input("")

while opcionMenu != "0":
  if opcionMenu == "1":
    cargarDatos()
    datosCargados = True
  elif opcionMenu == "2":
    imprimirMatrizEmoji(datos)
  elif opcionMenu == "3":
    for y in range(len(datos)):
      for x in range(len(datos[y])):
        if datos[y][x]  == pared:
          continue
        nuevosDatos = deepcopy(datos)
        buscarSolucion(y,x,1, nuevosDatos)
    imprimirMatrizEmoji(mejorCaso)
    print("Numero mínimo de bombillos: ",minBombillos)
  else:
    print("Opción no reconocida")
  menu()
  opcionMenu = input("")
