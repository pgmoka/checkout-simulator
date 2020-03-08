import pygame
from pygame import display
import variables as v
from datetime import timedelta


# TODO Start time


# Class to preform animation logic via pygame
class visual():
    # Initialize pygame module
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

    # List of colors to pull from as needed
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 200, 0)
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    blue = (0, 0, 255)

    # Fonts to choose from
    font = pygame.font.Font(None, 32)
    smallFont = pygame.font.Font(None, 20)  # Used inside text boxes

    # Ignore
    def __init__(self):
        pass

    def print_env(self, modelObj, update_time=1, start_time=None):
        """
        Visualizes a set of data stored inside a model object for the time
            specified in update_time.

        :param modelObj: The current state of the model to visualize.
        :param update_time: The time to display the visualization for.
            This number is in milliseconds, so 1000 ms = 1 second.
        :return: Prints an environment that shows both the cashiers and customers,
            and allows the user to determine statistics about the cashier or customer
            by hovering over them with the mouse.
        """

        # Pulls environment
        line = modelObj.line
        # Reference to cashiers
        cashiers = line.cashier_list

        # List of item's remaining
        item_list = modelObj.list_of_items_checked

        # Customers waiting to get into line
        cust_waiting = modelObj.list_of_customers_in_line

        # Model is updated by this many seconds each iteration
        cur_time_step = (60 / v.TIME_STEP) * len(item_list)

        start_hour = None
        if start_time is not None:
            start_hour = timedelta(seconds=(start_time * 3600))

        # Tells the loop to keep displaying until a certain condition is met
        active = True

        # Record when we this visualization
        startTimer = pygame.time.get_ticks()

        # Main logic
        while active:
            # Check for user interaction
            for event in pygame.event.get():
                # If the user exits out of the animation window
                if event.type == pygame.QUIT:
                    # Return false so the model doesn't keep making
                    # the window reappear
                    return False

            # Has this model been going for longer than the time in update_time?
            if (pygame.time.get_ticks() - startTimer) > (update_time * 1000):
                # The user didn't intervene, tell model
                # to keep showing the animation
                return True

            # Set background
            self.screen.fill(self.black)

            # Print Statistics about current timestep inside

            if start_time is None:
                # a text box at the top of the screen
                self.text_box(str(cur_time_step) + " Seconds",
                              int(self.displayWidth / 4), 0, width=int(self.displayWidth / 2), height=25)
            else:
                self.text_box(str(start_hour + timedelta(seconds=cur_time_step))[:-3],
                              int(self.displayWidth / 4), 0, width=int(self.displayWidth / 2), height=25)

            # Print the customers waiting to go into line
            self.text_box("Customers Not in Line: " + str(int(cust_waiting[-1])),
                          int(self.displayWidth / 4), 30, width=int(self.displayWidth / 2), height=25)

            # Print cashiers
            self.print_floor(cashiers)

            # Update screen
            pygame.display.flip()
            self.clock.tick(30)

    def print_floor(self, cashiers):
        """
        Takes in the list of all the current cashiers and displays them on the screen

        :param cashiers: A list of all the cashiers from our model object
        :return: The animation will now display all the cashiers correctly
        """
        # Store the total number of cashiers for readability
        num_cashiers = len(cashiers)

        # Determine how much room we need to divide the screen equally
        dist = int(self.displayWidth / min((num_cashiers + 1), 6))

        # Print up to three rows
        for row in range(max(int(num_cashiers / 6 + 1), 1)):
            # Print up to five cashiers
            for column in range(min(num_cashiers - (5 * row), 5)):
                # To make the data readable, we will only show the first 20 cashiers.
                if row * 5 + column < 19:
                    # Print a cashier and it's customers
                    self.print_both(cashiers[column + row * 5], cashiers[column + row * 5].cashier_queue, column, row, dist)
                # Print the rest of the cashiers inside a single box with a number representing them
                else:
                    # Show the rest of the cashiers as a single text box
                    self.print_final_cashier(dist * (column + 1),
                                             self.displayHeight / 3 + (80 * row),
                                             sum([1 for x in range(15, len(cashiers)) if not cashiers[x].self_checkout]),
                                             sum([1 for x in range(15, len(cashiers)) if cashiers[x].self_checkout]),
                                             sum([len(cashiers[x].cashier_queue) for x in range(15, len(cashiers))]))
                    # We don't need to print any other cashiers
                    return

    def print_both(self, cashier, queue, cashier_num, row, dist):
        """
        Print a single cashier and their customers

        :param cashier: A cashier object
        :param queue: The list of customers attached to a cashier object
        :param cashier_num: This correlates to the column number of the cashier; It is
            used to find the the x value
        :param row: Which row the cashier is on; This is used to find the y value
        :param dist: The distance between each cashier on the x-axis
        :return: A cashier is visualized on the screen with their current line. As well,
            the user can interact with them by hovering over them
        """

        # Where to print the cashier on the x axis
        xPos = dist * (cashier_num + 1)

        # The initial height of the cashier on the screen
        height = self.displayHeight / 3

        # Print the cashier object
        self.print_cashier(xPos, height + (80 * row), cashier)

        # Print the cashier's line
        self.print_line(xPos, height + (80 * row), queue)

    def print_cashier(self, x, y, cashier):
        """
        Print a single cashier object

        :param x: The x coordinate of the cashier on the screen
        :param y: The y coordinate of the cashier on the screen
        :param cashier: The cashier object to print
        :return: Prints a visual box to represent a cashier. Upon hovering
            over it, statistics about that specific cashier will appear
        """

        # Check the mouse's position
        mouse = pygame.mouse.get_pos()

        # Is the mouse over the box's position?
        if x + 25 > mouse[0] > x and y + 25 > mouse[1] > y:
            # Print a bright version of the cashier object
            if not cashier.self_checkout:
                # Print a highlighted regular cashier
                pygame.draw.rect(self.screen, self.bright_green, (x, y, 25, 25))
            else:
                # Print a highlighted self checkout
                pygame.draw.rect(self.screen, self.bright_red, (x, y, 25, 25))

            # Print statistics about the cashier at the top of the screen

            # Number of customers helped
            helpedText = "Helped: " + str(cashier.helped)
            self.text_box(helpedText, int(self.displayWidth / 6), 60, width=int(self.displayWidth / 6), height=25)

            # Cashiers Items Per Minute
            ipmText = "IPM: " + str(round(cashier.IPM, 2))
            self.text_box(ipmText, int(self.displayWidth / 3), 60, width=int(self.displayWidth / 6), height=25)

            # Total items checked out by this cashier
            itemText = "Items: " + str(round(cashier.total_items_checked, 2))
            self.text_box(itemText, int(self.displayWidth / 2), 60, width=int(self.displayWidth / 6), height=25)

            # Number of people in the cashier's line including the current person being helped
            custText = "Line: " + str(len(cashier.cashier_queue))
            self.text_box(custText, int(self.displayWidth * 2 / 3), 60, width=int(self.displayWidth / 6), height=25)

            # Cashier's chitchat levels
            chitText = "Chitchat: " + str(cashier.chatLevel)
            self.text_box(chitText, int(self.displayWidth / 3), 90, width=int(self.displayWidth / 6), height=25)

            # Empty box to make it look uniform
            self.text_box("", int(self.displayWidth / 2), 90, width=int(self.displayWidth / 6), height=25)
        # Mouse if not hovering over cashier
        else:
            # Print cashier object
            if not cashier.self_checkout:
                # Print normal cashier object
                pygame.draw.rect(self.screen, self.green, (x, y, 25, 25))
            else:
                # Print self checkout object
                pygame.draw.rect(self.screen, self.blue, (x, y, 25, 25))
        pass

    def print_final_cashier(self, x, y, num_cashiers, num_checkouts, num_custs):
        """
        A final block to hold the unshown cashiers and self-checkouts

        :param x: The x-position of the block
        :param y: The y-position of the block
        :param num_cashiers: Total number of regular cashiers
        :param num_checkouts: Total number of self-checkouts
        :param num_custs: Total number of customers inside the cashiers' and
            self checkouts' lines
        :return: Print a box at the specified coordinates that will tell the
            user about the number of cashiers, self checkouts, and customer's being
            helped when the user hovers over it.
        """

        # Get the mouse's position
        mouse = pygame.mouse.get_pos()

        # Is the mouse within the box's position
        if x + 25 > mouse[0] > x and y + 25 > mouse[1] > y:
            # Make a text box with the total number of cashiers and self checkouts
            self.text_box(str(num_cashiers + num_checkouts), x, y, 25, 25)

            # Display statistics about the remaining cashiers

            # Show the total number of normal cashiers
            helpedText = "Cashiers: " + str(num_cashiers)
            self.text_box(helpedText, int(self.displayWidth / 6), 60, width=int(self.displayWidth / 3), height=25)

            # Show the total number of self checkouts
            ipmText = "Self Checkouts: " + str(num_checkouts)
            self.text_box(ipmText, int(self.displayWidth / 2), 60, width=int(self.displayWidth / 3), height=25)

            # Show the total customers inside lines that are not shown
            itemText = "Customers: " + str(num_custs)
            self.text_box(itemText, int(self.displayWidth / 3), 90, width=int(self.displayWidth / 3), height=25)
        # The user isn't hovering over this box
        else:
            # Show a regular text box with details of how many cashiers and checkouts there are
            self.text_box(str(num_cashiers + num_checkouts), x, y, 25, 25)
        pass

    def print_line(self, x, y, cashier_queue=None):
        """
        Prints the customer's in line for the cashier

        :param x: The starting x coordinate to print the customer's at
        :param y: The starting y coordinate to print the customer's at
        :param cashier_queue: The list of customers in line
        :return: Two seperate boxes. The first, which is right next to the cashier,
            shows the current customer being helped, and will slowly disappear over time as it's items
            are checked out. The second is a non interactable block that shows the number of customers
            in line for the current cashier
        """

        # Get the mouse's position
        mouse = pygame.mouse.get_pos()

        # Is the mouse within the confines of the first customer block?
        if x - 5 > mouse[0] > x - 30 and y + 25 > mouse[1] > y:
            # Only do something if there is at least one person in line
            if len(cashier_queue) > 0:
                # Draw a completely white cashier
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (x - 30, y, 25, 25))

                # Show the current number of item's the the customer has left on top
                itemsText = "Items Left: " + str(round(cashier_queue[0].number_of_items, 2))
                self.text_box(itemsText, int(self.displayWidth / 3), 60, width=int(self.displayWidth / 3), height=25)
        # Print a single customer block that disappears as the number of items it has goes down
        elif len(cashier_queue) > 0:
            # Set transparency by the number of items currently in the queue
            if cashier_queue[-1].number_of_items >= 0 and cashier_queue[-1].total_items > 0:
                # Block goes from white to black
                transparency = int(255 * cashier_queue[-1].number_of_items / cashier_queue[-1].total_items)
            else:
                # In case of weird input, show a completely white block
                transparency = 255
            # Draw a customer block
            try:
                pygame.draw.rect(self.screen, (transparency, transparency, transparency),
                             (x - 30, y, 25, 25))
            except Exception as E:
                print(E, "Transparency is", transparency, "Number of items left", cashier_queue[-1].number_of_items, "Total items", cashier_queue[-1].total_items)
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (x - 30, y, 25, 25))
        # If there is more than 1 person in line
        if len(cashier_queue) > 1:
            # Draw a second square to represent the rest of the customers in line
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (x - 30, y - 30, 25, 25))

            # Represent the number of people in line as a string
            lineText = str(len(cashier_queue) - 1)

            # Write these items to screen
            textSurf, textRect = self.textObj(lineText, self.smallFont, self.red)
            textRect.center = ((x - 30 + int(25 / 2)),
                               (y - 30 + int(25 / 2)))
            self.screen.blit(textSurf, textRect)

    def textObj(self, text, t_font, t_color):
        """
        Used to get the necessary references to make and print text to screen

        :param text: A string to display; Numbers of any type must be passed through str()
        :param t_font: The font to print this text in
        :param t_color: The color to show this text with
        :return: The components to write text to screen
        """

        # Render the text using the specified font
        textSurface = t_font.render(text, True, t_color)

        # Return the render, and the rectangle so that people can modify it's location
        return textSurface, textSurface.get_rect()

    def text_box(self, text, x, y, width, height):
        """
        Used to quickly display a solid rectangle with text inside of it

        :param text: Text to display; Must be of type string, pass numbers through
            str(number) conversion before sending it here
        :param x: The x position of the rectangle and text on screen
        :param y: The y position of the rectangle and text on screen
        :param width: How wide the background rectangle should be; Does
            not effect the text
        :param height: How long the background rectable should be; Does
            not effect the text
        :return: A simple text box on screen
        """

        # Draw a green rectangle
        pygame.draw.rect(self.screen, self.green,
                         (x, y,
                          width, height))

        # Render the text
        textSurf, textRect = self.textObj(text, self.smallFont, self.white)

        # Position the text inside the box
        textRect.center = ((x + (width / 2)),
                           (y + ((height) / 2)))

        # Write the text to screen
        self.screen.blit(textSurf, textRect)


if __name__ == '__main__':
    # Do not allow this function to be called as main.
    pass
