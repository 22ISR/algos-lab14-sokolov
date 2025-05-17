import pygame
import random
import os

# Инициализация pygame
pygame.init()

# Определение цветов (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Размеры окна
window_width = 600
window_height = 400

# Создание окна игры
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Змейка')

# Часы для контроля скорости игры
clock = pygame.time.Clock()

# Размер блока и скорость змейки
block_size = 20
snake_speed = 15

# Шрифт для отображения счета
font_style = pygame.font.SysFont(None, 30)

def show_score(score):
    """Отображение текущего счета"""
    score_text = font_style.render("Счет: " + str(score), True, white)
    game_display.blit(score_text, [10, 10])

def message(msg, color):
    """Отображение сообщения на экране"""
    rendered_message = font_style.render(msg, True, color)
    game_display.blit(rendered_message, [window_width / 6, window_height / 3])

def draw_snake(snake_list, block_size):
    """Отрисовка змейки"""
    for segment in snake_list:
        pygame.draw.rect(game_display, white, [segment[0], segment[1], block_size, block_size])

def game_loop():
    """Основной игровой цикл"""
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1 = window_width / 2
    y1 = window_height / 2

    # Изменение позиции змейки
    x1_change = 0
    y1_change = 0

    # Тело змейки (список координат)
    snake_list = []
    snake_length = 1

    # Координаты еды
    foodx = round(random.randrange(0, window_width - block_size) / 20.0) * 20.0
    foody = round(random.randrange(0, window_height - block_size) / 20.0) * 20.0

    while not game_over:
        # Экран окончания игры
        while game_close:
            game_display.fill(black)
            message("Вы проиграли! Нажмите Q-выход или C-играть снова", red)
            show_score(snake_length - 1)
            pygame.display.update()

            # Обработка нажатий клавиш на экране окончания игры
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0

        # Проверка столкновения со стенами
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        # Обновление позиции змейки
        x1 += x1_change
        y1 += y1_change
        
        # Отрисовка игрового поля
        game_display.fill(black)
        
        # Отрисовка еды
        pygame.draw.rect(game_display, green, [foodx, foody, block_size, block_size])
        
        # Добавление текущей позиции змейки в список
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        
        # Удаление лишних элементов змейки
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка на столкновение с самим собой
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Отрисовка змейки
        draw_snake(snake_list, block_size)
        
        # Отображение счета
        show_score(snake_length - 1)
        
        # Обновление экрана
        pygame.display.update()

        # Проверка на поедание еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - block_size) / 20.0) * 20.0
            foody = round(random.randrange(0, window_height - block_size) / 20.0) * 20.0
            snake_length += 1

        # Контроль скорости игры
        clock.tick(snake_speed)

    # Завершение pygame
    pygame.quit()
    quit()

game_loop()