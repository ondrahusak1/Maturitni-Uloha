import pygame, sys, random, sqlite3

conn = sqlite3.connect("game_history.db")
cursor = conn.cursor()
cursor. execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_score INTEGER,
    opponent_score INTEGER
)""")
conn.commit()


def show_databse():
    screen.fill(bg_color)
    history_text = game_font.render("Historie výsledků", True, light_gray)
    back_text = game_font.render("Zpět do hlavního menu", True, light_gray)
    delete_text = game_font.render("Vymazat historii", True, light_gray)

    history_rect = history_text.get_rect(center=(screen_width / 2, screen_height / 3))
    back_rect = back_text.get_rect(center=(screen_width / 2, screen_height / 1.5))
    delete_rect = delete_text.get_rect(center=(screen_width / 2, screen_height / 1.3))

    screen.blit(history_text, history_rect)
    screen.blit(back_text, back_rect)
    screen.blit(delete_text, delete_rect)
    pygame.display.flip()

    # Načtení historie zápasů
    cursor.execute("SELECT player_score, opponent_score FROM history ORDER BY id DESC LIMIT 5")
    history = cursor.fetchall()
    for i, (player_score, opponent_score) in enumerate(history):
        history_text = f"Hráč: {player_score} - CPU: {opponent_score}"
        history_rect = game_font.render(history_text, True, light_gray)
        screen.blit(history_rect, (500, 400 + i * 30))

    pygame.display.flip()

    global opponent_mode
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    show_title_screen()
                if delete_rect.collidepoint(event.pos):
                    cursor.execute("DELETE  FROM history")
                    conn.commit()
                    print("Historie zápasů byla smazána")
                    opponent_mode = "historie"
                
#nastavení základního menu
def show_title_screen():
    screen.fill(bg_color)
    title_text = game_font.render("Ping-Pong", True, light_gray)
    menu_text = game_font.render("vs AI", True, light_gray)
    hrac_text = game_font.render("vs 2.Hráč", True, light_gray)
    database_text = game_font.render("Výsledky", True, light_gray)

    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
    menu_rect = menu_text.get_rect(center=(screen_width / 2, screen_height / 2))
    hrac_rect = hrac_text.get_rect(center=(screen_width / 2, screen_height / 1.8))
    database_rect = database_text.get_rect(center=(screen_width / 2, screen_height / 1.5))

    screen.blit(title_text, title_rect)
    screen.blit(menu_text, menu_rect)
    screen.blit(hrac_text, hrac_rect)
    screen.blit(database_text, database_rect)
    pygame.display.flip()



    #nastavení že při kliku na různé nápisy se nám objeví další menu
    global opponent_mode, game_difficulty
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    opponent_mode = "AI"
                    show_difficulty_menu()
                    waiting = False
                if hrac_rect.collidepoint(event.pos):
                    opponent_mode = "Player2"

                    waiting = False
                if database_rect.collidepoint(event.pos):
                    opponent_mode = "historie"
                    show_databse()
                    waiting = False

#nastavení samotného menu na obtížnost
def show_difficulty_menu():
    screen.fill(bg_color)
    difficulty_text = game_font.render("Výběr obtížnosti", True, light_gray)
    easy_text = game_font.render("Easy", True, light_gray)
    medium_text = game_font.render("Medium", True, light_gray)
    hard_text = game_font.render("Hard", True, light_gray)

    difficulty_rect = difficulty_text.get_rect(center=(screen_width / 2, screen_height / 3))
    easy_rect = easy_text.get_rect(center=(screen_width / 2, screen_height / 2.2))
    medium_rect = medium_text.get_rect(center=(screen_width / 2, screen_height / 2))
    hard_rect = hard_text.get_rect(center=(screen_width / 2, screen_height / 1.8))

    screen.blit(difficulty_text, difficulty_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    pygame.display.flip()


    #menu obtížností
    global game_difficulty
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    game_difficulty = "Easy"
                    set_difficulty()
                    waiting = False
                if medium_rect.collidepoint(event.pos):
                    game_difficulty = "Medium"
                    set_difficulty()
                    waiting = False
                if hard_rect.collidepoint(event.pos):
                    game_difficulty = "Hard"
                    set_difficulty()
                    waiting = False

#nastavení obtížností
def set_difficulty():
    global opponent_speed
    if game_difficulty == "Easy":
        opponent_speed = 4
    elif game_difficulty == "Medium":
        opponent_speed = 6
    elif game_difficulty == "Hard":
        opponent_speed = 10

#Jak se míček hýbe
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    # Počet kroků pro kontrolu kolize
    steps = int(max(abs(ball_speed_x), abs(ball_speed_y)))
    for step in range(steps):
        ball.x += ball_speed_x / steps
        ball.y += ball_speed_y / steps

        # Odražení míčku od stropu nebo podlahy
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        # Gól hráče
        if ball.left <= 0:
            pygame.mixer.Sound.play(score_sound)
            player_score += 1
            score_time = pygame.time.get_ticks()
            break

        # Gól opponent
        if ball.right >= screen_width:
            pygame.mixer.Sound.play(score_sound)
            opponent_score += 1
            score_time = pygame.time.get_ticks()
            break

        # Kolize míčku s hráčem a jeho odražení
        if ball.colliderect(player) and ball_speed_x > 0:
            ball_speed_x *= -1.1  # Zrychlení míčku při odražení
            ball_speed_y *= 1.1  # Zrychlení míčku při odražení
            break

        # Kolize míčku s opponentem a jeho odražení
        if ball.colliderect(opponent) and ball_speed_x < 0:
            ball_speed_x *= -1.1  # Zrychlení míčku při odražení
            ball_speed_y *= 1.1  # Zrychlení míčku při odražení
            break

# Pohyb hráče
def player_animation():
    player.y += player_speed
    #Ometení pohybu hráče na obrazovce
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
# Pohyb opponenta
def opponent_animation():
    #Pokud je soupeř AI
    if opponent_mode == "AI":
        if opponent.top < ball.y:
            opponent.top += opponent_speed
        if opponent.bottom > ball.y:
            opponent.bottom -= opponent_speed
    #Mód s 2 hráčem
    else:  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            opponent.y -= opponent_speed
        if keys[pygame.K_s]:
            opponent.y += opponent_speed
    # Omezení pohybu spoeře na obrazovce
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

# Restartování míčku po gólu
def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    #odpočítání od startu
    if current_time - score_time < 700:
        number_four = game_font.render("4", False, light_gray)
        screen.blit(number_four, (screen_width / 2 - 10, screen_height / 2 + 20))

    if 700 < current_time - score_time < 1400:
        number_three = game_font.render("3", False, light_gray)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_two = game_font.render("2", False, light_gray)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))

    if 2100 < current_time - score_time < 2800:
        number_one = game_font.render("1", False, light_gray)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2800:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

pygame.init()
clock = pygame.time.Clock()

#nastavení pozadí hry
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)


bg_color = pygame.Color("grey12")
light_gray = (200, 200, 200)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True

player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

score_sound = pygame.mixer.Sound("score.ogg")

opponent_mode = "AI"
show_title_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
                
    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_gray, player)
    pygame.draw.rect(screen, light_gray, opponent)
    pygame.draw.ellipse(screen, light_gray, ball)
    pygame.draw.aaline(screen, light_gray, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_gray)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_gray)
    screen.blit(opponent_text, (600, 470))

    pygame.display.flip()
    clock.tick(60)

    if opponent_score >= 5 or player_score >= 5:
        cursor.execute("INSERT INTO history (player_score, opponent_score) VALUES (?, ?)", (player_score, opponent_score))
        conn.commit()
        opponent_mode = None
        player_score, opponent_score = 0,0
