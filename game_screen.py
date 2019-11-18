import pygame
import random
from os import path
import math

from config import img_dir, snd_dir, fnt_dir, WIDTH, HEIGHT, BLACK, YELLOW, RED, FPS, QUIT

def animation(imgname,time,animname):
    
    for a in np.arange(time):
        filename = "{0} {0}".format(imgname,a)
        img=pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg=pygame.transform.scale(img, (40,40))
        anim[str(animname)].append(img_lg)
    


# Classe Jogador que representa a nave
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        
        # Velocidade da nave
        self.speedx = 0
        self.speedy = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 0
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Classe Mob que representa os meteoros
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, mob_img, player):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = random.randrange(-WIDTH, WIDTH*2)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-HEIGHT,HEIGHT*2)
        #impede que meteoreos apareçam no meio da tela
        while(0<self.rect.x<480 or -600<self.rect.y<0):
            self.rect.x = random.randrange(-WIDTH, WIDTH*2)
            self.rect.y = random.randrange(-HEIGHT,HEIGHT*2)
            
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)

        self.player = player

        
    # Metodo que atualiza a posição do meteoro
    
    def update(self):

        px = self.player.rect.x
        py = self.player.rect.y

        if self.rect.x < px:
            self.speedx = 1
        else:
            self.speedx = -1

        if self.rect.y > py:
            self.speedy = -1
        else:
            self.speedy = 1
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
          
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, mouse, bullet_anim):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.bullet_anim = bullet_anim
        self.index = 0

        # Carregando a imagem de fundo.
        self.image = self.bullet_anim[self.index]
        #alcance
        self.radius = 15
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = y
        self.rect.centerx = x

        self.targetx = mouse[0]
        self.targety = mouse[1]

        dx = (mouse[0] - self.rect.centerx)
        dy = (mouse[1] - self.rect.centery)
       
        self.speedx = dx/15
        self.speedy = dy/15

    # Metodo que atualiza a posição da navinha
    def update(self): 

        self.index += 1
        if self.index > 2:
            self.index = 0
        self.image = self.bullet_anim[self.index]

        if self.speedx == 0:
            self.kill()
        if self.speedy == 0:
            self.kill()
       
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # self.image = bullet_anim[]

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.y < 0 or self.radius == 0:
            self.kill()

# Classe que representa uma explosão de meteoro
class Explosion(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, center, explosion_anim):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Carrega a animação de explosão
        self.explosion_anim = explosion_anim

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Carrega todos os assets uma vez só.
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
    assets["background"] = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    #faz as animações do tiro 
    bullet_anim = []
    for i in range(3):
        filename = 'bullet{0}.png'.format(i)
        img = pygame.image.load(path.join(img_dir,filename)).convert()
        img = pygame.transform.scale(img, (25,25))
        img.set_colorkey(BLACK)
        bullet_anim.append(img)
    assets["bullet_anim"] = bullet_anim
    #faz as animações da explosão         
    explosion_anim = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (32, 32))        
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets

def game_screen(screen):
    # Carrega todos os assets uma vez só e guarda em um dicionário
    assets = load_assets(img_dir, snd_dir, fnt_dir)

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo do jogo
    background = assets["background"]
    background_rect = background.get_rect()

    # Carrega os sons do jogo
    pygame.mixer.music.load(path.join(snd_dir, '16 bit Metal - Iron Maiden - Aces High - Mega Man X.mp3'))
    boom_sound = assets["boom_sound"]
    destroy_sound = assets["destroy_sound"]
    pew_sound = assets["pew_sound"]
    pygame.mixer.music.set_volume(1)
    #pygame.mixer.pew_sound.set_volume(0.4)
    
    # Cria uma nave. O construtor será chamado automaticamente.
    player = Player(assets["player_img"])

    # Carrega a fonte para desenhar o score.
    score_font = assets["score_font"]

    # Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Cria um grupo só dos meteoros
    mobs = pygame.sprite.Group()

    # Cria um grupo para tiros
    bullets = pygame.sprite.Group()

    # Cria 8 meteoros e adiciona no grupo meteoros
    
    for i in range(10):
        m = Mob(assets["mob_img"], player)
        all_sprites.add(m)
        mobs.add(m)

    # Loop principal.
    pygame.mixer.music.play(loops=-1)

    score = 0

    lives = 3

    PLAYING = 0
    EXPLODING = 1
    DONE = 2

    state = PLAYING

    mouse = [0,0]
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        if state == PLAYING:
            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pygame.event.get():
                
                # Verifica se foi fechado.
                if event.type == pygame.QUIT:
                    state = DONE
                
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_a:
                        player.speedx = -8
                    if event.key == pygame.K_d:
                        player.speedx = 8
                    
                    if event.key == pygame.K_w:
                        player.speedy = -8

                    if event.key == pygame.K_s:
                        player.speedy = 8
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:                  
                        bullet = Bullet(player.rect.centerx, player.rect.top, mouse, assets["bullet_anim"])
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        pew_sound.play()
                        
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_a:
                        player.speedx = 0
                    if event.key == pygame.K_d:
                        player.speedx = 0

                    if event.key == pygame.K_w:
                        player.speedy = 0

                    if event.key == pygame.K_s:
                        player.speedy = 0
                

                if event.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                    

                    
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        if state == PLAYING:
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits: # Pode haver mais de um
                # O meteoro e destruido e precisa ser recriado
                destroy_sound.play()
                m = Mob(assets["mob_img"], player) 
                all_sprites.add(m)
                mobs.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(hit.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)

                # Ganhou pontos!
                score += 100
            
            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
                boom_sound.play()
                player.kill()
                lives -= 1
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
                for a in mobs:
                    a.kill()
            
        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Player(assets["player_img"])
                    all_sprites.add(player)
                    
                    for i in range(8):
                        m = Mob(assets["mob_img"], player)
                        all_sprites.add(m)
                        mobs.add(m)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        # Desenha o score
        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)

        # Desenha as vidas
        text_surface = score_font.render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        screen.blit(text_surface, text_rect)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return QUIT