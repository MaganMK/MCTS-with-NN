from Node import Node
import json
import random

class GameSimulator:
    
    def __init__(self, M, game_manager):
        self.M = M
        self.game_manager = game_manager
    
    
    def run_simulations(self, root):
        for i in range(self.M):
            leaf = self.tree_search(root)
            self.node_expansion(leaf)
            new_leaf = self.choose_rollout_root(leaf)
            winner = self.rollout(new_leaf)
            self.backpropagate(new_leaf, winner)
        
        
    def tree_search(self, root):
        current_node = root
        
        while not current_node.is_leaf():
            current_node = current_node.best_traverse()
        
        return current_node
    
    
    def node_expansion(self, leaf):
        game_state = leaf.game_state
        next_states = self.game_manager.get_all_next_states(game_state)
        if(next_states == None):
            return leaf
            
        for state in next_states:
            new_node = Node(state, leaf)
            leaf.add_child(new_node)
    
    
    def choose_rollout_root(self, node):
        return random.choice(list(node.children.keys())) if not node.is_leaf() else node
          
            
    def rollout(self, node):
        current_game_state = node.game_state
    
        while not self.game_manager.is_finished(current_game_state):
            current_game_state = self.random_move(current_game_state)
        
        return self.game_manager.get_winner(current_game_state)
    
    
    def random_move(self, game_state):
        next_states = self.game_manager.get_all_next_states(game_state)
        return random.choice(next_states)
    
    
    def backpropagate(self, leaf, winner):
        current_node = leaf
        
        while(current_node.parent != None):
            
            current_node.visited += 1
            current_node.parent.children[current_node]["n(s, a)"] += 1
            
            if(winner == 1):
                current_node.parent.children[current_node]["q(s, a)"] += 1
            else:
                current_node.parent.children[current_node]["q(s, a)"] += -1
            
            current_node = current_node.parent
            
        current_node.visited += 1
           
    
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        