import random
"""
This are all the possible mutation
"""
condition_container = [
    {(-1, 1): 0, (0, 1): 0, (1, 1): 0, (-1, 0): 1, (1, 0): 1},
    {(0, 1): 1, (0, -1): 1, (1, -1): 0, (1, 1): 0},
    {(-1, 1): 0, (0, 1): 0, (1, 1): 0},
    {(1, -1): 0, (1, 0): 0, (1, 1): 0},
    {(-1, 0): 1, (0, 0): 1, (1, 0): 1}, # Estrime
    {(0, -1): 1, (0, 0): 1, (0, 1): 1}  # Estrime
]
action_container = [
    {(0, 1): 1, (1, 1): 1, (-1, 1): 1, (0, 0): 0},
    {(1, 0): 1, (1, 1): 1, (1, -1): 1, (0, 0): 0},
    {(0, 1): 1},
    {(1, 0): 1},
    {(0, 0): 0, (-1, 1): 1,(0, 1): 0,(1, 1): 1, (-1, 2): 1, (0, 2): 0, (1, 2): 1, (-1, 3): 1, (0, 3): 0, (1, 3): 1, (-1, 4): 1, (0, 4): 0, (1, 4): 1, (-1, 5): 1, (0, 5): 0, (1, 5): 1, (-1, 6): 1, (0, 6): 1, (1, 6): 1},  # Estrime
    {(0, 0): 0, (1, 1): 1,(1, 0): 0,(1, -1): 1,(2, 1): 1,(2, 0): 0,(2, -1): 1,(3, 1): 1,(3, 0): 0,(3, -1): 1,(4, 1): 1,(4, 0): 0,(4, -1): 1,(5, 1): 1,(5, 0): 0,(5, -1): 1,(6, 1): 1,(6, 0): 1,(6, -1): 1,}  # Estrime
]
invertible = [
    (False, True), # Vertical symmetry
    (True, False), # Horizontal symmetry
    (False, True), # Vertical symmetry
    (True, False),  # Horizontal symmetry
    (False, True),  # Vertical symmetry
    (True, False) # Horizontal symmetry
]

def change_direction(direction, move):
    direction[0] = not direction[0] if invertible[move][0] else direction[0]
    direction[1] = not direction[1] if invertible[move][1] else direction[1]
    return direction

def check_one_random_move(neighbors, failed_moves):
    allowed_indices = [i for i in range(len(condition_container)) if i not in failed_moves]
    move = random.choice(allowed_indices)

    direction = [False, False]
    if random.choice([True, False]):
        direction = change_direction(direction, move)

    outcome = check_valid_move(neighbors, move, direction)
    if not outcome:
        direction = change_direction(direction, move)
        outcome = check_valid_move(neighbors, move, direction)
    return outcome, move, direction

def check_valid_move(neighbors, move_number, direction):
    num_checks = 0
    dir_x, dir_y = direction
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x, y) in condition_container[move_number]:
                oriented_x = -x if dir_x else x
                oriented_y = -y if dir_y else y
                if neighbors[oriented_x][oriented_y] == condition_container[move_number][x, y]:
                    num_checks += 1
                    if num_checks == len(condition_container[move_number]):
                        return True
    return False
