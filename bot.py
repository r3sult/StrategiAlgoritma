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
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    f_shot = open("shots.txt", "a")
    f_shot.write('{},{}\n'.format(x, y))
    f_shot.close()
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def destroy_ship():
    #Mendapat koordinat tembakan sebelumnya yang bernilai "HIT"
    #Melakukan algoritma
    


def convertshot(shotlist):
    #Convert file eksternal menjadi list
    with open("shots.txt", "r") as f:
        #Inisiasi seluruh isi file ke shotlist masih berbentuk str dan memiliki koma
        shotlist = f.readlines()
    # Menghilangkan \n
    shotlist = [x.strip() for x in shotlist]
    i=0
    for x in shotlist:
        #Menjadikan isi shotlist menjadi list of list (['1', '2'], ['3', '5']]) etc
        shotlist[i] = x.split(",")
        i+=1
    return


def shield():
    #   Each player is given a shield at the start of the game with 0 charges and a protection radius of 0.
    #   The shield will only be usable at the start of phase 2.
    #   After 7 rounds of not using the shield The shield will gain an additional charge.
    #   For every charge the shield protection radius will grow by 1.
    #   The shield will protect a square of cells, given the protection radius of the shield.
    #   The shield has a max radius protection size, depending on the size of the map.
    #       Small map will be a max radius of 1 unit: so a 3 x 3 block will be covered.
    #       Medium Map will be a max radius of 2 units: so a 5 x 5 block will be covered.
    #       Large Map will be a max radius of 3 units: so a 7 x 7 block will be covered.
    #   The shield will prevent any shots from hitting the cell underneath the shield.
    #   A shielded cell will only say it is shielded if it was hit.
    #   Only one shield can be activated at a time.
    #   Shields do not gain charge while they are active.
    #   Shields lose 1 charge for each round they are active.
    #   A shield must have at least 1 charge before it can be placed.
    #   Shields block seeker missiles from finding targets underneath the shield.

    if (map_size == 7):
        output_shot(4,4,8)
    elif (map_size == 10):
        output_shot(5,5,8)
    else:
        output_shot(7,7,8)

def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)


    #sudah mendapat koordinat dari file eksternal


    targets = []
    cross_shot_targets = []
    shotlist = []
    convertshot(shotlist)
    #Mengakses x dan y terakhir dgn cara -> shotlist[-1] (Hasilnya akan [X, Y]
    lastshot = shotlist[-1];
    if (is_hit(lastshot)):
    	destroy_ship()
    else:
	    for cell in opponent_map:
	        #Memilih cell yang tidak damaged, missed, dan grid yang X dan Y nya genap
	        if not cell['Damaged'] and not cell['Missed'] and ((cell['X'] % 2) == 0) and ((cell['Y'] % 2) == 0):
	            valid_cell = cell['X'], cell['Y']
	            targets.append(valid_cell)
	    target = choice(targets)
        if (len(cross_shot_targets) >= 0 and ((map_size == 7 and energy >= 24) or (map_size == 10 and energy >= 36) or (map_size == 14 and energy >= 48))):

        output_shot(*target)
return

def isCross(x, y, opponent_map):


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
    #Menghapus shots.txt yg awal
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
