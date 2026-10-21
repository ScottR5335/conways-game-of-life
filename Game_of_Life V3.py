import sys
import pygame
pygame.init()

timer = pygame.time.Clock()
# Raise the speed to speed up the progression to the next stage of life.
speed = 5

num_cells_wide = 140
num_cells_high = 80

# cell size should be an odd number
cell_size = 9

num_screen_updates = 0

screen_width = cell_size*num_cells_wide-1
screen_height = cell_size*num_cells_high-1

print(f"Screen width: {str(screen_width)}")
print(f"Screen height: {str(screen_height)}")

point_color = (0,0,255)

screen = pygame.display.set_mode([screen_width,screen_height])
screen_color = (180,180,180)
screen.fill(screen_color)

class Cell:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.previous_column = (self.x-1)%num_cells_wide
        self.next_column = (self.x+1)%num_cells_wide
        self.previous_row = (self.y-1)%num_cells_high
        self.next_row = (self.y+1)%num_cells_high
        self.all_neighbor_coords = [(self.previous_column, self.previous_row),
                                     (self.previous_column, self.y),
                                     (self.previous_column, self.next_row),
                                     (self.x, self.previous_row),
                                     (self.x, self.next_row),
                                     (self.next_column, self.previous_row),
                                     (self.next_column, self.y),
                                     (self.next_column, self.next_row)]
        self.currently_alive = False
        self.alive_in_next_stage = False


    def living_neighbor_count(self):
        num_living_neighbors = 0
        # print(f"The number of neighbors is {str(len(self.all_neighbor_coords))}.")
        for coordinates in self.all_neighbor_coords:
            if cols[coordinates[0]][coordinates[1]].currently_alive:
                num_living_neighbors += 1
        return num_living_neighbors




# cols is a list containing lists of cells.
cols = []
# rows is a list containing cells

def mouse_on_display_screen(mouse_position):
    if ((0 <= mouse_position[0] <= screen_width) and (0 <= mouse_position[1] <= screen_height)):
        return True
    else:
        return False
    
def change_cell_life_value(cell_col, cell_row):
    cols[cell_col][cell_row].currently_alive = not(cols[cell_col][cell_row].currently_alive)

def update_screen():
    # Plot a clear screen.
    print(f"Screen is being updated.")
    screen.fill(screen_color)
    for col_value in range(0,num_cells_wide):
        for row_value in range(0,num_cells_high):
            if cols[col_value][row_value].currently_alive:
                # pygame.draw.circle(screen, point_color, (cell_size*col_value+2,cell_size*row_value+2), 5)
                pygame.draw.rect(screen, point_color, pygame.Rect(cell_size*col_value, cell_size*row_value,cell_size,cell_size))
    pygame.display.flip()



# fill the cell matrix with dead cells
for col_value in range(0,num_cells_wide):
    rows = []
    # create a column of cells and then append it to cols
    for row_value in range(0,num_cells_high):
        coordinates = (col_value, row_value)
        new_cell = Cell(coordinates)
        rows.append(new_cell)
        # print(coordinates)
    cols.append(rows)
    # print (f"The column with index {col_value} was just filled with dead cells.")
print("The matrix has been filled.")

update_screen()

running = True
life_progressing = False
while running:
    timer.tick(speed)

    # User sets initial coditions by clicking on the grid to bring cells to life.
    # When user is satisfied, pressing "Enter" will start the progression of life.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not(life_progressing):
            # print("Waiting for the initial cells to be selected.")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("The Mouse was left-clicked while on the display screen.")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_position = (mouse_x,mouse_y)
                if mouse_on_display_screen(mouse_position):
                    cell_col = mouse_x//cell_size
                    cell_row = mouse_y//cell_size
                    change_cell_life_value(cell_col, cell_row)

        # pause or start the progression of life with the enter key
        # if the game is paused (or hasn't begun), cells can be killed or
        # brought to life with a mouse-click
        if event.type == pygame.KEYDOWN:
            if((event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER)):
                    life_progressing = not(life_progressing)
            
    if life_progressing:
        # Start the progression of life.
        for col_value in range(0,num_cells_wide):
            for row_value in range(0,num_cells_high):
                current_cell = cols[col_value][row_value]
                # Determine the appropriate state (alive/dead) for the next stage.
                if current_cell.currently_alive:
                    """current_cell.identify_all_neighbor_coords()"""
                    if current_cell.living_neighbor_count() in [2,3]:
                        current_cell.alive_in_next_stage = True
                    else:
                        current_cell.alive_in_next_stage = False
                if not(current_cell.currently_alive):
                    if current_cell.living_neighbor_count() == 3:
                        current_cell.alive_in_next_stage = True
                    else:
                        current_cell.alive_in_next_stage = False
        # Assign the appropriate state for the next stage to the current state.
        print(f"Update_screen was called this many times: {num_screen_updates}.")
        for col_value in range(0,num_cells_wide):
            for row_value in range(0,num_cells_high):
                current_cell = cols[col_value][row_value]
                current_cell.currently_alive = current_cell.alive_in_next_stage
    
    num_screen_updates += 1
    update_screen()

pygame.quit()
sys.exit()