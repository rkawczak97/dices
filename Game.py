import pandas as pd
from Dices import *
from Player import *

class Game:
    def __init__(self, n_throws: int=3, rounds: int=6) -> None:
        self.language: str = input('[PL/EN]?: ').lower()
        self.lang_dict: dict[str, str] = pd.read_excel('src/language.xlsx', index_col='key')[self.language].to_dict()
        self.n_players: int = int(input(self.lang_dict['n_players']))
        self.n_throws: int = n_throws
        self.rounds: int = rounds
        self.dices: Dices = Dices()
        self.players: list[Player] = self.create_players()

    def create_players(self):
        players = list()
        for i in range(self.n_players):
            name = input(self.lang_dict['player_name'].format(i+1))
            players.append(Player(self.dices, name))
        return players
        
    def play(self):
        for _ in range(self.rounds):
            t = input(self.lang_dict['throw_dices'])
            if t.lower() == 'y':
                for p in self.players:
                    for t in range(1, self.n_throws+1):
                        self.dices.throw()
                        self.display_status(p, t)
                        if t != self.n_throws:
                            self.select_dices_to_keep(t)
                            if t != 1:
                                self.select_dices_to_return(t)  
                    self.display_score()
                    self.display_player_score(p)
                    self.select_score(p)
                    self.dices.reset()
            else:
                print(self.lang_dict['close_game'])
                break
            self.dices.reset()
        self.display_results()

    def select_dices_to_keep(self, throw: int):
        k = input(self.lang_dict['keep_dices'].format(throw, self.n_throws))
        if k != '':
            idx = [int(x)-1 for x in k.split()]
            self.dices.keep(idx)
    
    def select_dices_to_return(self, throw: int):
        k = input(self.lang_dict['return_dices'].format(throw, self.n_throws))
        if k != '':
            idx = [int(x)-1 for x in k.split()]
            self.dices.back(idx)
   
    def select_score(self, player: Player):
        s = int(input(self.lang_dict['choose_score']))
        if player.get_score()[s] == None:
            player.set_score(s, self.dices.get_score()[s])
        else:
            print(self.lang_dict['choose_again'])
            return self.select_score()

    def display_score(self):
        score = self.dices.get_score()
        print('-'*30)
        print('Score:'+' | ', end='')
        for k, v in score.items():
            if v == 0:
                score[k] = 'X'
            elif v > 0:
                score[k] = '+{}'.format(v)
            else:
                score[k] = str(v)
            print('{}: {} |'.format(k, score[k]), end=' ')
        print('\n', end='')

    def display_status(self, player: Player, throw: int):
        print('-'*30)
        print('({}/{}) {}'.format(throw, self.n_throws, player.get_name()))
        print('S: {} | T: {}'.format(self.dices.get_dices_side(), self.dices.get_dices_throw()))

    def display_player_score(self, player: Player):
        print('{}: | '.format(player.get_name()), end='')
        for k, v in player.get_score().items():
            if v == None:
                v = '  '    
            print('{}: {} |'.format(k, v), end=' ')
        print('\n', end='')
    
    def display_results(self):
        print('-'*30)
        print(self.lang_dict['final_results'])
        for player in self.players:
            self.display_player_score(player)
        # TODO