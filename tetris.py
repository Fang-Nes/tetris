import pygame, random

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')
tetris_fon = pygame.image.load("pictures/tetris_fon.png")
tick = pygame.transform.scale(pygame.image.load("pictures/tick.png"), (100, 100))
dagger = pygame.transform.scale(pygame.image.load("pictures/dagger.png"), (100, 100))
data_now = []
data = []
nick = ""
pygame.mixer.music.load('tetris.mp3')
pygame.mixer.music.play()
line = pygame.mixer.Sound('line.wav')
fall = pygame.mixer.Sound('fall.wav')
pygame.time.set_timer(31, 180000)
try:
    with open('data.txt', 'r')as f:
        for i in f.readlines():
            data.append(eval(i))
except:
    with open('data.txt','w')as f:
        pass


#функция для копирования двух(и более)мерного массива
def get_copy(mas):
    if type(mas) not in (tuple, list):
        return mas
    self = []
    for i in mas:
        self.append(get_copy(i))
    if type(self) == tuple:
        now = tuple(self)
    return self


#функция для написания текста
def write(text, color, pos, size=75):
    font = pygame.font.Font(None, size)
    pos = list(pos)
    txt = font.render(text, False, color)
    screen.blit(txt, pos)

#хранение фигурок в массиве
figures = (
    #прямая линия
    (((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0))),
    #линия с изгибом в лево
    (((0, -1), (1, -1), (0, 0), (0, 1)), ((-1, 0), (0, 0), (1, 0), (1, 1)),
     ((0, 1), (1, 1), (1, 0), (1, -1)), ((-1, 1), (0, 1), (1, 1), (-1, 0))),
    #куб
    (((0, 0), (0, 1), (1, 0), (1, 1)),),
    #горка
    (((-1, 0), (0, 0), (1, 0), (0, 1)), ((0, -1), (0, 0), (0, 1), (-1, 0)),
     ((0, 0), (-1, 1), (0, 1), (1, 1)), ((0, -1), (0, 0), (0, 1), (1, 0))),
    #кривая
    (((-1, 0), (0, 0), (0, 1), (1, 1)), ((1, -1), (1, 0), (0, 0), (0, 1)))
)


#отрисовка игры
def drawer(score, rows, next_figure, next_type, next_color, bricks, figure, type, pos, color):
    screen.fill((50, 215, 200))
    screen.blit(tetris_fon, (512, 0))
    write("SCORE:", (0, 0, 0), (1080, 120), 40)
    write(str(score), (0, 0, 0), (1120, 160), 40)
    write("ROWS:", (0, 0, 0), (1080, 220), 40)
    write(str(rows), (0, 0, 0), (1120, 260), 40)
    write("NEXT:", (0, 0, 0), (1080, 320), 40)
    pygame.draw.rect(screen, (0, 0, 0), (1120, 360, 81, 81))
    for i in next_figure[next_type]:
        pygame.draw.rect(screen, next_color, (1141 + i[0] * 20, 381 + i[1] * 20, 19, 19))
    pygame.draw.rect(screen, (0, 0, 0), (662, 79, 401, 600))
    # отрисовка уже лежащих
    for i in range(len(bricks)):
        for j in range(len(bricks[i])):
            if bricks[i][j] != 0:
                pygame.draw.rect(screen, bricks[i][j], (663 + i * 20, 79 + j * 20, 19, 19))
    # сетка
    for i in range(1, 20):
        pygame.draw.line(screen, (100, 100, 100), (662 + i * 20, 79), (662 + i * 20, 678))
    for i in range(1, 30):
        pygame.draw.line(screen, (100, 100, 100), (662, 78 + i * 20), (1062, 78 + i * 20))
    #####
    for i in figure[type]:
        if pos[1] + i[1] >= 0:
            pygame.draw.rect(screen, color, (663 + (i[0] + pos[0]) * 20, 79 + (i[1] + pos[1]) * 20, 19, 19))
    pygame.display.flip()


