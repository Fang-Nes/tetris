import pygame, random

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')
game = 0


#функция для написания текста
def write(text, color, pos, size=75):
    font = pygame.font.Font(None, size)
    pos = list(pos)
    txt = font.render(text, False, color)
    if pos[0] == None:
        pos[0] = (400 - txt.get_width()) // 2
    screen.blit(txt, pos)


#создание и реализация фигурок
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

#начало игры
while game == 0:
    screen.fill((0, 0, 0))
    x, y = pygame.mouse.get_pos()
    text = 'PLAY'
    yep = False
    rect = (760, 440, 400, 200)
    txt_pos = (820, 490)
    bg = (255, 255, 255)
    txt_color = (0, 0, 0)
    active_bg = (180, 180, 180)
    active_txt_color = (80, 80, 80)
    size = 150
    pygame.draw.rect(screen, bg, rect)
    write(text, txt_color, txt_pos, size)
    if rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]:
        pygame.draw.rect(screen, active_bg, rect)
        write(text, active_txt_color, txt_pos, size)
        yep = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and yep:
            game = 1
    pygame.display.flip()


#сама игра
figure = random.choice(figures)
type_figure = random.randint(0, len(figure) - 1)
pos = [9, -2]
bricks = [0] * 20
for i in range(20):
    bricks[i] = [0] * 35
color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
#ставим таймер на опускание фигуры
pygame.time.set_timer(30, 600)
pause = False
score = 0
tetris_fon = pygame.image.load("tetris_fon.png")
red_pased = False
red_button1 = pygame.image.load("red_button1.png")
red_button2 = pygame.image.load("red_button2.png")


while game == 1:
    x, y = pygame.mouse.get_pos()
    #отрисовка элементов
    screen.fill((50, 215, 200))
    screen.blit(tetris_fon, (512, 0))
    if red_pased:
        screen.blit(red_button2, (620, 730))
    else:
        screen.blit(red_button1, (620, 730))
    pygame.draw.rect(screen, (0, 0, 0), (662, 79, 401, 600))
    for i in range(len(bricks)):
        for j in range(len(bricks[i])):
            if bricks[i][j] != 0:
                pygame.draw.rect(screen, bricks[i][j], (663 + i * 20, 79 + j * 20, 19, 19))

    for i in figure[type_figure]:
        if pos[1] + i[1] >= 0:
            pygame.draw.rect(screen, color, (663 + (i[0] + pos[0]) * 20, 79 + (i[1] + pos[1]) * 20, 19, 19))
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == 30 and not pause:
            pos[1] += 1
        #события на кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (((x - 651) ** 2) + ((y - 761) ** 2)) ** 0.5 <= 27:
                red_pased = True
                if pause:
                    pause = False
                else:
                    pause = True
        if event.type == pygame.MOUSEBUTTONUP:
            red_pased = False
        #все события на клавиатуру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_RIGHT and not pause:
                pos[0] += 1
                for i in figure[type_figure]:
                    if i[0] + pos[0] > 19:
                        pos[0] -= 1
                        break
                    for j in bricks:
                        if bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                            pos[0] -= 1
                            break

            #передвижение влево
            if event.key == pygame.K_LEFT and not pause:
                pos[0] -= 1
                for i in figure[type_figure]:
                    if i[0] + pos[0] < 0:
                        pos[0] += 1
                        break
                    if bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                        pos[0] += 1
                        break

            if event.key == pygame.K_DOWN:
                #при зажатии фигура ускоряет падение
                pygame.time.set_timer(30, 60)

            if event.key == pygame.K_UP and not pause:
                #разворот фигуры
                type_figure = (type_figure + 1) % len(figure)
                ret = 0
                for i in figure[type_figure]:
                    if i[0] + pos[0] < 0 or i[0] + pos[0] > 19 or i[1] + pos[1] > 29 or\
                            bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
                        ret = 1
                        break
                if ret:
                    type_figure = (type_figure - 1) % len(figure)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pygame.time.set_timer(30, 600)


    #проверка на то, легла фигура или нет
    for i in figure[type_figure]:
        if i[1] + pos[1] > 29 or bricks[i[0] + pos[0]][i[1] + pos[1]] != 0:
            for j in figure[type_figure]:
                bricks[j[0] + pos[0]][j[1] + pos[1] - 1] = color
            score += 10
            figure = random.choice(figures)
            pos = [9, -2]
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            type_figure = random.randint(0, len(figure) - 1)
            break

    #проверка и удаление заполненных слоев
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
                score += 100
                more = True
                for i1 in range(i, 0, -1):
                    for j1 in range(0, 20):
                        bricks[j1][i1] = bricks[j1][i1 - 1]
#############################
    write('score:'+str(score), (255, 255, 255), (0, 0), 25)
    for i in bricks:
        if i[0] != 0:
            game = 2
    pygame.display.flip()
for i in range(len(bricks)):
    for m in range(len(bricks[i])):
        if bricks[i][m] != 0:
            pygame.draw.rect(screen, bricks[i][m], (i * 20, m * 20, 19, 19))
write('score:' + str(score), (255, 255, 255), (None, 330))
while game == 2:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game = 0
        if event.type == pygame.QUIT:
            exit()
