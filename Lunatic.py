import pygame
import random

game_page_start = "Start"
game_page_score = "Score"
game_page_game_over = "GameOver"
game_page_win = "Win"
game_page_game = "Game"

pygame.display.set_caption('Invasion')
current_game_page = game_page_start

road1 = 5
road2 = 105
road3 = 205
road4 = 305

y_start  = 100
y_silver_goal = 430
y_gold_goal = 470
y_fail = 600

current_level = 1
didnt_count = 70
total_score = 0
best_score = 0
monster_count = 1
kill_monster_count = 0


pygame.mixer.init() # для звука
miss = pygame.mixer.Sound('miss.wav')
death = pygame.mixer.Sound('total_miss.wav')
kill = pygame.mixer.Sound('hit.wav')
correct = pygame.mixer.Sound('count.wav')
pygame.mixer.music.load("begin.mp3")

size = 600, 600
pygame.display.set_caption("My Game") # переименование окна
icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
background_image = pygame.image.load("first.jpg")
wait = ""
time = pygame.time.Clock()

pygame.init()# запускает pygame

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Invasion')
# arrow = pygame.image.load('creature.png') # загрузка инопланитанина
# arrow.set_colorkey((255, 255, 255))
x, y = road1, -100
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
running = True

def random_creature():
    lucky = random.randint(1, 4)
    if lucky == 1:
        return "creature.png"
    elif lucky == 2:
        return "ghost.png"
    elif lucky == 3:
        return "three.png"
    elif lucky == 4:
        return "two.png"

levels_data = [(0, '', 0, 0), (5, random_creature(), 10, 5), (7, random_creature(), 10, 6), (10, random_creature(), 10, 7), (15, random_creature(), 10, 8)]

arrow = pygame.image.load(levels_data[current_level][1]) # загрузка инопланитанина
arrow.set_colorkey((255, 255, 255))

def number():
    luck = random.randint(1, 4)
    if luck == 1:
        return road1
    elif luck == 2:
        return road2
    elif luck == 3:
        return road3
    elif luck == 4:
        return road4

def terminate():
    pygame.quit()

def drawText(intro_text, color, x, y):
    font = pygame.font.Font(None, 30)
    text_coord = y
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = x
        intro_rect.y = text_coord
        text_coord += intro_rect.height + 10
        screen.blit(string_rendered, intro_rect)

def show_total_score():
    global total_score
    global current_game_page
    global current_level
    global monster_count
    global kill_monster_count
    global x
    global arrow
    x = -100
    pygame.mixer.music.pause()
    intro_text = ["Поздравляю уровень пройден!", f"Cчет: {total_score}"]
    
    
    fon_intro = pygame.transform.scale(pygame.image.load('score.png'), (size))
    screen.blit(fon_intro, (0, 0))

    drawText(intro_text, "yellow", 150, 250)

    # fon_intro = pygame.font.Font(None, 30)
    # text_coord = 50
    # for line in intro_text:
    #     string_rendered = fon_intro.render(line, 1, pygame.Color('yellow'))# Написание текста
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 250
    #     intro_rect.top = text_coord
    #     intro_rect.x = 250
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        current_game_page = game_page_game
        current_level += 1
        monster_count = 1
        kill_monster_count = 0
        arrow = pygame.image.load(levels_data[current_level][1]) # загрузка инопланитанина
        arrow.set_colorkey((255, 255, 255))
        pygame.mixer.music.unpause()


def start_screen(): # Заставка 
    global current_game_page

    intro_text = ["Вторжение пришельцев", "",
                  "Правила игры:",
                  "Убивай всех кто попадает на стрелки",
                  "со временем они сильно ускоряются ",
                  "",
                  "(для продолжения нажмите пробел)"]
    
    

    fon_intro = pygame.transform.scale(pygame.image.load('plate2.jpg'), (size))
    screen.blit(fon_intro, (0, 0))

    drawText(intro_text, "white", 50, 50)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_SPACE]:
        pygame.mixer.music.play()
        current_game_page = game_page_game

