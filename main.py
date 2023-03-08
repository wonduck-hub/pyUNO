import pygame

pygame.init()

size = [800, 600]
screen = pygame.display.set_mode(size)

title = "pyUNO"
pygame.display.set_caption(title)

width = screen.get_width()
height = screen.get_height()

color_white = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_black = (0, 0, 0)

small_font = pygame.font.SysFont('Corbel', 35)

#rendering a text written in this font
text_start = small_font.render('start', True, color_black)
text_menu = small_font.render('menu', True, color_black)
text_quit = small_font.render('quit', True, color_black)

first_button_pos = (width // 2 - 50, height // 2 - 50)
second_button_pos = (width // 2 - 50, height // 2)
third_button_pos = (width // 2 - 50, height // 2 + 50)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if third_button_pos[0] <= mouse[0] <= third_button_pos[0] + 60 and third_button_pos[1] <= mouse[1] <= third_button_pos[1] + 40:
                #quit버튼을 눌렀을 때
                pygame.quit()

    mouse = pygame.mouse.get_pos()
    screen.fill(color_white)

    #버튼과 배경 겹치기
    #마우스 올리면 색 변경
    if width // 2 - 50 <= mouse[0] <= width // 2 + 15 and first_button_pos[1] <= mouse[1] <= height // 2:
        pygame.draw.rect(screen, color_light, first_button_pos + (65, 40))

    else:
        pygame.draw.rect(screen, color_dark, first_button_pos + (65, 40))

    if width // 2 - 50 <= mouse[0] <= width // 2 + 30 and second_button_pos[1] <= mouse[1] <= height // 2 + 40:
        pygame.draw.rect(screen, color_light, second_button_pos + (80, 40))

    else:
        pygame.draw.rect(screen, color_dark, second_button_pos + (80, 40))

    if width // 2 - 50 <= mouse[0] <= width // 2 + 10 and third_button_pos[1] <= mouse[1] <= height // 2 + 90:
        pygame.draw.rect(screen, color_light, third_button_pos + (60, 40))

    else:
        pygame.draw.rect(screen, color_dark, third_button_pos + (60, 40))

    #글 출력
    screen.blit(text_start, first_button_pos)
    screen.blit(text_menu, second_button_pos)
    screen.blit(text_quit, third_button_pos)
    pygame.display.update()