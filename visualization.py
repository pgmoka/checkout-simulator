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

    def __init__(self):
        pass

    def print_env(self, modelObj):
        # Pulls environment
        line = modelObj.line
        # Reference to cashiers
        cashiers = line.cashier_list
        num_cashiers = len(cashiers)

        # List of item's remaining
        item_list = modelObj.list_of_items_checked

        # Customers waiting to get into line
        cust_waiting = modelObj.list_of_customers_in_line
        cur_time_step = v.TIME_STEP * len(item_list)

        # Check for user interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Set background
        self.screen.fill(self.black)

        # Print Statistics about current timestep
        self.writeText("Current Time: " + str(cur_time_step) + " Seconds", width=int(self.displayWidth / 2), height=25)
        self.writeText("Items Left: " + str(int(item_list[-1])), width=int(self.displayWidth / 2), height=50)
        self.writeText("Customers Not in Line: " + str(int(cust_waiting[-1])), width=int(self.displayWidth / 2), height=75)

        # Print cashiers
        dist = int(self.displayWidth / (num_cashiers + 1))
        for i in range(num_cashiers):
            xPos = dist * (i + 1)
            self.print_cashier(xPos, 300, cashiers[i].self_checkout)
            self.print_line(xPos, 300, len(cashiers[i].cashier_queue))

        # Update screen
        pygame.display.flip()
        self.clock.tick(30)



    def print_cashier(self, x, y, self_checkout):
        if not self_checkout:
            pygame.draw.rect(self.screen, self.green, (x, y, 25, 25))
        else:
            pygame.draw.rect(self.screen, self.blue, (x, y, 25, 25))
        pass

    def print_line(self, x, y, num_customers=5):
        for i in range(num_customers):
            pygame.draw.rect(self.screen, self.red,
                             (x - 30, y - (50 * i), 25, 25))

    def update_customer_count(self, num_cashiers, num_customers):
        cust_per_cashier = int(num_customers / num_cashiers)
        customers_to_cashiers = [cust_per_cashier for x in range(0, num_cashiers)]
        remainder = num_customers - sum(customers_to_cashiers)
        for i in range(remainder):
            customers_to_cashiers[i] += 1
        return customers_to_cashiers

    def writeText(self, text, width=200, height=300, t_font=font, t_color=white):
        textToWrite, textRect = self.textObj(text, t_font, t_color)
        textRect.center = (width - 50, height)
        self.screen.blit(textToWrite, textRect)

    def textObj(self, text, t_font, t_color):
        textSurface = t_font.render(text, True, t_color)
        return textSurface, textSurface.get_rect()

if __name__ == '__main__':
    pass