#сама игра
def game(data_now1):
    if len(data_now1) == 0:
        figure = random.choice(figures)
        next_figure = random.choice(figures)
        type = random.randint(0, len(figure) - 1)
        next_type = random.randint(0, len(next_figure) - 1)
        pos = [9, -2]
        bricks = [0] * 20
        for i in range(20):
            bricks[i] = [0] * 35
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        next_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        # ставим таймер на опускание фигуры
        pygame.time.set_timer(30, 600)
        score = 0
        rows = 0
    else:
        score = data_now1[0]
        rows = data_now1[1]
        next_figure = tuple(data_now1[2])
        next_type = data_now1[3]
        next_color = tuple(data_now1[4])
        bricks = data_now1[5].copy()
        figure = tuple(data_now1[6])
        type = data_now1[7]
        pos = data_now1[8].copy()
        color = tuple(data_now1[9])
        pygame.time.set_timer(data_now1[10][0], data_now1[10][1])

    while True:
        x, y = pygame.mouse.get_pos()
        # отрисовка элементов
        drawer(score, rows, next_figure, next_type, next_color, bricks, figure, type, pos, color)
        for event in pygame.event.get():
            if event.type == 31:
                pygame.mixer.music.play()
            if event.type == 30:
                pos[1] += 1
            # события на кнопки мыши
            # все события на клавиатуру
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return [score, rows, next_figure, next_type, next_color,
                            bricks, figure, type, pos, color, [30, 600], 0]
                if event.key == pygame.K_RIGHT:
                    pos[0] += 1
                    for i in figure[type]:
                        if i[0] + pos[0] > 19:
                            pos[0] -= 1
                            break
                        for j in bricks:
                            if bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                                pos[0] -= 1
                                break

                # передвижение влево
                if event.key == pygame.K_LEFT:
                    pos[0] -= 1
                    for i in figure[type]:
                        if i[0] + pos[0] < 0:
                            pos[0] += 1
                            break
                        if bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                            pos[0] += 1
                            break

                if event.key == pygame.K_DOWN:
                    # при зажатии фигура ускоряет падение
                    pygame.time.set_timer(30, 60)

                if event.key == pygame.K_UP:
                    # разворот фигуры
                    type = (type + 1) % len(figure)
                    ret = 0
                    for i in figure[type]:
                        if i[0] + pos[0] < 0 or i[0] + pos[0] > 19 or i[1] + pos[1] > 29 or \
                                        bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                            ret = 1
                            break
                    if ret:
                        type = (type - 1) % len(figure)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(30, 600)

        # проверка на то, легла фигура или нет
        for i in figure[type]:
            if i[1] + pos[1] > 29 or bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                fall.play()
                for j in figure[type]:
                    bricks[j[0] + pos[0]][j[1] + pos[1] - 1] = color
                score += 10
                figure = next_figure
                next_figure = random.choice(figures)
                pos = [9, -2]
                color = next_color
                next_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                type = next_type
                next_type = random.randint(0, len(next_figure) - 1)
                break

        # проверка и удаление заполненных слоев
        more = True
        while more:
            more = False
            for i in range(34, -1, -1):
                busy = 0
                for j in range(0, 20):
                    if bricks[j][i] != 0:
                        busy += 1
                    else:
                        break
                if busy == 20:
                    line.play()
                    score += 100
                    rows += 1
                    more = True
                    for i1 in range(i, 0, -1):
                        for j1 in range(0, 20):
                            bricks[j1][i1] = bricks[j1][i1 - 1]
        for i in bricks:
            if i[0] != 0:
                return [score, rows, next_figure, next_type, next_color,
                            bricks, figure, type, pos, color, [30, 600], 1]


def saver():
    nickname = ""
    while True:
        x, y = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (740, 400, 440, 220))
        pygame.draw.rect(screen, (0, 0, 0), (750, 430, 420, 60), 1)
        write(nickname, (0, 0, 0), (755, 440), 70)
        screen.blit(tick, (790, 510))
        screen.blit(dagger, (1010, 510))
        for event in pygame.event.get():
            if event.type == 31:
                pygame.mixer.music.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (abs(x - 840) ** 2 + abs(y - 560) ** 2) ** 0.5 <= 50:
                    return nickname
                if (abs(x - 1060) ** 2 + abs(y - 560) ** 2) ** 0.5 <= 50:
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == 8:
                    nickname = nickname[:-1]
                else:
                    l = chr(event.key)
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        l = l.upper()
                    if event.key != 304:
                        nickname += l
        pygame.display.flip()


