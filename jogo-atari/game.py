import pygame
import sys
from settings import *
from sprites import Player, Asteroid, Bullet

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Atari Asteroids")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30)
        self.running = True
        self.playing = False
        self.score = 0
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Variável para controlar a taxa de criação de asteroides
        self.asteroid_timer = 0

    def new_game(self):
        # Limpa todos os sprites se estiver reiniciando
        self.all_sprites.empty()
        self.asteroids.empty()
        self.bullets.empty()
        
        # Recria o jogador
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Reseta as variáveis de estado
        self.score = 0
        self.playing = True
        self.asteroid_timer = 0
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)

    def update(self):
        self.all_sprites.update()
        
        # Lógica de criação de novos asteroides
        self.asteroid_timer += 1
        if self.asteroid_timer >= ASTEROID_SPAWN_RATE:
            self.asteroid_timer = 0
            asteroid = Asteroid()
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)
            
        # Colisão entre tiros e asteroides
        # True, True significa que ambos serão deletados ao colidir
        hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
        for hit in hits:
            self.score += 10 # Adiciona 10 pontos por acerto
            
        # Colisão entre a nave do jogador e os asteroides
        hits = pygame.sprite.spritecollide(self.player, self.asteroids, False)
        if hits:
            self.playing = False # Fim de jogo
            
        # Verifica se algum asteroide passou do limite inferior da tela
        for asteroid in self.asteroids:
            if asteroid.rect.top > HEIGHT:
                self.playing = False # Fim de jogo

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # Exibe a pontuação no canto superior esquerdo
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Pressione ESPAÇO para reiniciar ou ESC para sair", True, WHITE)
        
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        pygame.display.flip()
        
        waiting = True
        while waiting and self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False

    def run(self):
        self.new_game()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.run()
        if game.running:
            game.show_game_over_screen()
    pygame.quit()
    sys.exit()
