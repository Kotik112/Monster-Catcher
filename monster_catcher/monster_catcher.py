"""Credit for monster assets to:  http://www.blog.spoongraphics.co.uk"""

import random

import pygame

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Monster Catcher")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


class Game():
    """A class to control gameplay"""
    def __init__(self, player, monster_group):
        """Initilize the game object"""
        #Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        #Set sounds and music
        self.next_level_sound = pygame.mixer.Sound("assets/next_level.wav")

        #Set font
        self.font = pygame.font.Font("assets/Abrushow.ttf", 24)

        #Set images
        blue_image = pygame.image.load("assets/blue_monster.png")
        green_image = pygame.image.load("assets/green_monster.png")
        purple_image = pygame.image.load("assets/purple_monster.png")
        yellow_image = pygame.image.load("assets/yellow_monster.png")
        #This list cooresponds to the monster_type attribute int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]

        self.target_monster_type = random.randint(0,3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH//2
        self.target_monster_rect.top = 30

    def update(self):
        """Update the game"""
        self.frame_count += 1
        if self.frame_count >= FPS:
            self.round_time += 1
            self.frame_count = 0

        #Check for collision
        self.check_collisions()

    def draw(self):
        """Draw the HUD and other to the display"""
        # Set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # Add the monster colors to a list where the index of the color matches target_monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # Set text
        catch_text = self.font.render("Current Catch", True, WHITE).convert_alpha()
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top = 5

        score_text = self.font.render("Score: " + str(self.score), True, WHITE).convert_alpha()
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE).convert_alpha()
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Current Round: " + str(self.round_number), True, WHITE).convert_alpha()
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round Time: " + str(self.round_time), True, WHITE).convert_alpha()
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE).convert_alpha()
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        #Blit the HUD
        screen.blit(catch_text, catch_rect)
        screen.blit(score_text, score_rect)
        screen.blit(lives_text, lives_rect)
        screen.blit(round_text, round_rect)
        screen.blit(time_text, time_rect)
        screen.blit(warp_text, warp_rect)
        screen.blit(self.target_monster_image, self.target_monster_rect)

        #Draw rectangle around target monster
        pygame.draw.rect(screen, colors[self.target_monster_type], (WINDOW_WIDTH // 2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(screen, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

    def check_collisions(self):
        """Check for collisions between player and monsters"""
        #Check for collision between player and an individual monster
        #We must test the type of monster to see if it matches the target monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        #We collided with a monster
        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                #Remove caught monster
                collided_monster.remove(self.monster_group)

                if self.monster_group:
                    #There are more monsters to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()   #WIP

                else:
                    #Round is complete
                    self.player.reset()
                    self.start_new_round()

            #Caught the wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1

                #Check for game over
                if self.player.lives <= 0:
                    self.pause_game("Final score: " + str(self.score), "Press enter to play again!")
                    self.reset_game()
                self.player.reset()



    def start_new_round(self):
        """Populate board with new monsters"""
        #Calculate score bonus based on how quickly the round was finished
        self.score += int(10000 * self.round_number / (1 + self.round_time))

        #reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        #Remove any remaining monster from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)


        #Add monster to the monster group
        for i in range(self.round_number):
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[0], 0))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[1], 1))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[2], 2))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[3], 3))

            #Choose a new target monster
            self.choose_new_target()

            self.next_level_sound.play()

    def choose_new_target(self):
        """Choose a new target monster for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Create the sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        #Display the pause text
        screen.fill(BLACK)
        screen.blit(main_text, main_rect)
        screen.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()

class Player(pygame.sprite.Sprite):
    """A player class that the user can control"""

    def __init__(self):
        """Initialize the player"""
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound("assets/catch.wav")
        self.die_sound = pygame.mixer.Sound("assets/die.wav")
        self.warp_sound = pygame.mixer.Sound("assets/warp.wav")

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_w] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity


    def warp(self):
        """Warp the player to the bottom 'safe zone'"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        """Resets the players position"""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

class Monster(pygame.sprite.Sprite):
    """A class to create enemy monster objects"""
    def __init__(self, x, y, image, monster_type):
        """Initialize the monster"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Monster type is an int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.type = monster_type

        #Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

    def update(self):
        """Update the monster"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # Bounce the monster off the edges of the display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = -1 * self.dy

    def warp(self):
        """Warp the player back to starting position"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        """Resets the player's position"""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

#Create player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#Create a monster group
my_monster_group = pygame.sprite.Group()


#Create a game object
my_game = Game(my_player, my_monster_group)
my_game.pause_game("Monster Catcher", "Press 'Enter' to begin")
my_game.start_new_round()

#The main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    #Fill the display
    screen.fill((0, 0, 0))

    #Update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(screen)

    my_monster_group.update()
    my_monster_group.draw(screen)

    my_game.update()
    my_game.draw()

    #update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)
