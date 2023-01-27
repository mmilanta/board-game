import random
from prettytable import PrettyTable
import json
import numpy
from argparse import ArgumentParser
from tqdm import tqdm

"""
def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", default="stats.json", 
                        help="stats_file path")
    parser.add_argument("-n", "--dice_rolls", dest="n", default=10000,
                        help="number of iterations")    


    args = parser.parse_args()    
    with open(args.filename) as json_file:
        stats = json.load(json_file)
        #out = [[0 for _ in range(len(stats.values()))] for _ in range(len(stats.values()))]
        run_stats(stats,int(args.n))
    """
def main():
    parser = ArgumentParser()
    parser.add_argument("-a", "--attacker", dest="attacker", default="d6", 
                        help="attacker dice")
    parser.add_argument("-d", "--defender", dest="defender", default="d6", 
                        help="defender dice")
    parser.add_argument("-n", "--dice_rolls", dest="n", default=1000,
                        help="number of iterations")    
    
    args = parser.parse_args()  
    args.n = int(args.n)  
    count = 0
    for _ in tqdm(range(args.n)):
        if run_dices(dices(args.attacker))>run_dices(dices(args.defender)):
            count += 1
    print("Attacker: {0} - Defender: {1}".format(args.attacker,args.defender))
    print("Prob. attack to win: {0}".format(count/args.n))

def run_stats(stats, n):
    my_table = PrettyTable()
    my_table.field_names = ["att.\\def."] +  list(stats.keys())

    for attacker in stats.keys():
        t = [attacker]
        for defender in stats.keys():
            t += [simulate(dices(stats[attacker]["attack"]), dices(stats[defender]["defence"]),n)]
        my_table.add_row(t)
    print(my_table)

def simulate(d_attacker, d_defender, n):
    count = 0
    for _ in range(n):
        if run_dices(d_attacker)>run_dices(d_defender):
            count +=1
    return count/n

def dices(text):
    dices = text.split("+")
    out = []
    for dice_txt in dices:
        out += dice(dice_txt)
    return out

def dice(text="d6"):
    mult, val = text.split("d")
    if mult == '':
        mult = '1'
    mult = int(mult)
    val = int(val)
    return [val]*mult

def run_dices(code):
    out = 0
    for d in code:
        out += random.choice(range(d)) + 1
    return out

if __name__ == "__main__":
    main()