from abc import ABC, abstractmethod
import random

class GameManager(ABC):
    
    def __init__(self, P):
        self.current_player = None
        self.P = P
    
    @abstractmethod
    def initial_state(self):
        if(self.current_player == None and self.P == 3):
            self.current_player = 1 if random.randint(1, 11) <= 5 else 2
        elif(self.current_player == None and self.P == 1):
            self.current_player = 1
        elif(self.current_player == None and self.P == 2):
            self.current_player = 2
        pass
        
    @abstractmethod
    def is_finished(self, game_state):
        pass
    
    @abstractmethod
    def get_all_next_states(self, game_state):
        pass
    
    @abstractmethod
    def get_winner(self, game_state):
        pass
        
    @abstractmethod
    def get_move_as_string(self, old_game_state, new_game_state):
        pass
    
    @abstractmethod
    def get_start_position_as_string(self):
        pass
    
    def alternate_player(self, player):
        return 1 if player == 2 else 2