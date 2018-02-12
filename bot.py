import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0


def main(player_key):
    global map_size
    global state
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y, move):
    # 1=fire shot command code
    cell = state['OpponentMap']['Cells']
    f_shot = open("shots.txt", "a")
    f_shot.write('{},{},{},{},{},{},{}\n'.format(x, y, move, cell[x*map_size + y]['Damaged'], cell[x*map_size + y]['Missed'], cell[x*map_size + y]['X'], cell[x*map_size + y]['Y']))
    f_shot.close()
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def is_checked(x, y):
    if ((is_damaged(x-1, y) or is_missed(x-1, y)) and (is_damaged(x+1, y) or is_missed(x+1, y)) and (is_damaged(x, y-1) or is_missed(x, y-1)) and (is_damaged(x, y+1) or is_missed(x, y+1))):
        return True
    else:
        return False

def is_damaged(x, y):
    opponent_map = state['OpponentMap']['Cells']
    if (x>=0) and (x<map_size) and (y>=0) and (y<map_size):
        return (opponent_map[x*map_size + y]['Damaged'])
    else:
        return True

def is_missed(x, y):
    opponent_map = state['OpponentMap']['Cells']
    if (x>=0) and (x<map_size) and (y>=0) and (y<map_size):
        return (opponent_map[x*map_size + y]['Missed'])
    else:
        return True

def is_available(x, y):
    return ((not is_damaged(x, y)) and (not is_missed(x, y)))


def destroy_ship(hitlist):
    target = choice(hitlist)
    valid_target = None
    if is_available(target[0]-1, target[1]):
        valid_target = target[0]-1, target[1]
    elif is_available(target[0]+1, target[1]):
        valid_target = target[0]+1, target[1]
    elif is_available(target[0], target[1]-1):
        valid_target = target[0], target[1]-1
    elif is_available(target[0], target[1]+1):
        valid_target = target[0], target[1]+1
    output_shot((*valid_target), 1)



# Mendapat koordinat tembakan sebelumnya yang bernilai "HIT"
# Melakukan algoritma


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)


    # sudah mendapat koordinat dari file eksternal


    hit_list = []
    targets = []
    cross_shot_targets = []
    #shotlist = []
    #convertshot(shotlist)
    # Mengakses x dan y terakhir dgn cara -> shotlist[-1] (Hasilnya akan [X, Y]
    #lastshot = shotlist[-1];
    for cell in opponent_map:
        if ((cell['Damaged']) and (not is_checked(cell['X'], cell['Y']))):
            valid = (cell['X'], cell['Y'])
            hit_list.append(valid)
    if (len(hit_list)>0):
        destroy_ship(hit_list)
    else:
        for cell in opponent_map:
            # Memilih cell yang tidak damaged, missed, dan grid yang X dan Y nya genap
            if ((not cell['Damaged']) and (not cell['Missed']) and ((((cell['X'] % 2) == 0) and ((cell['Y'] % 2) == 0)) or (((cell['X'] % 2) == 1) and ((cell['Y'] % 2) == 1)))):
                valid_cell = (cell['X'], cell['Y'])
                targets.append(valid_cell)
                if (is_cross(cell['X'], cell['Y'])):
                    valid_cross_cell = (cell['X'], cell['Y'])
                    cross_shot_targets.append(valid_cross_cell)
        target = choice(targets)
        energy = state['PlayerMap']['Owner']['Energy']
        if ((len(cross_shot_targets) >= 0) and ((map_size == 7 and energy >= 24) or (map_size == 10 and energy >= 36) or (map_size == 14 and energy >= 48))):
            targetcross = choice(cross_shot_targets)
            output_shot((*targetcross), 5)
        else:
            output_shot((*target), 1)
    return

def is_cross(x, y):
    # mengecek apakah titik (x,y) sebagai titik tengah cross shot memenuhi sebagai kandidat cross shot
    # ke 4 titik lainnya harus layak untuk ditembak
    # kelayakan untuk ditembak adalah ketika tidak damaged dan tidak missed

    if ((x >= 1) and (x <= map_size - 2) and (y >= 1) and (y <= map_size - 2)):
        # tidak berada di pinggir map
        point_south_west = (x - 1, y - 1)
        point_north_west = (x - 1, y + 1)
        point_north_east = (x + 1, y + 1)
        point_south_east = (x + 1, y - 1)
        return(is_available(*point_south_west) and is_available(*point_north_west) and is_available(*point_north_east) and is_available(*point_south_east))
    else:
        return False


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west
    f_shot = open("shots.txt", "w")
    f_shot.write('')
    f_shot.close()
    ships = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 4 2 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]
    # Menghapus shots.txt yg awal
    with open("shots.txt", "w") as f_shot:
        f_shot.close()
    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
