import pygame
from pygame import display

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

    def display_simulation(self, num_cashiers=4, listCustomersLeft=None, listCustomersInLine=[x for x in range(10, -1, -1)], listItemsLeft=None):
        active = True
        curTimeStep = 0
        customers_to_cashiers = self.update_customer_count(num_cashiers, listCustomersInLine[curTimeStep])
        last_updated = pygame.time.get_ticks()

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            # Set background
            self.screen.fill(self.black)

            # Update current customers
            currentTime = (pygame.time.get_ticks() - last_updated) / 1000
            if currentTime > 1 and len(listCustomersInLine) > curTimeStep:
                customers_to_cashiers = self.update_customer_count(num_cashiers, listCustomersInLine[curTimeStep])
                curTimeStep += 1
                last_updated = pygame.time.get_ticks()

            # Print cashiers
            dist = int(self.displayWidth / (num_cashiers + 1))
            for i in range(1, num_cashiers + 1):
                xPos = dist * i
                self.print_cashier(xPos, 300)
                self.print_line(xPos, 300, customers_to_cashiers[i - 1])
            # Update screen
            pygame.display.flip()
            self.clock.tick(30)

    def print_cashier(self, x, y):
        pygame.draw.rect(self.screen, self.green, (x, y, 25, 25))
        pass

    def print_line(self, x, y, num_customers=5):
        for i in range(num_customers):
            pygame.draw.rect(self.screen, self.red,
                             (x - 30, y - (50 * i), 25, 25))

    def update_customer_count(self, num_cashiers, num_customers):
        cust_per_cashier = int(num_customers / num_cashiers)
        customers_to_cashiers = [cust_per_cashier for x in range(1, num_cashiers)]
        customers_to_cashiers.append(num_customers - sum(customers_to_cashiers))
        return customers_to_cashiers


if __name__ == '__main__':
    visual().display_simulation()