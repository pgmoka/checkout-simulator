import pygame
from pygame import display
import variables as v


class visual():
    pygame.init()

    # Screen size in pixels
    displayWidth = 450
    displayHeight = 450

    # Create Screen / Display Window
    screen = display.set_mode((displayWidth, displayHeight))

    # Create clock to control frame rate
    clock = pygame.time.Clock()

    # Provide a caption for the window
    display.set_caption("CSS 458 Group - Pedro Is a Meme")

    # Colors to chose from
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 200, 0)
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    blue = (0, 0, 255)

    # Fonts to choose from
    font = pygame.font.Font(None, 32)
    smallFont = pygame.font.Font(None, 20)

    def __init__(self):
        pass

    def print_env(self, modelObj):
        # Pulls environment
        line = modelObj.line
        # Reference to cashiers
        cashiers = line.cashier_list

        # List of item's remaining
        item_list = modelObj.list_of_items_checked

        # Customers waiting to get into line
        cust_waiting = modelObj.list_of_customers_in_line
        cur_time_step = (60 / v.TIME_STEP) * len(item_list)

        active = True
        startTimer = pygame.time.get_ticks()

        while active:
            # Check for user interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            # Is longer than a second
            if (pygame.time.get_ticks() - startTimer) / 1000 > 1:
                return True
            # Set background
            self.screen.fill(self.black)

            # Print Statistics about current timestep
            self.writeText("Current Time: " + str(cur_time_step) + " Seconds", width=int(self.displayWidth / 2), height=25)
            self.writeText("Items Left: " + str(int(item_list[-1])), width=int(self.displayWidth / 2), height=50)
            self.writeText("Customers Not in Line: " + str(int(cust_waiting[-1])), width=int(self.displayWidth / 2),
                           height=75)

            # Print cashiers
            self.print_floor(cashiers)

            # Update screen
            pygame.display.flip()
            self.clock.tick(30)

    def print_floor(self, cashiers):
        num_cashiers = len(cashiers)
        dist = int(self.displayWidth / min((num_cashiers + 1), 6))
        for row in range(max(int(num_cashiers / 6 + 1), 1)):
            for column in range(min(num_cashiers - (5 * row), 5)):
                self.print_both(cashiers[column + row * 5], cashiers[column + row * 5].cashier_queue, column, row, dist)

    def print_both(self, cashier, queue, cashier_num, row, dist):
        xPos = dist * (cashier_num + 1)
        self.print_cashier(xPos, 300 + (80 * row), cashier)
        self.print_line(xPos, 300 + (80 * row), len(cashier.cashier_queue), queue)

    def print_cashier(self, x, y, cashier):
        mouse = pygame.mouse.get_pos()

        if x + 25 > mouse[0] > x and y + 25 > mouse[1] > y:
            if not cashier.self_checkout:
                pygame.draw.rect(self.screen, self.bright_green, (x, y, 25, 25))
            else:
                pygame.draw.rect(self.screen, self.bright_red, (x, y, 25, 25))
            bottom_of_screen = int(self.displayHeight * 5 / 6)
            box_width = int(self.displayWidth * 2 / 3)
            distance_from_side = int(self.displayWidth / 6)
            box_height = int(self.displayHeight / 6)
            pygame.draw.rect(self.screen, self.green,
                             (distance_from_side, bottom_of_screen,
                              box_width, box_height))

            helpedText = "Helped: " + str(0)  # Add cashier numbers
            textSurf, textRect = self.textObj(helpedText, self.smallFont, self.white)
            textRect.center = ((distance_from_side + (box_width / 2)),
                               (bottom_of_screen + ((box_height - 50) / 2)))
            self.screen.blit(textSurf, textRect)

            ipmText = "IPM: " + str(round(cashier.IPM, 2))
            textSurf, textRect = self.textObj(ipmText, self.smallFont, self.white)
            textRect.center = ((distance_from_side + (box_width / 2)),
                               (bottom_of_screen + ((box_height - 25) / 2)))
            self.screen.blit(textSurf, textRect)

            itemText = "Items: " + str(round(cashier.total_items_checked, 2))
            textSurf, textRect = self.textObj(itemText, self.smallFont, self.white)
            textRect.center = ((distance_from_side + (box_width / 2)),
                               (bottom_of_screen + (box_height / 2)))
            self.screen.blit(textSurf, textRect)

            custText = "Line: " + str(len(cashier.cashier_queue))
            textSurf, textRect = self.textObj(custText, self.smallFont, self.white)
            textRect.center = ((distance_from_side + (box_width / 2)),
                               (bottom_of_screen + ((box_height + 25) / 2)))
            self.screen.blit(textSurf, textRect)

            chitText = "Chitchat: " + str(cashier.chitchatness)
            textSurf, textRect = self.textObj(chitText, self.smallFont, self.white)
            textRect.center = ((distance_from_side + (box_width / 2)),
                               (bottom_of_screen + ((box_height + 50) / 2)))
            self.screen.blit(textSurf, textRect)
        else:
            if not cashier.self_checkout:
                pygame.draw.rect(self.screen, self.green, (x, y, 25, 25))
            else:
                pygame.draw.rect(self.screen, self.blue, (x, y, 25, 25))
        pass

    def print_line(self, x, y, num_customers=5, cashier_queue=None):
        if len(cashier_queue) > 0:
            if cashier_queue[-1].number_of_items != 0:
                transparency = int(255 * cashier_queue[-1].number_of_items / cashier_queue[-1].total_items)
            else:
                transparency = 255
            pygame.draw.rect(self.screen, (transparency, transparency, transparency),
                             (x - 30, y, 25, 25))
        if len(cashier_queue) > 1:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (x - 30, y - 50, 25, 25))
            lineText = str(len(cashier_queue) - 1)
            textSurf, textRect = self.textObj(lineText, self.smallFont, self.red)
            textRect.center = ((x - 30 + int(25 / 2)),
                               (y - 50 + int(25 / 2)))
            self.screen.blit(textSurf, textRect)

    def writeText(self, text, width=200, height=300, t_font=font, t_color=white):
        textToWrite, textRect = self.textObj(text, t_font, t_color)
        textRect.center = (width - 50, height)
        self.screen.blit(textToWrite, textRect)

    def textObj(self, text, t_font, t_color):
        textSurface = t_font.render(text, True, t_color)
        return textSurface, textSurface.get_rect()


if __name__ == '__main__':
    pass
