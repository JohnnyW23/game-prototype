import pygame


class Game:
    def __init__(self):
        from character import generate_character

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.last_press_time = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_UP: 0,
            pygame.K_DOWN: 0
        }

        self.double_tap_delay = 200

        self.character = generate_character()

        self.character.is_running = False
        self.character.run_direction = None

        self.running = True
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    now = pygame.time.get_ticks()

                    if event.key in self.last_press_time:
                        if now - self.last_press_time[event.key] <= self.double_tap_delay:

                            # ativa corrida
                            self.character.is_running = True
                            self.character.run_direction = event.key

                    self.last_press_time[event.key] = now

            keys = pygame.key.get_pressed()

            moving = False

            speed = 75  # walk

            # se estiver correndo
            if self.character.is_running:
                speed = 200

            if keys[pygame.K_LEFT]:
                self.character.x -= speed * dt / 1000
                self.character.direction_row = 1
                moving = True

                # se soltou a direção do run → cancela corrida
                if self.character.run_direction != pygame.K_LEFT:
                    self.character.is_running = False

            elif keys[pygame.K_RIGHT]:
                self.character.x += speed * dt / 1000
                self.character.direction_row = 3
                moving = True

                if self.character.run_direction != pygame.K_RIGHT:
                    self.character.is_running = False

            elif keys[pygame.K_UP]:
                self.character.y -= speed * dt / 1000
                self.character.direction_row = 0
                moving = True

                if self.character.run_direction != pygame.K_UP:
                    self.character.is_running = False

            elif keys[pygame.K_DOWN]:
                self.character.y += speed * dt / 1000
                self.character.direction_row = 2
                moving = True

                if self.character.run_direction != pygame.K_DOWN:
                    self.character.is_running = False


            if moving:
                if self.character.is_running:
                    self.character.set_mode("Run")
                else:
                    self.character.set_mode("Walk")
            else:
                self.character.is_running = False
                self.character.set_mode("Idle")

            self.character.update(dt)

            # desenhar
            self.screen.fill((30, 30, 30))
            self.character.draw(self.screen, (self.character.x, self.character.y))

            pygame.display.flip()


game = Game()
game.run()