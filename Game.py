from GameSimulator import GameSimulator
from NIMManager import NIMManager
from LedgeManager import LedgeManager
from HexManager import HexManager
from Node import Node
import json

class Game:
    def __init__(self):
        self.conf = json.loads(open("conf.json", "r").read())
        self.G = self.conf["G"]
        self.M = self.conf["M"]
        self.game_type = self.conf["GameType"]
        self.verbose = self.conf["Verbose"]
        self.correct_winner_count = 0
        self.p1_winner_count = 0
        self.p1_starting_count = 0
        self.p2_winner_count = 0
        self.p2_starting_count = 0
    
    
    def initiate_game_manager(self):
        player_conf = self.conf["P"]
        if (self.game_type == "NIM"):
            nim_conf = self.conf["NIM"]
            self.game_manager = NIMManager(nim_conf["N"], nim_conf["K"], player_conf)         
        elif (self.game_type == "Ledge"):
            ledge_conf = self.conf["Ledge"]
            self.game_manager = LedgeManager(ledge_conf["B"], player_conf)
        elif (self.game_type == "Hex"):
            hex_conf = self.conf["Hex"]
            self.game_manager = HexManager(hex_conf["size"], hex_conf["frame_rate"], player_conf)
        else:
            print(f"Does not support {self.game_type} yet.") 
    
    
    def play(self):
        for i in range(self.G):
            self.initiate_game_manager()
            self.current_state = self.game_manager.initial_state()
            self.root = Node(self.current_state, None)
            self.simulator = GameSimulator(self.M, self.game_manager)
            self.starting_player = self.game_manager.current_player
            
            print(f"Starting player:\t P{self.game_manager.current_player}")
            if(self.verbose):
                print(self.game_manager.get_start_position_as_string())
            
            self.single_game()
            

        print("--------------------------------------------------------------")
        print(f"Total games:\t\t\t\t {self.G}")
        print(f"Games won by Player 1:\t\t\t {self.p1_winner_count}")
        print(f"Games where Player 1 had first move:\t {self.p1_starting_count}")
        print(f"Games won by Player 2:\t\t\t {self.p2_winner_count}")
        print(f"Games where Player 2 had first move:\t {self.p2_starting_count}")
        print(f"Percentage of games won by the player who had first move: {100*self.correct_winner_count/self.G} %")
        print("--------------------------------------------------------------") 
        while(True):
            pass
    
    def single_game(self):
        
        while not self.game_manager.is_finished(self.root.game_state):
            self.simulator.run_simulations(self.root)
            old_game_state = self.root.game_state
            self.root = self.root.best_traverse() # self.root.most_visited_child()
            self.root.set_as_root()
            new_game_state = self.root.game_state
            
            if(self.verbose):
                print(self.game_manager.get_move_as_string(old_game_state, new_game_state))
        
        
        winner = self.game_manager.get_winner(self.root.game_state)
        self.update_game_stats(winner)
        
        print(f"Winner:\t\t\t P{winner}")
        print("-----------\n")

    def update_game_stats(self, winner):
        if(self.starting_player == 1):
            self.p1_starting_count += 1
        else:
            self.p2_starting_count += 1
        
        if(winner == 1):
            self.p1_winner_count += 1
        else:
            self.p2_winner_count += 1
            
        if (winner == self.starting_player):
            self.correct_winner_count += 1

game = Game()
game.play()















