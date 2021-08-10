# Prueba de Simón Samán (©2021)

matrizPrueba = """00010111
01000000
01000111
01111000
01001000
01001010
01011010
00001000
01101101
00001000
10010011
00100000
"""
bombillo = "💡"
piso = "⬜"
pisoIluminado = "🎆"
pared = "⬛"
datos = []
puntuaciones = []
totalBombillos = 0
minBombillos = -1

def cargarDatos(matriz):
  salida = []
  fila = []
  for celda in matriz:
    if celda == '0':
      fila.append(piso)
    elif celda == '1':
      fila.append(pared)
    elif celda == '\n':
      salida.append(fila)
      fila = []
  global datos
  datos = salida

def imprimirMatriz(matriz, terminal):
  for fila in matriz:
    for celda in fila:
      print (celda,end=terminal)
    print ('')

def imprimirMatrizEmoji(matriz):
  for fila in matriz:
    for celda in fila:
      if celda == -1:
        print (pisoIluminado,end='')
      else:
        print (celda,end='')
    print ('')

def puntuacionCelda(i,j):
  puntuacion = 1

  #Recorrido Norte
  for y in reversed(range(0,i)):
    if datos[y][j] == pared :
      break
    puntuacion += 1

  #Recorrido Este
  for x in reversed(range(len(datos[i])-1, j, -1)):
    if datos[i][x] == pared :
      break
    puntuacion += 1
  #Recorrido Sur
  for y in reversed(range(len(datos)-1,i,-1)):
    if datos[y][j] == pared :
      break
    puntuacion += 1
  
  #Recorrido Oeste
  for x in reversed(range(0,j)):
    if datos[i][x] == pared:
      break
    puntuacion += 1
  
  return puntuacion


def determinarPuntuaciones():
  global puntuaciones
  for i in range (0,len(datos)):
    fila = []
    for j in range (0, len(datos[0])):
      if (datos[i][j] == pared ):
        fila.append(pared)
        continue
      fila.append(puntuacionCelda(i,j))
    puntuaciones.append(fila)

def recalcularPuntuaciones():
  global puntuaciones
  for i in range (0,len(puntuaciones)):
    fila = []
    for j in range (0, len(puntuaciones[0])):
      if puntuaciones[i][j] == bombillo or puntuaciones[i][j] == -1 or puntuaciones[i][j] == pared :
        continue
      puntuaciones[i][j] = puntuacionCelda(i,j)

def encontrarMayor():
  mayor = (-1, -1, -1)
  for i in range (0,len(puntuaciones)):
    for j in range (0, len(puntuaciones[0])):
      if (puntuaciones[i][j] == bombillo) or (puntuaciones[i][j] == pared) :
        continue
      if (puntuaciones[i][j] > 0 and puntuaciones[i][j] > mayor[2] ):
        mayor = (i,j,puntuaciones[i][j])
      
  return mayor    

def limpiarBombillos(i,j):
  global puntuaciones
  puntuaciones[i][j] = bombillo
  #Recorrido Norte
  for y in reversed(range(0,i)):
    if puntuaciones[y][j] == pared :
      break
    puntuaciones[y][j] = -1
    
  #Recorrido Este
  for x in reversed(range(len(datos[i])-1, j, -1)):
    if puntuaciones[i][x] == pared :
      break
    puntuaciones[i][x] = -1
    
  #Recorrido Sur
  for y in reversed(range(len(datos)-1,i,-1)):
    if puntuaciones[y][j] == pared :
      break
    puntuaciones[y][j] = -1
  
  #Recorrido Oeste
  for x in reversed(range(0,j)):
    if puntuaciones[i][x] == pared :
      break
    puntuaciones[i][x] = -1




cargarDatos(matrizPrueba)
imprimirMatriz(datos,'')
determinarPuntuaciones()
imprimirMatriz(puntuaciones,' ')
while True:
  (mayorI, mayorJ, mayor) = encontrarMayor()
  if mayor == -1:
    break
  limpiarBombillos(mayorI,mayorJ)
  totalBombillos+=1
  recalcularPuntuaciones()
  imprimirMatriz(puntuaciones,' ')

imprimirMatrizEmoji(puntuaciones)
print(totalBombillos)



