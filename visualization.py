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

    def print_env(self, modelObj, update_time=1000):
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
            if (pygame.time.get_ticks() - startTimer) > update_time:
                return True
            # Set background
            self.screen.fill(self.black)

            # Print Statistics about current timestep
            self.text_box(str(cur_time_step) + " Seconds",
                          int(self.displayWidth / 4), 0, width=int(self.displayWidth / 2), height=25)
            self.text_box("Customers Not in Line: " + str(int(cust_waiting[-1])),
                          int(self.displayWidth / 4), 30, width=int(self.displayWidth / 2), height=25)

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
                if row * 5 + column < 19:
                    self.print_both(cashiers[column + row * 5], cashiers[column + row * 5].cashier_queue, column, row, dist)
                else:
                    self.print_final_cashier(dist * (column + 1),
                                             self.displayHeight / 3 + (80 * row),
                                             sum([1 for x in range(15, len(cashiers)) if not cashiers[x].self_checkout]),
                                             sum([1 for x in range(15, len(cashiers)) if cashiers[x].self_checkout]),
                                             sum([len(cashiers[x].cashier_queue) for x in range(15, len(cashiers))]))
                    return


    def print_both(self, cashier, queue, cashier_num, row, dist):
        xPos = dist * (cashier_num + 1)
        height = self.displayHeight / 3
        self.print_cashier(xPos, height + (80 * row), cashier)
        self.print_line(xPos, height + (80 * row), len(cashier.cashier_queue), queue)

    def print_cashier(self, x, y, cashier):
        mouse = pygame.mouse.get_pos()

        if x + 25 > mouse[0] > x and y + 25 > mouse[1] > y:
            if not cashier.self_checkout:
                pygame.draw.rect(self.screen, self.bright_green, (x, y, 25, 25))
            else:
                pygame.draw.rect(self.screen, self.bright_red, (x, y, 25, 25))

            helpedText = "Helped: " + str(0)  # Add cashier numbers
            self.text_box(helpedText, int(self.displayWidth / 6), 60, width=int(self.displayWidth / 6), height=25)

            ipmText = "IPM: " + str(round(cashier.IPM, 2))
            self.text_box(ipmText, int(self.displayWidth / 3), 60, width=int(self.displayWidth / 6), height=25)

            itemText = "Items: " + str(round(cashier.total_items_checked, 2))
            self.text_box(itemText, int(self.displayWidth / 2), 60, width=int(self.displayWidth / 6), height=25)

            custText = "Line: " + str(len(cashier.cashier_queue))
            self.text_box(custText, int(self.displayWidth * 2 / 3), 60, width=int(self.displayWidth / 6), height=25)

            chitText = "Chitchat: " + str(cashier.chitchatness)
            self.text_box(chitText, int(self.displayWidth / 3), 90, width=int(self.displayWidth / 6), height=25)

            self.text_box("", int(self.displayWidth / 2), 90, width=int(self.displayWidth / 6), height=25)
        else:
            if not cashier.self_checkout:
                pygame.draw.rect(self.screen, self.green, (x, y, 25, 25))
            else:
                pygame.draw.rect(self.screen, self.blue, (x, y, 25, 25))
        pass

    def print_final_cashier(self, x, y, num_cashiers, num_checkouts, num_custs):
        mouse = pygame.mouse.get_pos()

        if x + 25 > mouse[0] > x and y + 25 > mouse[1] > y:
            self.text_box(str(num_cashiers + num_checkouts), x, y, 25, 25)

            helpedText = "Cashiers: " + str(num_cashiers)  # Add cashier numbers
            self.text_box(helpedText, int(self.displayWidth / 6), 60, width=int(self.displayWidth / 3), height=25)

            ipmText = "Self Checkouts: " + str(num_checkouts)
            self.text_box(ipmText, int(self.displayWidth / 2), 60, width=int(self.displayWidth / 3), height=25)

            itemText = "Customers: " + str(num_custs)
            self.text_box(itemText, int(self.displayWidth / 3), 90, width=int(self.displayWidth / 3), height=25)
        else:
            self.text_box(str(num_cashiers + num_checkouts), x, y, 25, 25)
        pass


    def print_line(self, x, y, num_customers=5, cashier_queue=None):
        mouse = pygame.mouse.get_pos()

        if x - 5 > mouse[0] > x - 30 and y + 25 > mouse[1] > y:
            if len(cashier_queue) > 0:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (x - 30, y, 25, 25))

                itemsText = "Items Left: " + str(round(cashier_queue[0].number_of_items, 2))  # Add cashier numbers
                self.text_box(itemsText, int(self.displayWidth / 3), 60, width=int(self.displayWidth / 3), height=25)
        elif len(cashier_queue) > 0:
            if cashier_queue[-1].number_of_items != 0:
                transparency = int(255 * cashier_queue[-1].number_of_items / cashier_queue[-1].total_items)
            else:
                transparency = 255
            pygame.draw.rect(self.screen, (transparency, transparency, transparency),
                             (x - 30, y, 25, 25))
        if len(cashier_queue) > 1:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (x - 30, y - 30, 25, 25))
            lineText = str(len(cashier_queue) - 1)
            textSurf, textRect = self.textObj(lineText, self.smallFont, self.red)
            textRect.center = ((x - 30 + int(25 / 2)),
                               (y - 30 + int(25 / 2)))
            self.screen.blit(textSurf, textRect)

    def textObj(self, text, t_font, t_color):
        textSurface = t_font.render(text, True, t_color)
        return textSurface, textSurface.get_rect()

    def text_box(self, text, x, y, width, height):
        pygame.draw.rect(self.screen, self.green,
                         (x, y,
                          width, height))
        textSurf, textRect = self.textObj(text, self.smallFont, self.white)
        textRect.center = ((x + (width / 2)),
                           (y + ((height) / 2)))
        self.screen.blit(textSurf, textRect)


if __name__ == '__main__':
    pass
