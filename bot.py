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
        x,y = check_state()
        if (x==-1 and y==-1):
            fire_shot(state['OpponentMap']['Cells'])
        else:
            output_shot(x, y, 8)


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

def ship_hitted():
    player_ship = state['PlayerMap']['Owner']['Ships']
    for i in range(5):
        hit = False
        shielded = False
        if (not player_ship[i]['Destroyed']):
            for cell in player_ship[i]['Cells']:
                if (not cell['Shielded']):
                    if (cell['Hit']):
                        x = cell['X']
                        y = cell['Y']
                        hit = True
                    if (cell['ShieldHit']):
                        shielded = True
                else:
                    return -1,-1
            if (hit and (not shielded)):
                return x,y
    return -1,-1

def check_state():
    player = state['PlayerMap']['Owner']
    if (player['Shield']['CurrentRadius'] == player['Shield']['MaxRadius']):
        x,y = ship_hitted()
        return x,y
    else:
        return  -1,-1



def is_damaged(x, y):
    opponent_map = state['OpponentMap']['Cells']
    if (x>=0) and (x<map_size) and (y>=0) and (y<map_size):
        return (opponent_map[x*map_size + y]['Damaged'])
    else:
        return False

def is_missed(x, y):
    opponent_map = state['OpponentMap']['Cells']
    if (x>=0) and (x<map_size) and (y>=0) and (y<map_size):
        return (opponent_map[x*map_size + y]['Missed'])
    else:
        return True

def is_available(x, y):
    return ((not is_damaged(x, y)) and (not is_missed(x, y)))


def seek_ship(x, y, dirx, diry, num):
    if (is_missed(x, y)):
        seek_ship(x-dirx, y-diry, 0-dirx, 0-diry, num+1)
    elif (is_damaged(x, y)):
        seek_ship(x+dirx, y+diry, dirx, diry, num)
    else:
        output_shot(x, y, 1)


def destroy_ship(x, y):
    player_ship = state['PlayerMap']['Owner']['Ships']
    player_energy = state['PlayerMap']['Owner']['Energy']
    if (is_damaged_nearby(x, y)):
        if (is_damaged(x, y+1) or is_damaged(x, y-1)):
            seek_ship(x, y, 0, 1, 1)
        else:
            seek_ship(x, y, 1, 0, 1)
    else:
        if (is_available(x, y+1) and is_available(x, y-1) and (player_ship[1]['Weapons'][1]['EnergyRequired'] <= player_energy) and (not player_ship[1]['Destroyed'])):
            output_shot(x, y, 2)
        elif (is_available(x+1, y) and is_available(x-1, y) and (player_ship[1]['Weapons'][1]['EnergyRequired'] <= player_energy) and (not player_ship[1]['Destroyed'])):
            output_shot(x, y, 3)
        elif (is_available(x, y+1)):
            output_shot(x, y+1, 1)
        elif (is_available(x+1, y)):
            output_shot(x+1, y, 1)
        elif (is_available(x, y-1)):
            output_shot(x, y-1, 1)
        else:
            output_shot(x-1, y, 1)
    return



def is_damaged_nearby(x, y):
    return (is_damaged(x-1, y) or is_damaged(x+1,y) or is_damaged(x, y-1) or is_damaged(x, y+1))

def check_hit_after(x, y, up, right):
    if ((x>=0 and x<map_size) and (y>=0 and y<map_size)):
        if (is_available(x, y)):
            return True
        elif (is_damaged(x, y)):
            return (check_hit_after(x+up, y+right, up, right))
        else:
            return False
    else:
        return False

def check_hit(x, y, up, right):
    if ((up == 0) and (right ==0)):
        if (is_damaged_nearby(x, y)):
            if ((is_damaged(x+1, y) or is_damaged(x-1, y)) and (is_damaged(x, y+1), is_damaged(x, y-1))):
                return (check_hit(x+1, y, 1, 0) and check_hit(x, y+1, 0, 1))
            elif (is_damaged(x+1, y) or is_damaged(x-1, y)):
                return (check_hit(x+1, y, 1, 0))
            else:
                return (check_hit(x, y+1, 0, 1))
        else:
            return True
    else:
        if (is_missed(x, y)):
            return check_hit_after(x-up, y-right, 0-up, 0-right)
        elif (is_damaged(x, y)):
            return (check_hit(x + up, y + right, up, right))
        else:
            return True

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
        if (cell['Damaged']):
            valid = (cell['X'], cell['Y'])
            if (check_hit((*valid), 0, 0)):
                destroy_ship(*valid)
                return

    else:
        sort_list(targets, cross_shot_targets)
        target = choice(targets)
        player_energy = state['PlayerMap']['Owner']['Energy']
        player_ship = state['PlayerMap']['Owner']['Ships']
        if ((len(cross_shot_targets) > 0) and (not player_ship[2]['Destroyed']) and (player_ship[2]['Weapons'][1]['EnergyRequired'] <= player_energy)):
            targetcross = choice(cross_shot_targets)
            output_shot((*targetcross), 5)
        else:
            output_shot((*target), 1)
    return

def sort_list(targets, cross_shot_targets):
    opponent_map = state['OpponentMap']['Cells']
    for cell in opponent_map:
        # Memilih cell yang tidak damaged, missed, dan grid yang X dan Y nya genap
        if ((not cell['Damaged']) and (not cell['Missed']) and ((((cell['X'] % 2) == 0) and ((cell['Y'] % 2) == 0)) or (
            ((cell['X'] % 2) == 1) and ((cell['Y'] % 2) == 1)))):
            valid_cell = (cell['X'], cell['Y'])
            targets.append(valid_cell)
            if (is_cross(cell['X'], cell['Y'])):
                valid_cross_cell = (cell['X'], cell['Y'])
                cross_shot_targets.append(valid_cross_cell)

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
    if (map_size == 10):
        ships = ['Battleship 0 3 north',
                 'Carrier 5 3 East',
                 'Cruiser 1 0 north',
                 'Destroyer 8 1 East',
                 'Submarine 1 7 north'
                 ]
    elif (map_size == 7):
        ships = ['Battleship 0 0 East',
                 'Carrier 3 3 East',
                 'Cruiser 6 4 north',
                 'Destroyer 6 2 north',
                 'Submarine 5 0 north'
                 ]
    else:
        ships = ['Battleship 1 13 East',
                 'Carrier 0 6 East',
                 'Cruiser 11 2 East',
                 'Destroyer 12 1 East',
                 'Submarine 11 8 north'
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
