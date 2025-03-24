import pygame, sys, random, sqlite3, math

# Připojení k databázi SQLite
conn = sqlite3.connect("game_history.db")
cursor = conn.cursor()

# Vytvoření tabulky pro ukládání historie her (pokud neexistuje)
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_score INTEGER,
    opponent_score INTEGER
)""")
conn.commit()


# Funkce pro zobrazení hlavního menu
def show_title_screen():
    screen.fill(bg_color) # Vyplnění obrazovky pozadím
    title_text = game_font.render("Ping-Pong", True, light_gray) # Vytvoření textu pro název hry
    menu_text = game_font.render("vs AI", True, light_gray) # Vytvoření textu pro režim hry "vs AI"
    hrac_text = game_font.render("vs 2.Hráč", True, light_gray) # Vytvoření textu pro režim hry "vs 2.Hráč"
    database_text = game_font.render("Výsledky", True, light_gray) # Vytvoření textu pro zobrazení výsledků

    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3)) # Pozice textu "Ping-Pong"
    menu_rect = menu_text.get_rect(center=(screen_width / 2, screen_height / 2)) # Pozice textu "vs AI"
    hrac_rect = hrac_text.get_rect(center=(screen_width / 2, screen_height / 1.8)) # Pozice textu "vs 2.Hráč"
    database_rect = database_text.get_rect(center=(screen_width / 2, screen_height / 1.5)) # Pozice textu "Výsledky"

    screen.blit(title_text, title_rect) # Vykreslení textu "Ping-Pong"
    screen.blit(menu_text, menu_rect) # Vykreslení textu "vs AI"
    screen.blit(hrac_text, hrac_rect) # Vykreslení textu "vs 2.Hráč"
    screen.blit(database_text, database_rect) # Vykreslení textu "Výsledky"
    pygame.display.flip() # Aktualizace obrazovky

    # Zpracování událostí pro výběr režimu hry v hlavním menu
    global opponent_mode, game_difficulty
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos): # Pokud klikneme na "vs AI"
                    opponent_mode = "AI" # Nastavení režimu hry na "vs AI"
                    show_difficulty_menu() # Zobrazení menu pro výběr obtížnosti
                    waiting = False
                if hrac_rect.collidepoint(event.pos): # Pokud klikneme na "vs 2.Hráč"
                    opponent_mode = "Player2" # Nastavení režimu hry na "vs 2.Hráč"
                    waiting = False
                if database_rect.collidepoint(event.pos): # Pokud klikneme na "Výsledky"
                    opponent_mode = "historie" # Nastavení režimu hry na "historie"
                    show_databse() # Zobrazení historie výsledků
                    waiting = False
# Funkce pro zobrazení databáze (historie výsledků)
def show_databse():
    screen.fill(bg_color) # Vyplnění obrazovky pozadím
    history_text = game_font.render("Historie výsledků", True, light_gray) # Vytvoření textu pro název
    back_text = game_font.render("Zpět do hlavního menu", True, light_gray) # Vytvoření textu pro tlačítko "Zpět"
    delete_text = game_font.render("Vymazat historii", True, light_gray) # Vytvoření textu pro tlačítko "Vymazat"

    history_rect = history_text.get_rect(center=(screen_width / 2, screen_height / 3)) # Pozice textu "Historie výsledků"
    back_rect = back_text.get_rect(center=(screen_width / 2, screen_height / 1.5)) # Pozice textu "Zpět"
    delete_rect = delete_text.get_rect(center=(screen_width / 2, screen_height / 1.3)) # Pozice textu "Vymazat"

    screen.blit(history_text, history_rect) # Vykreslení textu "Historie výsledků"
    screen.blit(back_text, back_rect) # Vykreslení textu "Zpět"
    screen.blit(delete_text, delete_rect) # Vykreslení textu "Vymazat"
    pygame.display.flip() # Aktualizace obrazovky

    # Načtení a zobrazení posledních 5 výsledků z databáze
    cursor.execute("SELECT player_score, opponent_score FROM history ORDER BY id DESC LIMIT 5")
    history = cursor.fetchall() # Načtení výsledků z databáze
    for i, (player_score, opponent_score) in enumerate(history):
        history_text = f"Hráč: {player_score} - CPU: {opponent_score}" # Formátování textu pro zobrazení výsledků
        history_rect = game_font.render(history_text, True, light_gray) # Vytvoření textu pro zobrazení výsledků
        screen.blit(history_rect, (500, 400 + i * 30)) # Vykreslení textu s výsledky

    pygame.display.flip() # Aktualizace obrazovky

    # Zpracování událostí pro navigaci v menu databáze
    global opponent_mode
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos): # Pokud klikneme na "Zpět"
                    waiting = False
                    show_title_screen() # Zobrazení hlavního menu
                if delete_rect.collidepoint(event.pos): # Pokud klikneme na "Vymazat"
                    cursor.execute("DELETE FROM history") # Vymazání historie z databáze
                    conn.commit() # Uložení změn do databáze
                    print("Historie zápasů byla smazána") # Výpis potvrzení do konzole
                    opponent_mode = "historie" # Nastavení režimu hry

# Funkce pro zobrazení menu výběru obtížnosti AI
def show_difficulty_menu():
    screen.fill(bg_color) # Vyplnění obrazovky pozadím
    difficulty_text = game_font.render("Výběr obtížnosti", True, light_gray) # Vytvoření textu pro název menu
    easy_text = game_font.render("Easy", True, light_gray) # Vytvoření textu pro obtížnost "Easy"
    medium_text = game_font.render("Medium", True, light_gray) # Vytvoření textu pro obtížnost "Medium"
    hard_text = game_font.render("Hard", True, light_gray) # Vytvoření textu pro obtížnost "Hard"
    back_text = game_font.render("Zpět do hlavního menu", True, light_gray) # Vytvoření textu pro tlačítko "Zpět"

    difficulty_rect = difficulty_text.get_rect(center=(screen_width / 2, screen_height / 3)) # Pozice textu "Výběr obtížnosti"
    easy_rect = easy_text.get_rect(center=(screen_width / 2, screen_height / 2.2)) # Pozice textu "Easy"
    medium_rect = medium_text.get_rect(center=(screen_width / 2, screen_height / 2))
    hard_rect = hard_text.get_rect(center=(screen_width / 2, screen_height / 1.8)) # Pozice textu "Hard"
    back_rect = back_text.get_rect(center=(screen_width / 2, screen_height / 1.5)) # Pozice textu "Zpět"

    screen.blit(difficulty_text, difficulty_rect) # Vykreslení textu "Výběr obtížnosti"
    screen.blit(easy_text, easy_rect) # Vykreslení textu "Easy"
    screen.blit(medium_text, medium_rect) # Vykreslení textu "Medium"
    screen.blit(hard_text, hard_rect) # Vykreslení textu "Hard"
    screen.blit(back_text, back_rect) # Vykreslení textu "Zpět"
    pygame.display.flip() # Aktualizace obrazovky

    # Zpracování událostí pro výběr obtížnosti AI
    global game_difficulty
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos): # Pokud klikneme na "Easy"
                    game_difficulty = "Easy" # Nastavení obtížnosti na "Easy"
                    set_difficulty() # Nastavení rychlosti AI podle obtížnosti
                    waiting = False # Ukončení čekání na události
                if medium_rect.collidepoint(event.pos): # Pokud klikneme na "Medium"
                    game_difficulty = "Medium" # Nastavení obtížnosti na "Medium"
                    set_difficulty() # Nastavení rychlosti AI podle obtížnosti
                    waiting = False # Ukončení čekání na události
                if hard_rect.collidepoint(event.pos): # Pokud klikneme na "Hard"
                    game_difficulty = "Hard" # Nastavení obtížnosti na "Hard"
                    set_difficulty() # Nastavení rychlosti AI podle obtížnosti
                    waiting = False # Ukončení čekání na události
                if back_rect.collidepoint(event.pos): # Pokud klikneme na "Zpět"
                    show_title_screen() # Zobrazení hlavního menu
                    waiting = False


# Funkce pro nastavení obtížnosti AI
def set_difficulty():
    global opponent_speed
    if game_difficulty == "Easy": # Pokud je obtížnost "Easy"
        opponent_speed = 4 # Nastavení rychlosti AI na 4
    elif game_difficulty == "Medium": # Pokud je obtížnost "Medium"
        opponent_speed = 6 # Nastavení rychlosti AI na 6
    elif game_difficulty == "Hard": # Pokud je obtížnost "Hard"
        opponent_speed = 15 # Nastavení rychlosti AI na 15

# Funkce pro animaci míčku
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, prekazka_x, prekazka_y, ball_angle, ball_image, power_up, power_up_type, power_up_active

    ball.x += ball_speed_x # Pohyb míčku po ose X
    ball.y += ball_speed_y # Pohyb míčku po ose Y

    # Odrážení míčku od horní a dolní stěny
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1 # Změna směru míčku po ose Y

    # Detekce gólů
    if ball.left <= 0: # Pokud míček opustí levou stranu obrazovky
        pygame.mixer.Sound.play(score_sound) # Přehrání zvuku gólu
        player_score += 1 # Zvýšení skóre hráče
        score_time = pygame.time.get_ticks() # Uložení času gólu
        prekazka.x = screen_width / 2 - 5 # Reset pozice překážky
        prekazka.y = screen_height / 1 - 70
        ball_restart() # Restart míčku
        

    if ball.right >= screen_width: # Pokud míček opustí pravou stranu obrazovky
        pygame.mixer.Sound.play(score_sound) # Přehrání zvuku gólu
        opponent_score += 1 # Zvýšení skóre soupeře
        score_time = pygame.time.get_ticks() # Uložení času gólu
        prekazka.x = screen_width / 2 - 5 # Reset pozice překážky
        prekazka.y = screen_height / 1 - 70
        ball_restart() # Restart míčku

    # Kolize míčku s hráčem a jeho odražení
    if ball.colliderect(player) and ball_speed_x > 0:
        ball_speed_x *= -1.1 # Změna směru a rychlosti míčku po ose X
        ball_speed_y *= 1.1 # Změna rychlosti míčku po ose Y

    # Kolize míčku se soupeřem a jeho odražení
    if ball.colliderect(opponent) and ball_speed_x < 0:
        ball_speed_x *= -1.1 # Změna směru a rychlosti míčku po ose X
        ball_speed_y *= 1.1 # Změna rychlosti míčku po ose Y

    # Kolize míčku s překážkou a jeho odražení
    if ball.colliderect(prekazka):
        ball_speed_x *= -1.1 # Změna směru a rychlosti míčku po ose X
        ball_speed_y *= 1.1 # Změna rychlosti míčku po ose Y

    # Kolize míčku s power-upem
    if power_up and ball.colliderect(power_up):
        power_up_active = True # Aktivace power-upu
        if power_up_type == "size": # Pokud je typ power-upu "size"
            player.height *= 1.5 # Zvětšení výšky pálky hráče
        elif power_up_type == "speed": # Pokud je typ power-upu "speed"
            ball_speed_x *= 1.5 # Zrychlení míčku po ose X
            ball_speed_y *= 1.5 # Zrychlení míčku po ose Y
        power_up = None # Odstranění power-upu z obrazovky

    ball_angle += 5 # Zvýšení úhlu rotace míčku
    rotated_ball = pygame.transform.rotate(ball_image, ball_angle) # Rotace míčku
    screen.blit(rotated_ball, ball.topleft) # Vykreslení rotovaného míčku

# Funkce pro pohyb hráče
def player_animation():
    player.y += player_speed # Pohyb hráče po ose Y
    # Omezení pohybu hráče na obrazovce
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

# Funkce pro pohyb soupeře
def opponent_animation():
    # Pokud je soupeř AI
    if opponent_mode == "AI":
        if opponent.top < ball.y: # Pokud je soupeř nad míčkem
            opponent.top += opponent_speed # Pohyb soupeře dolů
        if opponent.bottom > ball.y: # Pokud je soupeř pod míčkem
            opponent.bottom -= opponent_speed # Pohyb soupeře nahoru
    # Mód s 2 hráči
    else:
        keys = pygame.key.get_pressed() # Získání stisknutých kláves
        if keys[pygame.K_w]: # Pokud je stisknuta klávesa "w"
            opponent.y -= opponent_speed # Pohyb soupeře nahoru
        if keys[pygame.K_s]: # Pokud je stisknuta klávesa "s"
            opponent.y += opponent_speed # Pohyb soupeře dolů
    # Omezení pohybu soupeře na obrazovce
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

# Funkce pro animaci překážky
def prekazka_animace():
    global prekazka_speed

    prekazka.y += prekazka_speed # Pohyb překážky po ose Y

    # Kontrola hranic, aby překážka zůstala v herní ploše
    if prekazka.top <= 0:
        prekazka.top = 0 # Zajistí, že překážka nepřesáhne horní hranici
        prekazka_speed *= -1 # Obrátí směr pohybu

    if prekazka.bottom >= screen_height:
        prekazka.bottom = screen_height # Zajistí, že překážka nepřesáhne spodní hranici
        prekazka_speed *= -1 # Obrátí směr pohybu

# Funkce pro restart míčku po gólu
def ball_restart():
    global ball_speed_x, ball_speed_y, score_time, prekazka_speed

    current_time = pygame.time.get_ticks() # Získání aktuálního času
    ball.center = (screen_width / 2, screen_height / 2) # Nastavení míčku na střed obrazovky

    # Odpočítávání od startu
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

    # Kontrola toho aby míček opravdu vyletěl až bude 0
    if current_time - score_time < 2800:
        ball_speed_x, ball_speed_y, prekazka_speed = 0, 0, 0
    # Vypuštění míčku do hry po odbytí 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        prekazka_speed = 7

        score_time = None

pygame.init() # Inicializace Pygame
clock = pygame.time.Clock() # Vytvoření objektu Clock pro řízení FPS

# Nastavení obrazovky
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong") # Nastavení titulku okna

# Vytvoření herních objektů
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30) # Míček
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140) # Hráč
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140) # Soupeř
prekazka = pygame.Rect(screen_width / 2 - 5, screen_height / 1 - 70, 10, 180) # Překážka

# Nastavení barev
bg_color = pygame.Color("grey12") # Barva pozadí
light_gray = (200, 200, 200) # Světle šedá barva

# Nastavení rychlostí a směru
ball_speed_x = 7 * random.choice((1, -1)) # Rychlost míčku po ose X
ball_speed_y = 7 * random.choice((1, -1)) # Rychlost míčku po ose Y
player_speed = 0 # Rychlost hráče
opponent_speed = 10 # Rychlost soupeře
prekazka_speed = 12 # Rychlost překážky
ball_moving = False # Stav míčku
score_time = True # Stav odpočítávání po gólu
ball_angle = 0 # Úhel rotace míčku
ball_image = pygame.Surface((30, 30)) # Obrázek míčku
ball_image.fill(light_gray) # Vyplnění obrázku míčku barvou

# Nastavení skóre a písma
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Načtení zvuků
score_sound = pygame.mixer.Sound("score.ogg") # Zvuk gólu

# Nastavení režimu hry
opponent_mode = "AI" # Výchozí režim je proti AI

# Proměnné pro power-upy
power_up = None # Power-up objekt
power_up_type = None # Typ power-upu
power_up_active = False # Stav power-upu
power_up_timer = 0 # Časovač pro power-upy

# Barvy pro power-upy
power_up_colors = {
    "size": (0, 255, 0),  # Zelená pro zvětšení pálky
    "speed": (255, 0, 0) # Červená pro zrychlení míčku
}

# Zobrazení hlavního menu
show_title_screen()

# Hlavní herní smyčka
while True:
    for event in pygame.event.get(): # Zpracování událostí
        if event.type == pygame.QUIT: # Pokud hráč zavře okno
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: # Pokud je stisknuta klávesa
            if event.key == pygame.K_DOWN: # Klávesa "šipka dolů"
                player_speed += 7 # Zvýšení rychlosti hráče
            if event.key == pygame.K_UP: # Klávesa "šipka nahoru"
                player_speed -= 7 # Snížení rychlosti hráče
        if event.type == pygame.KEYUP: # Pokud je klávesa uvolněna
            if event.key == pygame.K_DOWN: # Klávesa "šipka dolů"
                player_speed -= 7 # Snížení rychlosti hráče
            if event.key == pygame.K_UP: # Klávesa "šipka nahoru"
                player_speed += 7 # Zvýšení rychlosti hráče

    ball_animation() # Animace míčku
    player_animation() # Animace hráče
    opponent_animation() # Animace soupeře
    prekazka_animace() # Animace překážky

    screen.fill(bg_color) # Vykreslení pozadí
    pygame.draw.rect(screen, light_gray, player) # Vykreslení hráče
    pygame.draw.rect(screen, light_gray, opponent) # Vykreslení soupeře
    pygame.draw.rect(screen, light_gray, prekazka) # Vykreslení překážky
    pygame.draw.ellipse(screen, light_gray, ball) # Vykreslení míčku
    pygame.draw.aaline(screen, light_gray, (screen_width / 2, 0), (screen_width / 2, screen_height)) # Vykreslení čáry uprostřed

    if score_time: # Pokud je odpočítávání po gólu aktivní
        ball_restart() # Restart míčku

    player_text = game_font.render(f"{player_score}", False, light_gray) # Vytvoření textu skóre hráče
    screen.blit(player_text, (660, 470)) # Vykreslení skóre hráče

    opponent_text = game_font.render(f"{opponent_score}", False, light_gray) # Vytvoření textu skóre soupeře
    screen.blit(opponent_text, (600, 470)) # Vykreslení skóre soupeře

    # Generování power-upu
    if random.random() < 0.001 and not power_up:  # 0.5% šance na generování power-upu
        power_up = pygame.Rect(random.randint(100, screen_width - 100), random.randint(100, screen_height - 100), 40, 40)
        power_up_type = random.choice(["size", "speed"])

    # Vykreslení power-upu
    if power_up:
        pygame.draw.rect(screen, power_up_colors[power_up_type], power_up)

    # Deaktivace power-upu po určitém čase
    if power_up_active:
        power_up_timer += 1
        if power_up_timer > 500:  # 500 snímků = cca 8 sekund
            power_up_active = False
            player.height = 140 
            ball_speed_x /= 1.5 #Zrychlení míčku 1,5krát
            ball_speed_y /= 1.5 #Zrychlení míčku 1,5krát
            power_up_timer = 0

    pygame.display.flip() # Aktualizace obrazovky
    clock.tick(60) # Omezení FPS na 60

    # Nastavení ukládání výsledků do databáze
    if opponent_score >= 5 or player_score >= 5:
        cursor.execute("INSERT INTO history (player_score, opponent_score) VALUES (?, ?)", (player_score, opponent_score))
        conn.commit()
        opponent_mode = None
        player_score, opponent_score = 0,0

        show_title_screen()