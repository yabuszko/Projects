import pygame
import pygame_gui
pygame.init()

width, height = 900, 500
pygame.display.set_caption('Electrostatics by Oliwier Moskalewicz')
window_surface = pygame.display.set_mode((width, height))

background = pygame.Surface((width, height))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((width, height))

add_charge_button_p = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), 
(200, 50)), text='Add Charge (+)', manager=manager)
add_charge_button_n = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 50), 
(200, 50)), text='Add Charge (-)', manager=manager)

print_all_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 100),
(200, 50)), text='Show all data', manager=manager)

class Charge:
    def __init__(self, sign, value, rect):
        self.sign = sign
        self.value = value
        self.color = (0, 0, 0)
        self.position = (0, 0)

        self.rect = rect

        self.put = False

        if value < 0:
            self.color = (0, 0, 255)
        elif value > 0:
            self.color = (255, 0, 0)
    
    def print_data(self):
        print(f"sign: {self.sign}, value: {self.value} C")

    def permamently_place(self, surface):
        if self.put:
            pygame.draw.circle(surface, self.color, self.position, 10)

class TempCharge:
    def __init__(self, col, value, sign):
        self.color = col
        self.sign = sign
        self.value = value
    
    def follow(self, surface):
        pygame.draw.circle(surface, self.color, pygame.mouse.get_pos(), 10)

charges = []

clock = pygame.time.Clock()

def main():
    is_running = True
    charge_follow = False

    while is_running:
        delta_time = clock.tick(60)/1000.0
        window_surface.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if charge_follow:
                    charge_follow = False
                    charges.append(Charge(
                        tempcharge.sign, 
                        tempcharge.value,
                        pygame.Rect(pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20)
                        ))
                    c = charges[len(charges) - 1]
                    c.put = True
                    c.position = pygame.mouse.get_pos()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == add_charge_button_p:
                    if not charge_follow:
                        tempcharge = TempCharge((150,0,0), 1, 'positive')
                        charge_follow = True

                elif event.ui_element == add_charge_button_n:
                    if not charge_follow:
                        tempcharge = TempCharge((0,0,150), -1, 'negative')
                        charge_follow = True
                elif event.ui_element == print_all_button:
                    for c in charges:
                        c.print_data()

            manager.process_events(event)
        
        manager.update(delta_time)
        
        manager.draw_ui(window_surface)

        if charge_follow:
            tempcharge.follow(window_surface)

        for c in charges:
            c.permamently_place(window_surface)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
