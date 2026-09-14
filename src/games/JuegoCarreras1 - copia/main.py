import pygame
import math
import random
pygame.init()
# =========================================================
# CONFIGURACIÓN
# =========================================================
ANCHO = 1000
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Carrera — Bienvenida F1")
reloj = pygame.time.Clock()
# =========================================================
# 🎨 PALETA DE COLORES
# =========================================================
CIELO_SUPERIOR = (30, 60, 114)
CIELO_INFERIOR = (176, 216, 230)
CIELO_HORIZONTE = (255, 255, 255)
CESPED_CLARO = (76, 175, 80)
CESPED_OSCURO = (56, 142, 60)
ASFALTO = (52, 58, 64)
BORDE_SEGURIDAD_ROJO = (211, 47, 47)
BORDE_SEGURIDAD_BLANCO = (255, 255, 255)
LINEA_CARRIL = (245, 245, 245)
LINEA_META = (255, 215, 0)
DORADO = (255, 215, 0)
ROJO_F1 = (211, 47, 47)
FONDO_TALLER = (22, 28, 36)
GRIS_TARJETA = (44, 52, 64)
GRIS_BORDE = (86, 96, 110)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO_POTENCIA = (255, 230, 0)
NARANJA_FRENO = (255, 110, 64)
SOMBRA = (0, 0, 0, 80)
EFECTO_VELOCIDAD = (255, 230, 0, 100)
EFECTO_FRENO = (255, 110, 64, 100)
# =========================================================
# FUENTES
# =========================================================
fuente = pygame.font.Font(None, 38)
fuente_pequena = pygame.font.Font(None, 26)
fuente_mediana = pygame.font.Font(None, 48)
fuente_grande = pygame.font.Font(None, 72)
fuente_titulo = pygame.font.Font(None, 56)
fuente_bienvenida = pygame.font.Font(None, 82)
# =========================================================
# 🚗 IMÁGENES
# =========================================================
RUTA_IMAGENES = "C:/Users/romin/OneDrive/Documentos/JuegoCarreras1/imagenes/"
autos_pista = [
    pygame.image.load(RUTA_IMAGENES + "Corredor 1.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "Corredor 2.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "Corredor 3.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "Corredor 4.png").convert_alpha(),
]
autos_taller = [
    pygame.image.load(RUTA_IMAGENES + "pista 1.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "pista 2.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "pista 3.png").convert_alpha(),
    pygame.image.load(RUTA_IMAGENES + "pista 4.png").convert_alpha(),
]
# Si tenés una imagen de piloto F1, reemplaza esta línea:
# piloto_f1 = pygame.image.load(RUTA_IMAGENES + "piloto_f1.png").convert_alpha()
# Por ahora generamos una versión gráfica:
piloto_f1 = None
def escalar_imagen(imagen, escala):
    ancho = int(imagen.get_width() * escala)
    alto = int(imagen.get_height() * escala)
    return pygame.transform.smoothscale(imagen, (ancho, alto))
# =========================================================
# ESTADOS DEL JUEGO
# =========================================================
ESTADO_BIENVENIDA = "bienvenida"
ESTADO_TALLER = "taller"
ESTADO_CARRERA = "carrera"
ESTADO_FIN = "fin"
# =========================================================
# ⚙️ CONFIGURACIÓN DE EFECTOS
# =========================================================
DURACION_EFECTO = 180
BONUS_VELOCIDAD = 7.5
PENALIZACION_FRENO = 0.35
UMBRAL_CARRIL = 0.14
SEPARACION_MINIMA = 650
# =========================================================
# 📦 VARIABLES
# =========================================================
posicion_auto_anim = -150
velocidad_auto_anim = 8
imagen_auto_anim = escalar_imagen(autos_taller[0], 0.45)
direccion_auto_anim = 1
# Variables para la animación de bienvenida
tiempo_bienvenida = 0
texto_mostrado = 0
mostrar_presionar_tecla = False
transicion_a_taller = False
alfa_transicion = 0
# =========================================================
# 📊 VARIABLES DE LA CARRERA
# =========================================================
estado_juego = ESTADO_BIENVENIDA
seleccion_j1 = {"color": 0, "listo": False}
seleccion_j2 = {"color": 1, "listo": False}
ganador = None
contador_inicio = 0
DISTANCIA_META = 12000
distancia1 = 0.0
distancia2 = 0.0
distancia3 = 0.0
distancia4 = 0.0
auto1_pos = -0.40
auto2_pos = 0.40
auto3_pos = -0.15
auto4_pos = 0.15
velocidad1_base = 7.2
velocidad2_base = 7.2
velocidad3_base = 6.0
velocidad4_base = 6.0
velocidad1 = velocidad1_base
velocidad2 = velocidad2_base
velocidad3 = velocidad3_base
velocidad4 = velocidad4_base
efecto1 = 0
efecto2 = 0
efecto3 = 0
efecto4 = 0
bonus_acumulado1 = 0.0
bonus_acumulado2 = 0.0
bonus_acumulado3 = 0.0
bonus_acumulado4 = 0.0
# Valores de la posición del frame anterior. Se usan para detectar
# el cruce REAL de un rayo, un freno o la línea de meta.
distancia_anterior1 = 0.0
distancia_anterior2 = 0.0
distancia_anterior3 = 0.0
distancia_anterior4 = 0.0
auto1_pos_anterior = -0.40
auto2_pos_anterior = 0.40
auto3_pos_anterior = -0.15
auto4_pos_anterior = 0.15
objetos = []
banderas = []
# =========================================================
# 🔄 REINICIAR CARRERA
# =========================================================
def reiniciar_carrera_volver_taller():
    global estado_juego, seleccion_j1, seleccion_j2
    global ganador, contador_inicio, DISTANCIA_META
    global distancia1, distancia2, distancia3, distancia4
    global auto1_pos, auto2_pos, auto3_pos, auto4_pos
    global velocidad1_base, velocidad2_base, velocidad3_base, velocidad4_base
    global velocidad1, velocidad2, velocidad3, velocidad4
    global efecto1, efecto2, efecto3, efecto4
    global bonus_acumulado1, bonus_acumulado2, bonus_acumulado3, bonus_acumulado4
    global distancia_anterior1, distancia_anterior2, distancia_anterior3, distancia_anterior4
    global auto1_pos_anterior, auto2_pos_anterior, auto3_pos_anterior, auto4_pos_anterior
    global objetos, banderas
    estado_juego = ESTADO_TALLER
    seleccion_j1["listo"] = False
    seleccion_j2["listo"] = False
    ganador = None
    contador_inicio = 0
    DISTANCIA_META = 12000
    distancia1 = 0.0
    distancia2 = 0.0
    distancia3 = 0.0
    distancia4 = 0.0
    auto1_pos = -0.40
    auto2_pos = 0.40
    auto3_pos = -0.15
    auto4_pos = 0.15
    velocidad1_base = 7.2
    velocidad2_base = 7.2
    velocidad3_base = 6.0
    velocidad4_base = 6.0
    velocidad1 = velocidad1_base
    velocidad2 = velocidad2_base
    velocidad3 = velocidad3_base
    velocidad4 = velocidad4_base
    efecto1 = 0
    efecto2 = 0
    efecto3 = 0
    efecto4 = 0
    bonus_acumulado1 = 0.0
    bonus_acumulado2 = 0.0
    bonus_acumulado3 = 0.0
    bonus_acumulado4 = 0.0
    distancia_anterior1 = distancia1
    distancia_anterior2 = distancia2
    distancia_anterior3 = distancia3
    distancia_anterior4 = distancia4
    auto1_pos_anterior = auto1_pos
    auto2_pos_anterior = auto2_pos
    auto3_pos_anterior = auto3_pos
    auto4_pos_anterior = auto4_pos
    objetos = []
    distancia_objeto = 900
    tipos = ["rayo", "freno"] * 6
    random.shuffle(tipos)
    for tipo in tipos:
        distancia_objeto += SEPARACION_MINIMA + random.randint(80, 220)
        if distancia_objeto >= DISTANCIA_META - 700:
            break
        objetos.append({
            "distancia": distancia_objeto,
            "posicion": random.uniform(-0.42, 0.42),
            "tipo": tipo,
            "usado_por": 0
        })
    banderas = []
    for _ in range(60):
        lado = random.choice([-1, 1])
        distancia = random.randint(100, int(DISTANCIA_META - 100))
        posicion = random.uniform(0.35, 1.4)
        banderas.append({"lado": lado, "distancia": distancia, "posicion": posicion})
def iniciar_juego_nuevo():
    global estado_juego, seleccion_j1, seleccion_j2
    global tiempo_bienvenida, texto_mostrado, mostrar_presionar_tecla, transicion_a_taller, alfa_transicion
    seleccion_j1 = {"color": 0, "listo": False}
    seleccion_j2 = {"color": 1, "listo": False}
    tiempo_bienvenida = 0
    texto_mostrado = 0
    mostrar_presionar_tecla = False
    transicion_a_taller = False
    alfa_transicion = 0
    reiniciar_carrera_volver_taller()
    estado_juego = ESTADO_BIENVENIDA
def obtener_autos_ia():
    elegidos = {seleccion_j1["color"], seleccion_j2["color"]}
    libres = [i for i in range(4) if i not in elegidos]
    return libres[0], libres[1]
# =========================================================
# FUNCIONES DE PISTA
# =========================================================
def perspectiva(distancia_relativa):
    distancia_relativa = max(0.0, min(1.0, distancia_relativa))
    horizonte = 165
    return horizonte + (distancia_relativa ** 1.6) * (ALTO - horizonte)
def ancho_carretera(distancia_relativa):
    return 90 + (distancia_relativa ** 1.6) * (840 - 90)
def centro_carretera(y):
    max_d = max(distancia1, distancia2, distancia3, distancia4)
    progreso = max_d / 1.5
    curva1 = math.sin(progreso * 0.0008) * 70
    curva2 = math.sin(progreso * 0.0025 + 1.5) * 35
    curva3 = math.sin(progreso * 0.0005 + y * 0.006) * 25
    return ANCHO // 2 + curva1 + curva2 + curva3
def dibujar_bandera(x, y, escala):
    if escala <= 0: return
    grosor_poste = max(3, int(8 * escala))
    alto_poste = max(28, int(75 * escala))
    ancho_bandera = max(14, int(40 * escala))
    alto_bandera = max(10, int(24 * escala))
    pygame.draw.rect(pantalla, (200, 200, 200), (int(x - grosor_poste/2), int(y - alto_poste), grosor_poste, alto_poste))
    cx = int(x + grosor_poste/2)
    cy = int(y - alto_poste)
    for fila in range(2):
        for col in range(2):
            color = BLANCO if (fila + col) % 2 == 0 else ROJO_F1
            pygame.draw.rect(pantalla, color, (cx + col * ancho_bandera // 2, cy + fila * alto_bandera // 2, ancho_bandera // 2 + 1, alto_bandera // 2 + 1))
# =========================================================
# 🚗 DIBUJAR AUTO
# =========================================================
def dibujar_auto(x, y, escala, indice_auto, tipo_efecto=None):
    img_original = autos_pista[indice_auto]
    escala_base = 0.32
    img = escalar_imagen(img_original, escala_base * escala)
    rect = img.get_rect(center=(int(x), int(y)))
    if tipo_efecto == "velocidad":
        superficie_estela = pygame.Surface((int(img.get_width()*1.6), int(img.get_height()*1.4)), pygame.SRCALPHA)
        pygame.draw.ellipse(superficie_estela, EFECTO_VELOCIDAD, (0, int(img.get_height()*0.15), int(img.get_width()*1.6), int(img.get_height()*1.0)))
        pantalla.blit(superficie_estela, (rect.centerx - img.get_width()*0.80, rect.centery - img.get_height()*0.60))
    elif tipo_efecto == "freno":
        superficie_estela = pygame.Surface((int(img.get_width()*1.4), int(img.get_height()*1.3)), pygame.SRCALPHA)
        pygame.draw.ellipse(superficie_estela, EFECTO_FRENO, (0, int(img.get_height()*0.10), int(img.get_width()*1.4), int(img.get_height()*0.95)))
        pantalla.blit(superficie_estela, (rect.centerx - img.get_width()*0.70, rect.centery - img.get_height()*0.55))
    sombra = pygame.Surface((int(img.get_width()*1.15), int(img.get_height()*0.22)), pygame.SRCALPHA)
    sombra.fill(SOMBRA)
    pantalla.blit(sombra, (rect.centerx - img.get_width()*0.575, rect.bottom - img.get_height()*0.13))
    pantalla.blit(img, rect)
# =========================================================
# ⚡ SISTEMA DE EFECTOS
# =========================================================
def aplicar_efecto(num_auto, tipo):
    global velocidad1, velocidad2, velocidad3, velocidad4
    global efecto1, efecto2, efecto3, efecto4
    global bonus_acumulado1, bonus_acumulado2, bonus_acumulado3, bonus_acumulado4
    if tipo == "rayo":
        if num_auto == 1:
            bonus_acumulado1 += BONUS_VELOCIDAD
            velocidad1 = velocidad1_base + bonus_acumulado1
            efecto1 = DURACION_EFECTO
        elif num_auto == 2:
            bonus_acumulado2 += BONUS_VELOCIDAD
            velocidad2 = velocidad2_base + bonus_acumulado2
            efecto2 = DURACION_EFECTO
        elif num_auto == 3:
            bonus_acumulado3 += BONUS_VELOCIDAD
            velocidad3 = velocidad3_base + bonus_acumulado3
            efecto3 = DURACION_EFECTO
        elif num_auto == 4:
            bonus_acumulado4 += BONUS_VELOCIDAD
            velocidad4 = velocidad4_base + bonus_acumulado4
            efecto4 = DURACION_EFECTO
    elif tipo == "freno":
        if num_auto == 1:
            bonus_acumulado1 = 0.0
            velocidad1 = velocidad1_base * PENALIZACION_FRENO
            efecto1 = -DURACION_EFECTO
        elif num_auto == 2:
            bonus_acumulado2 = 0.0
            velocidad2 = velocidad2_base * PENALIZACION_FRENO
            efecto2 = -DURACION_EFECTO
        elif num_auto == 3:
            bonus_acumulado3 = 0.0
            velocidad3 = velocidad3_base * PENALIZACION_FRENO
            efecto3 = -DURACION_EFECTO
        elif num_auto == 4:
            bonus_acumulado4 = 0.0
            velocidad4 = velocidad4_base * PENALIZACION_FRENO
            efecto4 = -DURACION_EFECTO
def comprobar_objetos():
    autos = [
        (1, distancia_anterior1, distancia1, auto1_pos_anterior, auto1_pos),
        (2, distancia_anterior2, distancia2, auto2_pos_anterior, auto2_pos),
        (3, distancia_anterior3, distancia3, auto3_pos_anterior, auto3_pos),
        (4, distancia_anterior4, distancia4, auto4_pos_anterior, auto4_pos),
    ]
    for obj in objetos:
        if obj["usado_por"] != 0:
            continue
        dist_obj = obj["distancia"]
        pos_obj = obj["posicion"]
        candidatos = []
        for num_auto, dist_anterior, dist_actual, pos_anterior, pos_actual in autos:
            if dist_anterior < dist_obj <= dist_actual:
                avance = dist_actual - dist_anterior
                if avance <= 0:
                    continue
                factor = (dist_obj - dist_anterior) / avance
                pos_en_cruce = pos_anterior + (pos_actual - pos_anterior) * factor
                if abs(pos_en_cruce - pos_obj) <= UMBRAL_CARRIL:
                    candidatos.append((factor, num_auto))
        if candidatos:
            candidatos.sort(key=lambda x: x[0])
            _, auto_que_lo_tomo = candidatos[0]
            aplicar_efecto(auto_que_lo_tomo, obj["tipo"])
            obj["usado_por"] = auto_que_lo_tomo
def actualizar_efectos():
    global velocidad1, velocidad2, velocidad3, velocidad4
    global efecto1, efecto2, efecto3, efecto4
    datos = [
        (1, velocidad1_base, "velocidad1", "efecto1", "bonus_acumulado1"),
        (2, velocidad2_base, "velocidad2", "efecto2", "bonus_acumulado2"),
        (3, velocidad3_base, "velocidad3", "efecto3", "bonus_acumulado3"),
        (4, velocidad4_base, "velocidad4", "efecto4", "bonus_acumulado4"),
    ]
    for _, base, velocidad_nombre, efecto_nombre, bonus_nombre in datos:
        ef = globals()[efecto_nombre]
        bonus = globals()[bonus_nombre]
        if ef > 0:
            ef -= 1
            if ef > 0:
                globals()[velocidad_nombre] = base + bonus
            else:
                globals()[efecto_nombre] = 0
                globals()[bonus_nombre] = 0.0
                globals()[velocidad_nombre] = base
        elif ef < 0:
            ef += 1
            if ef < 0:
                globals()[velocidad_nombre] = base * PENALIZACION_FRENO
            else:
                globals()[efecto_nombre] = 0
                globals()[velocidad_nombre] = base
        globals()[efecto_nombre] = ef
# =========================================================
# 🏁 LÓGICA DE VICTORIA
# =========================================================
def comprobar_ganador():
    global ganador
    autos = [
        (1, distancia_anterior1, distancia1, "JUGADOR 1"),
        (2, distancia_anterior2, distancia2, "JUGADOR 2"),
        (3, distancia_anterior3, distancia3, "IA 1"),
        (4, distancia_anterior4, distancia4, "IA 2"),
    ]
    candidatos = []
    for _, dist_anterior, dist_actual, nombre in autos:
        if dist_anterior < DISTANCIA_META <= dist_actual:
            avance = dist_actual - dist_anterior
            if avance > 0:
                fraccion_cruce = (DISTANCIA_META - dist_anterior) / avance
                candidatos.append((fraccion_cruce, nombre))
                # Puedes descomentar la siguiente línea para depuración:
                # print(f"{nombre} cruzó la meta en fracción {fraccion_cruce}")
    if candidatos:
        candidatos.sort(key=lambda x: x[0])
        ganador = candidatos[0][1]
        # print(f"Ganador detectado: {ganador}")  # Depuración
# =========================================================
# ⚡ DIBUJADO DE OBJETOS Y PISTA
# =========================================================
def dibujar_rayo(x, y, escala):
    t = max(12, int(38 * escala))
    pts = [
        (x - t*0.10, y - t),
        (x + t*0.35, y - t*0.30),
        (x + t*0.08, y - t*0.30),
        (x + t*0.25, y),
        (x - t*0.40, y - t*0.55),
        (x - t*0.10, y - t*0.55)
    ]
    pygame.draw.polygon(pantalla, AMARILLO_POTENCIA, pts)
    pygame.draw.polygon(pantalla, (255, 255, 180), pts, max(3, int(4*escala)))
def dibujar_freno(x, y, escala):
    t = max(14, int(45 * escala))
    pts = [
        (x - t*0.30, y - t),
        (x + t*0.30, y - t),
        (x + t*0.30, y - t*0.50),
        (x + t*0.55, y - t*0.50),
        (x, y),
        (x - t*0.55, y - t*0.50),
        (x - t*0.30, y - t*0.50)
    ]
    pygame.draw.polygon(pantalla, NARANJA_FRENO, pts)
    pygame.draw.polygon(pantalla, (255, 200, 150), pts, max(3, int(4*escala)))
def dibujar_objetos():
    max_d = max(distancia1, distancia2, distancia3, distancia4)
    for obj in objetos:
        if obj["usado_por"] != 0:
            continue
        dr = obj["distancia"] - max_d
        if dr < -500: dr += DISTANCIA_META
        if dr <= -500 or dr > 2500: continue
        prof = 1.0 - max(0.0, dr) / 2500.0
        y = perspectiva(prof)
        ancho = ancho_carretera(prof)
        centro = centro_carretera(y)
        x = centro + obj["posicion"] * ancho * 0.38
        escala = 0.22 + prof * 1.15
        dibujar_rayo(x, y, escala) if obj["tipo"] == "rayo" else dibujar_freno(x, y, escala)
def dibujar_paisaje():
    max_d = max(distancia1, distancia2, distancia3, distancia4)
    for b in banderas:
        dr = b["distancia"] - max_d
        if dr < -500: dr += DISTANCIA_META
        if dr <= 0 or dr > 2500: continue
        prof = 1.0 - dr / 2500.0
        y = perspectiva(prof)
        ancho = ancho_carretera(prof)
        centro = centro_carretera(y)
        x = centro + b["lado"] * (ancho/2 + 50 + 110 * b["posicion"])
        dibujar_bandera(x, y, 0.22 + prof * 1.20)
def dibujar_carretera():
    for y in range(int(ALTO*0.70)):
        pr = y / (ALTO*0.70)
        r = int(CIELO_SUPERIOR[0] + (CIELO_INFERIOR[0] - CIELO_SUPERIOR[0]) * pr)
        g = int(CIELO_SUPERIOR[1] + (CIELO_INFERIOR[1] - CIELO_SUPERIOR[1]) * pr)
        b = int(CIELO_SUPERIOR[2] + (CIELO_INFERIOR[2] - CIELO_SUPERIOR[2]) * pr)
        pygame.draw.line(pantalla, (r, g, b), (0, y), (ANCHO, y))
    pygame.draw.rect(pantalla, CIELO_HORIZONTE, (0, 155, ANCHO, 25))
    for y in range(165, ALTO, 12):
        color = CESPED_CLARO if (y // 12) % 2 == 0 else CESPED_OSCURO
        pygame.draw.rect(pantalla, color, (0, y, ANCHO, 12))
    segmentos = 65
    for i in range(segmentos):
        cerca = i / segmentos
        lejos = (i + 1) / segmentos
        y1 = perspectiva(cerca)
        y2 = perspectiva(lejos)
        ancho1 = ancho_carretera(cerca)
        ancho2 = ancho_carretera(lejos)
        c1 = centro_carretera(y1)
        c2 = centro_carretera(y2)
        izq1, der1 = c1 - ancho1/2, c1 + ancho1/2
        izq2, der2 = c2 - ancho2/2, c2 + ancho2/2
        pygame.draw.polygon(pantalla, ASFALTO, [(int(izq1), int(y1)), (int(der1), int(y1)), (int(der2), int(y2)), (int(izq2), int(y2))])
        for signo in [1, -1]:
            borde_ext1 = c1 + signo * ancho1/2
            borde_int1 = c1 + signo * (ancho1/2 - ancho1*0.040)
            borde_ext2 = c2 + signo * ancho2/2
            borde_int2 = c2 + signo * (ancho2/2 - ancho2*0.040)
            pygame.draw.polygon(pantalla, BORDE_SEGURIDAD_ROJO, [(int(borde_ext1), int(y1)), (int(borde_int1), int(y1)), (int(borde_int2), int(y2)), (int(borde_ext2), int(y2))])
            linea_int1 = c1 + signo * (ancho1/2 - ancho1*0.052)
            linea_int2 = c2 + signo * (ancho2/2 - ancho2*0.052)
            pygame.draw.polygon(pantalla, BORDE_SEGURIDAD_BLANCO, [(int(linea_int1 - 4), int(y1)), (int(linea_int1 + 4), int(y1)), (int(linea_int2 + 3), int(y2)), (int(linea_int2 - 3), int(y2))])
        if i % 3 == 0:
            for carril in [-1/3, 0, 1/3]:
                x1 = c1 + ancho1 * carril * 0.65
                x2 = c2 + ancho2 * carril * 0.65
                grosor = max(2, int(7 * cerca))
                color = LINEA_META if carril == 0 else LINEA_CARRIL
                pygame.draw.polygon(pantalla, color, [(int(x1 - grosor), int(y1)), (int(x1 + grosor), int(y1)), (int(x2 + grosor/2), int(y2)), (int(x2 - grosor/2), int(y2))])
def dibujar_meta(progreso):
    dm = DISTANCIA_META - progreso
    if dm <= 0: return
    rel = 1.0 - min(dm / 2500.0, 1.0)
    if rel < 0.10: return
    y = perspectiva(rel)
    ancho = ancho_carretera(rel)
    c = centro_carretera(y)
    alto = max(30, int(120 * rel))
    pw = max(8, int(18 * rel))
    for signo in [-1, 1]:
        pygame.draw.rect(pantalla, BORDE_SEGURIDAD_ROJO, (int(c + signo*ancho*0.45 - pw/2), int(y - alto), pw, alto))
    cuadros = 12
    ac = ancho / cuadros
    ab = max(14, int(alto * 0.40))
    for fila in range(2):
        for col in range(cuadros):
            pygame.draw.rect(pantalla, BLANCO if (fila + col) % 2 == 0 else NEGRO, (int(c - ancho/2 + col*ac), int(y - alto + fila*ab), int(ac + 1), int(ab + 1)))
    txt = fuente_mediana.render("🏁 LÍNEA DE META", True, BLANCO)
    fondo = pygame.Surface((txt.get_width() + 30, txt.get_height() + 15), pygame.SRCALPHA)
    fondo.fill((0, 0, 0, 180))
    pantalla.blit(fondo, (int(c - txt.get_width()/2 - 15), int(y - alto - 60)))
    pantalla.blit(txt, (int(c - txt.get_width()/2), int(y - alto - 55)))
def calcular_posicion_visual(dist_auto, pos_carril):
    max_d = max(distancia1, distancia2, distancia3, distancia4)
    rel_dist = (dist_auto - (max_d - 2500.0)) / 2500.0
    rel_dist = max(0.0, min(1.0, rel_dist))
    y = perspectiva(rel_dist)
    ancho = ancho_carretera(rel_dist)
    c = centro_carretera(y)
    x = c + pos_carril * ancho * 0.35
    escala = 0.35 + rel_dist * 0.45
    return x, y, escala
# =========================================================
# 🏎️ PILOTO F1 ANIMADO
# =========================================================
def dibujar_piloto_f1(x, y, parpadeo_boca):
    escala = 0.9
    casco_ancho = int(50 * escala)
    casco_alto = int(60 * escala)
    pygame.draw.ellipse(pantalla, ROJO_F1, (x - casco_ancho//2, y - casco_alto//2, casco_ancho, casco_alto))
    pygame.draw.ellipse(pantalla, DORADO, (x - casco_ancho//2, y - casco_alto//2, casco_ancho, casco_alto), 3)
    visera_ancho = int(36 * escala)
    visera_alto = int(22 * escala)
    pygame.draw.ellipse(pantalla, (20, 20, 60), (x - visera_ancho//2, y - visera_alto//2, visera_ancho, visera_alto))
    pygame.draw.ellipse(pantalla, (60, 80, 120), (x - visera_ancho//2, y - visera_alto//2, visera_ancho, visera_alto), 2)
    pygame.draw.line(pantalla, DORADO, (x, y - casco_alto//2), (x, y + casco_alto//2), 2)
    pygame.draw.circle(pantalla, BLANCO, (x, y - 10), int(6 * escala))
    pygame.draw.rect(pantalla, ROJO_F1, (x - int(22 * escala), y + casco_alto//2 - 5, int(44 * escala), int(35 * escala)))
    pygame.draw.rect(pantalla, DORADO, (x - int(22 * escala), y + casco_alto//2 - 5, int(44 * escala), int(35 * escala)), 2)
    pygame.draw.line(pantalla, ROJO_F1, (x + int(18 * escala), y + casco_alto//2), (x + int(45 * escala), y - int(10 * escala)), int(10 * escala))
    pygame.draw.circle(pantalla, ROJO_F1, (x + int(48 * escala), y - int(12 * escala)), int(8 * escala))
    if parpadeo_boca:
        pygame.draw.circle(pantalla, NEGRO, (x, y + 2), int(5 * escala))
    else:
        pygame.draw.line(pantalla, NEGRO, (x - int(4 * escala), y + 5), (x + int(4 * escala), y + 5), int(2 * escala))
# =========================================================
# 🎨 CARTEL DE BIENVENIDA MEJORADO
# =========================================================
def dibujar_bienvenida():
    global estado_juego
    global tiempo_bienvenida, texto_mostrado, mostrar_presionar_tecla, transicion_a_taller, alfa_transicion
    tiempo_bienvenida += 1
    for y in range(ALTO):
        pr = y / ALTO
        r = int(CIELO_SUPERIOR[0] + (CIELO_INFERIOR[0] - CIELO_SUPERIOR[0]) * pr)
        g = int(CIELO_SUPERIOR[1] + (CIELO_INFERIOR[1] - CIELO_SUPERIOR[1]) * pr)
        b = int(CIELO_SUPERIOR[2] + (CIELO_INFERIOR[2] - CIELO_SUPERIOR[2]) * pr)
        pygame.draw.line(pantalla, (r, g, b), (0, y), (ANCHO, y))
    for i in range(20):
        y_pista = ALTO - 80 + i * 4
        ancho_pista = 100 + i * 45
        c = ANCHO // 2
        pygame.draw.line(pantalla, ASFALTO, (c - ancho_pista//2, y_pista), (c + ancho_pista//2, y_pista), 6)
        if i % 4 == 0:
            pygame.draw.line(pantalla, LINEA_CARRIL, (c - ancho_pista//2, y_pista), (c + ancho_pista//2, y_pista), 3)
    bandera_x = ANCHO // 2
    bandera_y = 130 + int(10 * math.sin(tiempo_bienvenida * 0.05))
    pygame.draw.rect(pantalla, (200, 200, 200), (bandera_x - 4, bandera_y - 60, 8, 60))
    for fila in range(3):
        for col in range(4):
            color = BLANCO if (fila + col) % 2 == 0 else ROJO_F1
            pygame.draw.rect(pantalla, color, (bandera_x + 4 + col * 16, bandera_y - 60 + fila * 20, 16, 20))
    parpadeo_boca = (tiempo_bienvenida % 40) < 20
    dibujar_piloto_f1(180, ALTO // 2 - 30, parpadeo_boca)
    globo_alfa = min(255, tiempo_bienvenida * 3)
    globo = pygame.Surface((360, 140), pygame.SRCALPHA)
    globo.fill((255, 255, 255, globo_alfa))
    pygame.draw.polygon(globo, (255, 255, 255, globo_alfa), ((30, 110), (0, 140), (50, 130)))
    pygame.draw.rect(globo, DORADO, (0, 0, 360, 140), 4, border_radius=20)
    pygame.draw.polygon(globo, DORADO, ((30, 110), (0, 140), (50, 130)), 3)
    pantalla.blit(globo, (260, ALTO // 2 - 70))
    texto1 = fuente_titulo.render("¡Bienvenidos, jugadores!", True, ROJO_F1)
    texto2 = fuente_mediana.render("El primero en cruzar la meta gana", True, NEGRO)
    pantalla.blit(texto1, texto1.get_rect(center=(ANCHO//2 + 50, ALTO//2 - 20)))
    pantalla.blit(texto2, texto2.get_rect(center=(ANCHO//2 + 50, ALTO//2 + 20)))
    if tiempo_bienvenida > 180:
        mostrar_presionar_tecla = True
    if mostrar_presionar_tecla:
        alfa_tecla = int(120 + 135 * abs(math.sin(tiempo_bienvenida / 30)))
        txt_tecla = fuente.render("► Presiona cualquier tecla para ir al taller ◄", True, BLANCO)
        fondo_tecla = pygame.Surface((txt_tecla.get_width() + 40, txt_tecla.get_height() + 20), pygame.SRCALPHA)
        fondo_tecla.fill((0, 0, 0, 180))
        fondo_tecla.set_alpha(alfa_tecla)
        pygame.draw.rect(fondo_tecla, DORADO, (0, 0, fondo_tecla.get_width(), fondo_tecla.get_height()), 2, border_radius=10)
        pantalla.blit(fondo_tecla, fondo_tecla.get_rect(center=(ANCHO//2, ALTO - 100)))
        pantalla.blit(txt_tecla, txt_tecla.get_rect(center=(ANCHO//2, ALTO - 100)))
    if transicion_a_taller:
        alfa_transicion += 5
        capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        capa.fill((0, 0, 0, min(255, alfa_transicion)))
        pantalla.blit(capa, (0, 0))
        if alfa_transicion >= 255:
            reiniciar_carrera_volver_taller()
            seleccion_j1["listo"] = False
            seleccion_j2["listo"] = False
            estado_juego = ESTADO_TALLER
# =========================================================
# TALLER
# =========================================================
def dibujar_taller_fondo():
    for y in range(ALTO):
        pr = y / ALTO
        r = int(FONDO_TALLER[0] + (GRIS_TARJETA[0] - FONDO_TALLER[0]) * pr)
        g = int(FONDO_TALLER[1] + (GRIS_TARJETA[1] - FONDO_TALLER[1]) * pr)
        b = int(FONDO_TALLER[2] + (GRIS_TARJETA[2] - FONDO_TALLER[2]) * pr)
        pygame.draw.line(pantalla, (r, g, b), (0, y), (ANCHO, y))
    pygame.draw.rect(pantalla, DORADO, (0, 0, ANCHO, 8))
    pygame.draw.rect(pantalla, ROJO_F1, (0, 8, ANCHO, 4))
    pygame.draw.rect(pantalla, ROJO_F1, (0, ALTO - 12, ANCHO, 8))
    pygame.draw.rect(pantalla, DORADO, (0, ALTO - 4, ANCHO, 4))
    pygame.draw.rect(pantalla, GRIS_BORDE, (60, 70, 6, ALTO - 100))
    pygame.draw.rect(pantalla, GRIS_BORDE, (ANCHO - 66, 70, 6, ALTO - 100))
def dibujar_panel_seleccion(x, y, seleccion, titulo, tecla_izq, tecla_der, tecla_listo, otro_color):
    indice = seleccion["color"]
    if indice == otro_color and not seleccion["listo"]:
        while indice == otro_color:
            indice = (indice + 1) % 4
        seleccion["color"] = indice
    ancho_panel = 330
    alto_panel = 410
    rect_panel = pygame.Rect(x - ancho_panel//2, y - 20, ancho_panel, alto_panel)
    pygame.draw.rect(pantalla, GRIS_TARJETA, rect_panel, border_radius=18)
    pygame.draw.rect(pantalla, DORADO if seleccion["listo"] else GRIS_BORDE, rect_panel, 5, border_radius=18)
    fondo_titulo = pygame.Rect(x - ancho_panel//2, y - 20, ancho_panel, 52)
    pygame.draw.rect(pantalla, ROJO_F1 if not seleccion["listo"] else (27, 157, 58), fondo_titulo, border_radius=18)
    pygame.draw.rect(pantalla, DORADO, fondo_titulo, 2, border_radius=18)
    txt_titulo = fuente_titulo.render(titulo, True, BLANCO)
    pantalla.blit(txt_titulo, txt_titulo.get_rect(center=(x, y + 6)))
    img_muestra = escalar_imagen(autos_taller[indice], 0.75)
    rect_img = img_muestra.get_rect(center=(x, y + 135))
    pantalla.blit(img_muestra, rect_img)
    if indice == otro_color:
        pygame.draw.rect(pantalla, (120, 20, 20, 180), (x - 140, y + 255, 280, 36), border_radius=10)
        txt_estado = fuente_pequena.render("❌ Auto elegido por el otro jugador", True, BLANCO)
    elif seleccion["listo"]:
        pygame.draw.rect(pantalla, (27, 157, 58, 180), (x - 140, y + 255, 280, 36), border_radius=10)
        txt_estado = fuente_pequena.render("✅ ¡CONFIRMADO! Listo para correr", True, BLANCO)
    else:
        pygame.draw.rect(pantalla, (33, 150, 243, 160), (x - 140, y + 255, 280, 36), border_radius=10)
        txt_estado = fuente_pequena.render("✓ Disponible — Elige tu diseño", True, BLANCO)
    pantalla.blit(txt_estado, txt_estado.get_rect(center=(x, y + 273)))
def dibujar_auto_animacion():
    global posicion_auto_anim, direccion_auto_anim
    posicion_auto_anim += velocidad_auto_anim * direccion_auto_anim
    ancho_img = imagen_auto_anim.get_width()
    if direccion_auto_anim == 1 and posicion_auto_anim > ANCHO + ancho_img:
        posicion_auto_anim = -ancho_img
    elif direccion_auto_anim == -1 and posicion_auto_anim < -ancho_img:
        posicion_auto_anim = ANCHO + ancho_img
    estela = pygame.Surface((int(ancho_img * 1.8), int(imagen_auto_anim.get_height() * 1.2)), pygame.SRCALPHA)
    pygame.draw.ellipse(estela, (255, 230, 0, 60), (0, int(imagen_auto_anim.get_height() * 0.1), int(ancho_img * 1.5), int(imagen_auto_anim.get_height())))
    if direccion_auto_anim == 1:
        pantalla.blit(estela, (posicion_auto_anim - ancho_img * 0.5, ALTO - 75))
        pantalla.blit(imagen_auto_anim, (posicion_auto_anim, ALTO - 90))
    else:
        estela_volteada = pygame.transform.flip(estela, True, False)
        img_volteada = pygame.transform.flip(imagen_auto_anim, True, False)
        pantalla.blit(estela_volteada, (posicion_auto_anim - ancho_img * 0.3, ALTO - 75))
        pantalla.blit(img_volteada, (posicion_auto_anim, ALTO - 90))
def dibujar_taller():
    dibujar_taller_fondo()
    titulo = fuente_grande.render("Elige Un Auto", True, BLANCO)
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO//2, 50)))
    dibujar_panel_seleccion(250, 120, seleccion_j1, "JUGADOR 1", "A", "D", "S", seleccion_j2["color"])
    dibujar_panel_seleccion(750, 120, seleccion_j2, "JUGADOR 2", "←", "→", "Enter", seleccion_j1["color"])
    if seleccion_j1["listo"] and seleccion_j2["listo"]:
        pygame.draw.rect(pantalla, (27, 94, 32), (ANCHO//2 - 300, ALTO - 55, 600, 42), border_radius=12)
        pygame.draw.rect(pantalla, DORADO, (ANCHO//2 - 300, ALTO - 55, 600, 42), 3, border_radius=12)
        txt = fuente.render("🏁 ¡EL PRIMERO EN LLEGAR A LA META GANA! Que gane el más rápido... 🏁", True, AMARILLO_POTENCIA)
        pantalla.blit(txt, txt.get_rect(center=(ANCHO//2, ALTO - 34)))
    dibujar_auto_animacion()
def dibujar_fin_carrera():
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 190))
    pantalla.blit(capa, (0, 0))
    color_ganador = DORADO if ganador.startswith("JUGADOR") else (180, 180, 255)
    txt_ganador = fuente_grande.render(f"¡GANÓ {ganador}! 🏆", True, color_ganador)
    pantalla.blit(txt_ganador, txt_ganador.get_rect(center=(ANCHO//2, ALTO//2 - 40)))
    d1, d2, d3, d4 = distancia1, distancia2, distancia3, distancia4
    txt_dist = fuente_pequena.render(
        f"J1: {d1:.0f}m  |  J2: {d2:.0f}m  |  IA1: {d3:.0f}m  |  IA2: {d4:.0f}m  |  Meta: {DISTANCIA_META}m",
        True, BLANCO
    )
    pantalla.blit(txt_dist, txt_dist.get_rect(center=(ANCHO//2, ALTO//2 + 20)))
    tiempo = pygame.time.get_ticks()
    alfa = int(120 + 135 * abs(math.sin(tiempo / 350)))
    txt_reiniciar = fuente.render("► Presiona ESPACIO → Volver al Taller ◄", True, BLANCO)
    sup_reiniciar = pygame.Surface((txt_reiniciar.get_width() + 40, txt_reiniciar.get_height() + 15), pygame.SRCALPHA)
    sup_reiniciar.blit(txt_reiniciar, (20, 7))
    sup_reiniciar.set_alpha(alfa)
    pygame.draw.rect(sup_reiniciar, (30, 40, 60), (0, 0, sup_reiniciar.get_width(), sup_reiniciar.get_height()), border_radius=8)
    pantalla.blit(sup_reiniciar, sup_reiniciar.get_rect(center=(ANCHO//2, ALTO//2 + 85)))
# =========================================================
# BUCLE PRINCIPAL
# =========================================================
iniciar_juego_nuevo()
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if estado_juego == ESTADO_BIENVENIDA:
                if mostrar_presionar_tecla and not transicion_a_taller:
                    transicion_a_taller = True
            elif estado_juego == ESTADO_TALLER:
                if not seleccion_j1["listo"]:
                    if evento.key == pygame.K_a:
                        seleccion_j1["color"] = (seleccion_j1["color"] - 1) % 4
                        while seleccion_j1["color"] == seleccion_j2["color"]:
                            seleccion_j1["color"] = (seleccion_j1["color"] - 1) % 4
                    if evento.key == pygame.K_d:
                        seleccion_j1["color"] = (seleccion_j1["color"] + 1) % 4
                        while seleccion_j1["color"] == seleccion_j2["color"]:
                            seleccion_j1["color"] = (seleccion_j1["color"] + 1) % 4
                    if evento.key == pygame.K_s:
                        seleccion_j1["listo"] = True
                if not seleccion_j2["listo"]:
                    if evento.key == pygame.K_LEFT:
                        seleccion_j2["color"] = (seleccion_j2["color"] - 1) % 4
                        while seleccion_j2["color"] == seleccion_j1["color"]:
                            seleccion_j2["color"] = (seleccion_j2["color"] - 1) % 4
                    if evento.key == pygame.K_RIGHT:
                        seleccion_j2["color"] = (seleccion_j2["color"] + 1) % 4
                        while seleccion_j2["color"] == seleccion_j1["color"]:
                            seleccion_j2["color"] = (seleccion_j2["color"] + 1) % 4
                    if evento.key == pygame.K_RETURN:
                        seleccion_j2["listo"] = True
            elif estado_juego == ESTADO_CARRERA and ganador is None:
                if evento.key == pygame.K_a: auto1_pos = max(-0.85, auto1_pos - 0.07)
                if evento.key == pygame.K_d: auto1_pos = min(0.85, auto1_pos + 0.07)
                if evento.key == pygame.K_LEFT: auto2_pos = max(-0.85, auto2_pos - 0.07)
                if evento.key == pygame.K_RIGHT: auto2_pos = min(0.85, auto2_pos + 0.07)
            elif estado_juego == ESTADO_FIN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_carrera_volver_taller()
    if estado_juego == ESTADO_BIENVENIDA:
        dibujar_bienvenida()
    elif estado_juego == ESTADO_TALLER:
        dibujar_taller()
        if seleccion_j1["listo"] and seleccion_j2["listo"]:
            contador_inicio += 1
            if contador_inicio > 120:
                reiniciar_carrera_volver_taller()
                seleccion_j1["listo"] = True
                seleccion_j2["listo"] = True
                estado_juego = ESTADO_CARRERA
    elif estado_juego == ESTADO_CARRERA and ganador is None:
        ia1_color, ia2_color = obtener_autos_ia()
        # =====================================================
        # GUARDAR EL FRAME ANTERIOR
        # =====================================================
        distancia_anterior1 = distancia1
        distancia_anterior2 = distancia2
        distancia_anterior3 = distancia3
        distancia_anterior4 = distancia4
        auto1_pos_anterior = auto1_pos
        auto2_pos_anterior = auto2_pos
        auto3_pos_anterior = auto3_pos
        auto4_pos_anterior = auto4_pos
        distancia1 += velocidad1
        distancia2 += velocidad2
        distancia3 += velocidad3
        distancia4 += velocidad4
        auto3_pos = -0.15 + math.sin(distancia3 * 0.005) * 0.18
        auto4_pos = 0.15 + math.sin(distancia4 * 0.004) * 0.15
        actualizar_efectos()
        comprobar_objetos()
        comprobar_ganador()
        if ganador:
            estado_juego = ESTADO_FIN
        dibujar_carretera()
        dibujar_paisaje()
        dibujar_objetos()
        dibujar_meta(max(distancia1, distancia2, distancia3, distancia4))
        autos_lista = [
            (distancia3, auto3_pos, ia1_color, efecto3),
            (distancia4, auto4_pos, ia2_color, efecto4),
            (distancia2, auto2_pos, seleccion_j2["color"], efecto2),
            (distancia1, auto1_pos, seleccion_j1["color"], efecto1),
        ]
        autos_lista.sort(key=lambda x: -x[0])
        for dist, pos, indice_img, ef in autos_lista:
            x, y, escala = calcular_posicion_visual(dist, pos)
            tipo_efecto = "velocidad" if ef > 0 else ("freno" if ef < 0 else None)
            dibujar_auto(x, y, escala, indice_img, tipo_efecto)
        dist_restante = max(0, DISTANCIA_META - max(distancia1, distancia2, distancia3, distancia4))
        progreso = int(100 - (dist_restante / DISTANCIA_META) * 100)
        info = f"J1: {velocidad1:.1f}   J2: {velocidad2:.1f}   IA1: {velocidad3:.1f}   IA2: {velocidad4:.1f}   |   Progreso: {progreso}%   Restante: {int(dist_restante)}m"
        pygame.draw.rect(pantalla, (0, 0, 0, 140), (15, 12, ANCHO - 30, 95), border_radius=10)
        pantalla.blit(fuente_pequena.render(info, True, BLANCO), (25, 18))
        y_info = 42
        for na, vel, ef in [(1, velocidad1, efecto1), (2, velocidad2, efecto2), (3, velocidad3, efecto3), (4, velocidad4, efecto4)]:
            nombre = ["", "J1", "J2", "IA1", "IA2"][na]
            if ef > 0:
                txt = fuente_pequena.render(f"⚡ {nombre} VELOZ! ({ef//60+1}s)", True, AMARILLO_POTENCIA)
                pantalla.blit(txt, (25, y_info))
                y_info += 18
            elif ef < 0:
                txt = fuente_pequena.render(f"⚠️ {nombre} LENTO! ({abs(ef)//60+1}s)", True, NARANJA_FRENO)
                pantalla.blit(txt, (25, y_info))
                y_info += 18
    elif estado_juego == ESTADO_FIN:
        d1, d2, d3, d4 = distancia1, distancia2, distancia3, distancia4
        dibujar_carretera()
        dibujar_paisaje()
        dibujar_objetos()
        dibujar_meta(max(d1, d2, d3, d4))
        ia1_color, ia2_color = obtener_autos_ia()
        autos_lista = [
            (distancia3, auto3_pos, ia1_color, efecto3),
            (distancia4, auto4_pos, ia2_color, efecto4),
            (distancia2, auto2_pos, seleccion_j2["color"], efecto2),
            (distancia1, auto1_pos, seleccion_j1["color"], efecto1),
        ]
        autos_lista.sort(key=lambda x: -x[0])
        for dist, pos, indice_img, ef in autos_lista:
            x, y, escala = calcular_posicion_visual(dist, pos)
            tipo_efecto = "velocidad" if ef > 0 else ("freno" if ef < 0 else None)
            dibujar_auto(x, y, escala, indice_img, tipo_efecto)
        dibujar_fin_carrera()
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()