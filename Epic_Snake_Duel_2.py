import pygame
import random
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Define constants
FPS = 15

mixer.music.load('Epic_music.mp3')
start_time = 107
#mixer.music.play(-1, start_time)

# Set up the game window
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Epic Cobra Duel 2")
clock = pygame.time.Clock()
WIDTH, HEIGHT = win.get_size()



#Set up the class of snake
class Snake:
    # Initialize the snake
    def __init__(self, start_pos):
        self.segment_size = 20  # Grid size
        self.size = 5
        # Align the start position with the grid
        grid_x = (start_pos[0] // self.segment_size) * self.segment_size
        grid_y = (start_pos[1] // self.segment_size) * self.segment_size
        self.elements = [[grid_x, grid_y]]
        self.dir = 'RIGHT' if start_pos[0] < WIDTH // 2 else 'LEFT'
        self.color = (250, 173, 5)
    
    # Get the head position
    def get_head_position(self):
        return self.elements[0]
   
    # Snake Movement
    def move(self):
        head = self.get_head_position()
        x_move, y_move = 0, 0

        if self.dir == 'UP':
            y_move = -self.segment_size
        elif self.dir == 'DOWN':
            y_move = self.segment_size
        elif self.dir == 'LEFT':
            x_move = -self.segment_size
        elif self.dir == 'RIGHT':
            x_move = self.segment_size

        new_head = [head[0] + x_move, head[1] + y_move]

        # Teleportation through the edges
        new_head[0] %= WIDTH
        new_head[1] %= HEIGHT
        self.elements.insert(0, new_head)
        if len(self.elements) > self.size:
            self.elements.pop()
    
    # Direction controls for the snake
    def change_direction(self, new_dir):
        if new_dir == 'UP' and not self.dir == 'DOWN':
            self.dir = 'UP'
        if new_dir == 'DOWN' and not self.dir == 'UP':
            self.dir = 'DOWN'
        if new_dir == 'LEFT' and not self.dir == 'RIGHT':
            self.dir = 'LEFT'
        if new_dir == 'RIGHT' and not self.dir == 'LEFT':
            self.dir = 'RIGHT'
    
    # Snake Apperance
    def draw(self, surface, color=None):
        for element in self.elements:
            pygame.draw.rect(surface, self.color if color is None else color, pygame.Rect(element[0], element[1], self.segment_size, self.segment_size))


#Set up the class of food
class Food:
    def __init__(self):
        self.grid_size = 20  # Assuming the snake segment size is 20
        self.respawn_food()
    
    # Respawn food in a random position on the map, aligned with the grid
    def respawn_food(self):
        # Calculate the effective area for food spawning
        effective_width = WIDTH - (WIDTH % self.grid_size)
        effective_height = HEIGHT - (HEIGHT % self.grid_size)

        # Choose a random position within the effective area
        self.position = [
            random.randint(0, (effective_width // self.grid_size) - 1) * self.grid_size,
            random.randint(0, (effective_height // self.grid_size) - 1) * self.grid_size
        ]

        # Debugging: Print the position of the food to help diagnose alignment issues
        print(f"Food spawned at: {self.position}")

    # Food Design/Appearance
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], self.grid_size, self.grid_size))



#Collision Detection for the snake (between head and body of the two snakes)
def check_snake_collision(snake1, snake2):
    head1 = snake1.get_head_position()
    head2 = snake2.get_head_position()

    # Check for head-on collision (with a tolerance for near misses)
    distance = ((head1[0] - head2[0]) ** 2 + (head1[1] - head2[1]) ** 2) ** 0.5
    if distance < max(snake1.segment_size, snake2.segment_size):
        return 'tie'

    # Check if snake1's head collides with any part of snake2
    for segment in snake2.elements:
        if head1 == segment:
            return snake1  # Snake1 loses

    # Check if snake2's head collides with any part of snake1
    for segment in snake1.elements:
        if head2 == segment:
            return snake2  # Snake2 loses

    return None



#Game Over Screen and Score board
def game_over_screen(loser_snake, snake1_score, snake2_score):
    # Display scores and winning message
    win.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    large_font = pygame.font.Font(None, 100)
    win_msg = None

    if loser_snake == 'tie':
        win_msg = large_font.render('It\'s a Tie!', True, (255, 255, 255))
    elif loser_snake == 'snake1':
        winner = 'Blue'
        textColor = (5, 165, 250)
        win_msg = large_font.render(f'{winner} Snake Wins the Round!', True, textColor)
    elif loser_snake == 'snake2':
        winner = 'Yellow'
        textColor = (250, 173, 5)
        win_msg = large_font.render(f'{winner} Snake Wins the Round!', True, textColor)


    yellow_v_blue = font.render(f'Yellow               Blue', True, (250, 255, 255))
    scores_output = font.render(f'{snake1_score}                     {snake2_score}', True, (255, 255, 255))
    further_instrutions = font.render('Press Space to Proceed', True, (255, 255, 255))

    win_msg_rect = win_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    yellow_v_blue_rect = yellow_v_blue.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    scores_output_rect = scores_output.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
    further_instrutions_rect = further_instrutions.get_rect(center=(WIDTH // 2, HEIGHT - 125))


    win.blit(win_msg, win_msg_rect)
    win.blit(yellow_v_blue, yellow_v_blue_rect)
    win.blit(scores_output, scores_output_rect)
    win.blit(further_instrutions, further_instrutions_rect)
    pygame.display.flip()

    pygame.time.wait(1000)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Check if the snake's head is within the bounds of the food (Collision Detection)
def check_food_collision(snake, food):
    head_x, head_y = snake.get_head_position()
    food_x, food_y = food.position

    # Check if the snake's head is within the bounds of the food
    if (food_x <= head_x < food_x + 20) and (food_y <= head_y < food_y + 20):
        snake.size += 3
        food.respawn_food()

def start_menu():
    menu_running = True

    # Load background image
    background_image = pygame.image.load('Epic_Snake_Duel.png')

    # Resize the image to fit the window
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    while menu_running:
        # Draw the background image
        win.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 75)
        text = font.render('Press SPACE to Start', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 125))
        game_name = font.render('EPIC COBRA DUEL 2', True, (255, 255, 255))
        game_name_rect = game_name.get_rect(center=(WIDTH // 2, 125))

        rectangle_background = text.get_rect()
        rectangle_background.inflate_ip(20, 10)  
        rectangle_background.center = text_rect.center
        pygame.draw.rect(win, (0, 0, 0), rectangle_background)

        rectangle_background_2 = game_name.get_rect()
        rectangle_background_2.inflate_ip(20, 10)
        rectangle_background_2.center = game_name_rect.center
        pygame.draw.rect(win, (0, 0, 0), rectangle_background_2)

        win.blit(text, text_rect)
        win.blit(game_name, game_name_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False
    return True

def end_of_game(snake1_score, snake2_score):
    win.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    if snake1_score > snake2_score:
        winner_msg = font.render('Yellow Cobra Wins!', True, (250, 173, 5))
    else:
        winner_msg = font.render('Blue Cobra Wins!', True, (5, 165, 250))

    winner_msg_rect = winner_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(winner_msg, winner_msg_rect)
    pygame.display.flip()
    mixer.music.stop()
    pygame.time.wait(5000)

def main_game_loop():
    snake1_score = 0
    snake2_score = 0

    if not start_menu():
        return

    running = True
    snake1 = Snake([60, 50])
    snake2 = Snake([WIDTH - 60, 50])
    food = Food()

    while running:
        win.fill((0, 0, 0)) # Backgorund

        # Check for food collision
        check_food_collision(snake1, food)
        check_food_collision(snake2, food)

        # Check if the snake's head is within the bounds of the food
        collision_result = check_snake_collision(snake1, snake2)
        if collision_result:
            # Handle game over screen
            if collision_result == 'tie':
                game_over_screen('tie', snake1_score, snake2_score)
            elif collision_result == snake1:
                snake2_score += 1
                game_over_screen('snake1', snake1_score, snake2_score)
            elif collision_result == snake2:
                snake1_score += 1
                game_over_screen('snake2', snake1_score, snake2_score)

            # Check if the game should end
            if snake1_score == 5 or snake2_score == 5:
                end_of_game(snake1_score, snake2_score)
                break  # End the game

            # Reset the game state for a new round
            snake1 = Snake([60, 50])
            snake2 = Snake([WIDTH - 60, 50])
            food = Food()
            continue



        # Drawing snakes and food
        snake1.draw(win)
        snake2.draw(win, (5, 165, 250))
        food.draw(win)
        # Display updatre r
        pygame.display.flip()
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_w:
                    snake1.change_direction('UP')
                if event.key == pygame.K_s:
                    snake1.change_direction('DOWN')
                if event.key == pygame.K_a:
                    snake1.change_direction('LEFT')
                if event.key == pygame.K_d:
                    snake1.change_direction('RIGHT')

                # Player 2 controls
                if event.key == pygame.K_UP:
                    snake2.change_direction('UP')
                if event.key == pygame.K_DOWN:
                    snake2.change_direction('DOWN')
                if event.key == pygame.K_LEFT:
                    snake2.change_direction('LEFT')
                if event.key == pygame.K_RIGHT:
                    snake2.change_direction('RIGHT')


        snake1.move()
        snake2.move()

    pygame.quit()
#End of main game loop
if __name__ == "__main__":
    main_game_loop()
    pygame.quit()