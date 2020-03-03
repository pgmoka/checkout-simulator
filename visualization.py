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

    def display_simulation(self, num_cashiers=4, customer_left=[x for x in range(0, 10)], queue_values=[x for x in range(0, 10)], line_values=[x for x in range(10, -1, -1)], items_left=[x for x in range(10, -1, -1)]):
        active = True
        print_time = 0
        cur_time_step = 0
        total_time_ticks = len(line_values)
        customers_to_cashiers = self.update_customer_count(num_cashiers, line_values[cur_time_step] + queue_values[cur_time_step])
        last_updated = pygame.time.get_ticks()

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            # Set background
            self.screen.fill(self.black)

            # Update current customers
            current_time = (pygame.time.get_ticks() - last_updated) / 1000
            if current_time > 1 and total_time_ticks > cur_time_step:
                customers_to_cashiers = self.update_customer_count(num_cashiers, line_values[cur_time_step] + queue_values[cur_time_step])
                print_time = cur_time_step
                cur_time_step += 1
                last_updated = pygame.time.get_ticks()
            # Reset simulation when we get to the end
            elif cur_time_step >= total_time_ticks:
                cur_time_step = 0
                last_updated = pygame.time.get_ticks()
                print_time = total_time_ticks - 1

            # Print out current time
            self.writeText("Current Time: " + str(print_time) + " Minutes", width=int(self.displayWidth / 2), height=25)
            self.writeText("Items Left: " + str(int(items_left[print_time])), width=int(self.displayWidth / 2), height=50)
            self.writeText("Customers Left: " + str(customer_left[print_time]), width=int(self.displayWidth / 2), height=75)


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
    visual().display_simulation()