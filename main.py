import pygame
import random
import math
import io
from pygame import mixer

pygame.init() #initialize all imported pygame modules

#Crear la pantalla
pantalla = pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono) #cargamos icono
fondo = pygame.image.load('Fondo.jpg')


#agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


#Player
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0


#enemy
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8


# funcion
def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()

    return io.BytesIO(ttf_bytes)


for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)


#bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("Cute Quality.otf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y= 10


#texto final juego
fuente_final = pygame.font.Font(fuente_como_bytes, 70)



#funcion terminar
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (160, 200))


#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


#function player
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


#function enemy
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


#funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


#funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False






#Loop del juego
se_ejecuta = True
while se_ejecuta:
    #img fondo
    pantalla.blit(fondo, (0,0))

    #iterar eventos
    for evento in pygame.event.get():
        #evento cerrar
        if evento.type == pygame.QUIT: #uninitialize all pygame modules
            se_ejecuta = False
        #evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
        #evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #modificar ubicacion jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicacion enemigo
    for e in range(cantidad_enemigos):
        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]


        # mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.6
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.6
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    #movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)


    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    #actualizar
    pygame.display.update()
