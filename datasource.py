#coding: utf-8
from trello import TrelloClient
from trello import Card
import re
'''
    Trello datasource
    Available metrics:
    
    {title} <- Title card
    {members} <- Card members
    {members[column]} <- Card members in column
    {duration} <- all duration in card
    {duration[column]} <- duraration of card in column
'''


class CardListDatasource(object):
    '''

    '''
    METHODS = {
        'title': 'get_card_title',
        'members': 'get_card_members',
        'duration': 'get_card_duration'
    }

    def __init__(self, api_key, api_secret, token_key, token_secret):
        self.client = TrelloClient(api_key, api_secret, token_key, token_secret)

    def get_board(self, board_name):
        '''
            Return board by name
        '''
        boards = self.client.list_boards()
        for board in boards:
            if board.name == board_name:
                return board
        return None

    def get_cards(self, board):
        return board.all_cards()

    def parse_key(self, key):
        key = key[1:-1] # remove {}
        method = key.split('[')[0]
        try:
            param = re.match(r"[^[]*\[([^]]*)\]", key).groups()[0]
        except AttributeError:
            param = None
        return (method, param)

    def get_row(self, card, keys):
        row = {}
        for key in keys:
            parsed_key = self.parse_key(key)
            method = parsed_key[0]
            column = parsed_key[1]
            kwargs = {
                'card' : card
            }
            if column:
                kwargs['column'] = column
            value = getattr(self, self.METHODS[method])(**kwargs)
            row[key] = value
        return row
        
    def get_card_duration(self, card, column=None):
        '''
            Return card duration, with called column arg
            return card duration inside column
        '''
        history = card.listCardMove_date()
        pass