def load_best_score():
    global best_score
    lis = []
    with open("best_score.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            lis.append(int(line))
        best_score = max(lis)

def save_best_score():
    global total_score
    global best_score
    with open("best_score.txt", "a") as file:
        file.writelines(str(total_score) + "\n")
    best_score = max(best_score, total_score)

def show_win():
    global x
    x = -100

    pygame.mixer.music.pause()
    fon_intro = pygame.transform.scale(pygame.image.load('victory.png'), (size))
    screen.blit(fon_intro, (0, 0))

    drawText(["Congratulaitons! You Win!", f"Current Score: {total_score}", f"Best Score: {best_score}"], "red", 250, 400)

def game_over():
    global x
    x = -100

    pygame.mixer.music.pause()
    fon_intro = pygame.transform.scale(pygame.image.load('aliens.jpg'), (size))
    screen.blit(fon_intro, (0, 0))
    lis = []

    drawText(["Game Over", f"Current Score: {total_score}", f"Best Score: {best_score}"], "red", 250, 400)

def maingame():
    global current_game_page
    global monster_count
    global kill_monster_count
    global current_level
    global x, y
    global total_score
    if monster_count > levels_data[current_level][2]:
        if kill_monster_count >= levels_data[current_level][3]:
            current_game_page = game_page_score
            if current_level > len(levels_data):
                print('The End')    
                current_game_page = game_page_win
                return
        else:
            print('Game Over')
            current_game_page = game_page_game_over
            save_best_score()
            return

    #screen.fill((255, 255, 255))
    screen.blit(background_image,(0, 0))
    # Создание полос
    
    pygame.draw.line(screen, "black", [100, 0], [100, 600], 2)
    pygame.draw.line(screen, "black", [200, 0], [200, 600], 2)
    pygame.draw.line(screen, "black", [300, 0], [300, 600], 2)
    pygame.draw.line(screen, "black", [400, 0], [400, 600], 2)
    pygame.draw.line(screen, "white", [0, 500], [400, 500], 4)
    cursor_left = pygame.image.load("Left.png")
    cursor_up = pygame.image.load("Right.png")
    cursor_right = pygame.image.load("Up.png")
    cursor_down = pygame.image.load("Down.png")
    screen.blit(cursor_left, (15, 515))
    screen.blit(cursor_up, (115, 515))
    screen.blit(cursor_right, (215, 515))
    screen.blit(cursor_down, (315, 515))
    cursor_left.set_colorkey((255, 255, 255))

    drawText([f"Score: {total_score}", f"Level: {current_level}"], "blue", 450, 50)
    drawText([f"Best score: {best_score}"], "red", 420, 300)
    if best_score < total_score:
        drawText([f"NEW BEST SCORE"], "yellow", 410, 400)

    if y > y_fail:
        arrow = pygame.image.load(random_creature())
        if total_score == 0:
            x, y = number(), 0
            miss.play()
            monster_count += 1
        elif total_score == 5:
            total_score -= 5
            x, y = number(), 0
            miss.play()
            monster_count += 1
        else:
            total_score -= 10
            death.play()
            x, y = number(), 0
            monster_count += 1
    else:
        y += levels_data[current_level][0]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:

        if y < y_start:
            pass
        elif y > y_gold_goal and x == road1:
            total_score += 10
            kill.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y > y_silver_goal and x == road1:
            total_score += 5
            correct.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y < didnt_count:
            pass
        else:
            if total_score == 0:
                x, y = number(), 0
                miss.play()
                monster_count += 1
            else:
                total_score -= 5
                x, y = number(), 0
                miss.play()
                monster_count += 1

    if keys[pygame.K_RIGHT]:

        if y < y_start:
            pass
        if y > y_gold_goal and x == road2:
            total_score += 10
            kill.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y > y_silver_goal and x == road2:
            total_score += 5
            correct.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y < didnt_count:
            pass
        else:
            if total_score == 0:
                x, y = number(), 0
                miss.play()
                monster_count += 1
            else:
                total_score -= 5
                x, y = number(), 0
                miss.play()
                monster_count += 1

    if keys[pygame.K_UP]:

        if y < y_start:
            pass
        if y > y_gold_goal and x == road3:
            total_score += 10
            kill.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y > y_silver_goal and x == road3:
            total_score += 5
            correct.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y < didnt_count:
            pass
        else:
            if total_score == 0:
                x, y = number(), 0
                miss.play()
                monster_count += 1
            else:
                total_score -= 5
                x, y = number(), 0
                miss.play()
                monster_count += 1

    if keys[pygame.K_DOWN]:

        if y < y_start:
            pass

        if y > y_gold_goal and x == road4:
            total_score += 10
            kill.play()
            kill_monster_count += 1
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y > y_silver_goal and x == road4:
            total_score += 5
            correct.play()
            arrow = pygame.image.load(random_creature())
            x, y = number(), 0
            monster_count += 1
        elif y < didnt_count:
            pass
        else:
            if total_score == 0:
                x, y = number(), 0
                miss.play()
                monster_count += 1
            else:
                total_score -= 5
                x, y = number(), 0
                miss.play()
                monster_count += 1


    if total_score < 0:
        total_score = 0

load_best_score()

while running:
    if current_game_page == game_page_start:
        start_screen() # Запуск заставки
    elif current_game_page == game_page_game:
        maingame()
    elif current_game_page == game_page_score:
        show_total_score()
    elif current_game_page == game_page_win:
        show_win()
    elif current_game_page == game_page_game_over:
        game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(arrow, (x, y))
    pygame.display.flip()
    pygame.display.update()
    time.tick(50)

pygame.quit()
