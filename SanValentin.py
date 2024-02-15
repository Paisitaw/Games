import pygame 
import sys
import random

# Inciador de Juego
pygame.init()

# Configuración de pantalla
width, height = 700, 775
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Disparando con la ROLIS")

# Cargar las imagenes y escalarlas
player_image = pygame.image.load("img/Rolis.png")
player_image = pygame.transform.scale(player_image, (60, 60))

bullet_image = pygame.image.load("img/Heart.png")
bullet_image = pygame.transform.scale(bullet_image, (50, 50))

enemy_image = pygame.image.load("img/Cat.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

background_image = pygame.image.load("img/Fondo.png")
background_image = pygame.transform.scale(background_image, (width, height))


# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
player_speed = 15

# Balas
bullet_rect = bullet_image.get_rect()
bullet_speed = 10
bullets = []

# Enemigo
enemy_rect = enemy_image.get_rect()
enemy_speed = 5
enemies = []

# Reloj
clock = pygame.time.Clock()

# Mantener registro de teclas presionadas
key_pressed = {'left': False, 'right': False}

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejar movimientos del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key_pressed['left'] = True
            elif event.key == pygame.K_RIGHT:
                key_pressed['right'] = True
            elif event.key == pygame.K_SPACE:
                bullet_rect = bullet_image.get_rect()
                bullet = {
                    'rect': pygame.Rect(
                        player_rect.x + player_rect.width // 2 - bullet_rect.width // 2,
                        player_rect.y,
                        bullet_rect.width,
                        bullet_rect.height
                    ),
                    'image': bullet_image
                }
                bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                key_pressed['right'] = False

        # Actualizar posición de jugador
        if key_pressed['left'] and player_rect.left > 0:
            player_rect.x -= player_speed
        if key_pressed['right'] and player_rect.right < width:
            player_rect.x += player_speed

    # Actualizar posición de balas
    for bullet in bullets:
        bullet['rect'].y -= bullet_speed

    # Generar enemigos aleatorios
    if random.randint(0, 100) < 5:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = random.randint(0, width - enemy_rect.width)
        enemies.append(enemy_rect.copy())

    # Actualizar posición de enemigos
    for enemy in enemies:
        enemy.y += enemy_speed

    # Colisiones entre balas y enemigos
    for bullet in bullets:
        for enemy in enemies:
            if enemy.colliderect(bullet['rect']):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Colisiones entre jugador y enemigos
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            pygame.quit()
            sys.exit()

    # Limpiar pantalla con el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar al jugador
    screen.blit(player_image, player_rect)

    # Dibujar las balas
    for bullet in bullets:
        screen.blit(bullet['image'], bullet['rect'].topleft)

    # Dibujar los enemigos
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Actualizar pantalla
    pygame.display.flip()

    # Limite de FPS
    clock.tick(30)