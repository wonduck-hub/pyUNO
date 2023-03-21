import pygame

class PygameScreen:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # 화면을 검정색으로 채우기
            self.screen.fill((0, 0, 0))
            
            # 여기에 화면에 그리는 코드를 작성합니다.
            # 예를 들어, pygame.draw.circle(self.screen, (255, 255, 255), (self.width/2, self.height/2), 50)과 같은 코드를 사용하여 원을 그릴 수 있습니다.
            
            pygame.display.update()
        
        pygame.quit()
