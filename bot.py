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


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    
    
    #sudah mendapat koordinat dari file eksternal
    
    
    targets = []
    shotlist = []
    convertshot(shotlist)
    #Mengakses x dan y terakhir dgn cara -> shotlist[-1] (Hasilnya akan [X, Y]
    for cell in opponent_map:
        #Memilih cell yang tidak damaged, missed, dan grid yang X dan Y nya genap
        if not cell['Damaged'] and not cell['Missed'] and ((cell['X'] % 2) == 0) and ((cell['Y'] % 2) == 0):
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)
    output_shot(*target)
    return	


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

    
    
    
    
