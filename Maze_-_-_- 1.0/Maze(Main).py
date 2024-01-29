from Displey import *
from Rules import *
import random
import time

Walkable = 1
Wall = 0
Boundary = -1
StartOrGool = 2
Goal = 3

LabSize = 20
PixelsPerSquare = 60
WindowsSize = LabSize * PixelsPerSquare
Squares = [[0 for _ in range(LabSize)] for _ in range(LabSize)]
WalkableSquaresList = []
StartSquare = [0, 0]
GoalSquare = [0, 0]

FailedMovesAtCoordinates = {}
UntouchableSquares = []
NumMutations = 1500
TimePerMutation = 0.001

def remove_failed_moves_nearby(pos):
    """
    Remove all the neighbor squares from Untouchable Squares

    Parameters:
    - pos: Coordinates of the center.
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            pos_tuple = (pos[0] + i, pos[1] + j)
            if pos_tuple in FailedMovesAtCoordinates:
                del FailedMovesAtCoordinates[pos_tuple]
            if pos_tuple in UntouchableSquares:
                UntouchableSquares.remove(pos_tuple)
                display_small_square(pos[0] + i, pos[1] + j, color_rgb(200, 20, 20), PixelsPerSquare, PixelsPerSquare / 3)

def get_neighboring_squares(pos):
    """
    Get the values of neighboring squares.

    Parameters:
    - pos: Coordinates of the center.

    Returns:
    List of lists representing neighboring square values.
    """
    x, y = pos
    neighbors = [[0 for _ in range(3)] for _ in range(3)]

    for i in range(-1, 2):
        for j in range(-1, 2):
            new_x, new_y = x + i, y + j
            if 0 <= new_x < LabSize and 0 <= new_y < LabSize:
                neighbors[i][j] = Squares[new_x][new_y]  # 1 Walkable or 0 Wall or 2 (Start or End)
            else:
                neighbors[i][j] = Boundary  # -1 Boundary

    return neighbors

def change_square(pos, value):
    """
    Change the value of a square and handle related actions.

    Parameters:
    - pos: Coordinates of the square.
    - value: Value for the square.
    """
    # Specific actions
    if Squares[pos[0]][pos[1]] == StartOrGool:
        return
    if Squares[pos[0]][pos[1]] == Walkable and value != Walkable:
        WalkableSquaresList.remove([pos[0], pos[1]])
    # General actions
    if value == Walkable:
        display_square(pos[0], pos[1], color_rgb(0, 143, 57), PixelsPerSquare)
        WalkableSquaresList.append([pos[0], pos[1]])
    if value == StartOrGool:
        display_square(pos[0], pos[1], color_rgb(255, 126, 0), PixelsPerSquare)
    if value == Wall:
        display_square(pos[0], pos[1], color_rgb(0, 0, 0), PixelsPerSquare)
    if value == Goal:
        display_square(pos[0], pos[1], color_rgb(30, 200, 30), PixelsPerSquare)
        value = StartOrGool
    Squares[pos[0]][pos[1]] = value
    remove_failed_moves_nearby(pos)

def main():
    Start(WindowsSize)
    # Select start point
    while True:
        x, y = get_click_position()
        SquareX = int(x / PixelsPerSquare)
        SquareY = int(y / PixelsPerSquare)
        # remove the if statement if you want to start in the center
        if SquareX == 0 or SquareY == 0 or SquareX == LabSize - 1 or SquareY == LabSize - 1:
            StartSquare[0] = SquareX
            StartSquare[1] = SquareY
            change_square([SquareX, SquareY], StartOrGool)
            print(f"You clicked at coordinates: ({SquareX}, {SquareY})")
            break
    # Select goal point
    x, y = get_click_position()
    SquareX = int(x / PixelsPerSquare)
    SquareY = int(y / PixelsPerSquare)
    GoalSquare[0] = SquareX
    GoalSquare[1] = SquareY
    change_square([SquareX, SquareY], Goal)
    print(f"You clicked at coordinates: ({SquareX}, {SquareY})")
    # Create optimal path
    Pos = StartSquare.copy()
    while True:
        if Pos != StartSquare and Pos != GoalSquare:
            change_square(Pos, Walkable)
        if Pos[0] < GoalSquare[0]:
            Pos[0] += 1
            continue
        if Pos[0] > GoalSquare[0]:
            Pos[0] -= 1
            continue
        if Pos[1] < GoalSquare[1]:
            Pos[1] += 1
            continue
        if Pos[1] > GoalSquare[1]:
            Pos[1] -= 1
            continue
        break
    # Create branches
    for _ in range(NumMutations):
        # Convert lists to sets
        set_a = set(tuple(coord) for coord in WalkableSquaresList)
        set_b = set(tuple(coord) for coord in UntouchableSquares)
        # Calculate set difference
        difference = set_a - set_b
        # Convert result to a list
        allowed_indices = list(difference)
        if len(allowed_indices) - 1 == 0:  # Maximum mutations reached
            break
        i = random.randint(0, len(allowed_indices) - 1)
        Pos = allowed_indices[i]
        pos_tuple = tuple(Pos)
        neighbors = get_neighboring_squares(Pos)
        outcome, move, direction = check_one_random_move(neighbors, FailedMovesAtCoordinates.get(pos_tuple, []))

        if pos_tuple in FailedMovesAtCoordinates:
            FailedMovesAtCoordinates[pos_tuple].append(move)
        else:
            FailedMovesAtCoordinates[pos_tuple] = [move]
        if len(FailedMovesAtCoordinates.get(pos_tuple, [])) == len(condition_container):
            UntouchableSquares.append(pos_tuple)
            display_small_square(Pos[0], Pos[1], color_rgb(200, 200, 200), PixelsPerSquare, PixelsPerSquare / 3)
        if outcome:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x, y) in action_container[move]:
                        DirX = -x if direction[0] else x
                        DirY = -y if direction[1] else y
                        change_square([Pos[0] + DirX, Pos[1] + DirY], action_container[move][(x, y)])
        time.sleep(TimePerMutation)
    End()
if __name__ == "__main__":
    main()