def loader(data_now1):
    k = 0
    choosed = -1
    while True:
        x, y = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (600, 0, 720, 1080))
        if 600 < x < 1320 and y < 936 and (y - 1) // 72 < len(data):
            pygame.draw.rect(screen, (190, 190, 190), (601, 1 + (y - 1) // 72 * 72, 718, 71))
        for i in range(len(data)):
            if i + k == choosed:
                pygame.draw.rect(screen, (100, 100, 100), (601, 1 + i * 72, 718, 71))
            else:
                pygame.draw.rect(screen, (100, 100, 100), (601, 1 + i * 72, 718, 71), 1)
            write(data[i][-1], (0, 0, 0), (605, 13 + (i + k) * 72), 70)
        pygame.draw.rect(screen, (255, 255, 255), (600, 936, 720, 144))
        screen.blit(tick, (650, 960))
        screen.blit(dagger, (1140, 960))
        pygame.draw.rect(screen, (255, 0, 0), (800, 960, 300, 100))
        write("DELETE", (0, 0, 0), (810, 975), 100)
        if 800 < x < 1100 and 960 < y < 1060:
            pygame.draw.rect(screen, (100, 100, 100), (800, 960, 300, 100), 3)
        for event in pygame.event.get():
            if event.type == 31:
                pygame.mixer.music.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 600 < x < 1320 and y < 936 and (y - 1) // 72 < len(data):
                        choosed = (y - 1) // 72 + k

                    if (abs(x - 1180) ** 2 + abs(y - 1010) ** 2) ** 0.5 <= 50:
                        return data_now1.copy()
                    if 800 < x < 1100 and 960 < y < 1060 and choosed != -1:
                        del data[choosed]
                    if (abs(x - 710) ** 2 + abs(y - 1010) ** 2) ** 0.5 <= 50 and choosed != -1:
                        return data[choosed].copy()
                if event.button == 4 and k < 0:
                    k += 1
                if event.button == 5:
                    if abs(k) < len(data) - 13:
                        k -= 1
            if event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


#начальное окно
while True:
    #кнопки в началном меню
    screen.fill((0, 0, 0))
    x, y = pygame.mouse.get_pos()

    play = 0
    pygame.draw.rect(screen, (255, 255, 255), (750, 70, 420, 120))
    write("PLAY", (0, 0, 0), (870, 100), 100)
    if 750 < x < 1170 and 70 < y < 190:
        pygame.draw.rect(screen, (180, 180, 180), (750, 70, 420, 120))
        write("PLAY", (80, 80, 80), (870, 100), 100)
        play = 1

    save = 0
    pygame.draw.rect(screen, (255, 255, 255), (750, 250, 420, 120))
    write("SAVE", (0, 0, 0), (870, 280), 100)
    if 750 < x < 1170 and 250 < y < 370:
        pygame.draw.rect(screen, (180, 180, 180), (750, 250, 420, 120))
        write("SAVE", (80, 80, 80), (870, 280), 100)
        save = 1

    download = 0
    pygame.draw.rect(screen, (255, 255, 255), (750, 430, 420, 120))
    write("DOWNLOAD", (0, 0, 0), (750, 460), 100)
    if 750 < x < 1170 and 450 < y < 550:
        pygame.draw.rect(screen, (180, 180, 180), (750, 430, 420, 120))
        write("DOWNLOAD", (80, 80, 80), (750, 460), 100)
        download = 1

    ext = 0
    pygame.draw.rect(screen, (255, 255, 255), (750, 890, 420, 120))
    write("EXIT", (0, 0, 0), (870, 920), 100)
    if 750 < x < 1170 and 890 < y < 1010:
        pygame.draw.rect(screen, (180, 180, 180), (750, 890, 420, 120))
        write("EXIT", (80, 80, 80), (870, 920), 100)
        ext = 1

    for event in pygame.event.get():
        if event.type == 31:
            pygame.mixer.music.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ext:
                with open('data.txt', 'w')as f:
                    for i in data:
                        f.write(str(i) + '\n')
                exit()
            if play:
                data_now = game(get_copy(data_now))
                if data_now[11] == 1:
                    ##################

                    #ДОБАВИТЬ ДОБАВЛЕНИЕ В ТОП ЛИСТ!!!!

                    ##################
                    data_now = []
            if save and len(data_now) != 0:
                nick = saver()
                if nick != "":
                    data_now.append(nick)
                    data.append(get_copy(data_now))
            if download:
                data_now = loader(get_copy(data_now))
    pygame.display.flip()
