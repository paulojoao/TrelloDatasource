#coding: utf-8
import unittest
import mock
from datetime import datetime, timedelta

from datasource import CardListDatasource
from trello import Board


class TestDatasource(unittest.TestCase):

    def test_parse_key_without_param(self):
        ds = CardListDatasource('','','','')
        key = '{duration}'
        rtn = ds.parse_key(key)
        expected = ('duration', None)
        self.assertEqual(rtn, expected)

    def test_parse_key_with_param(self):
        ds = CardListDatasource('','','','')
        key = '{duration[Done]}'
        rtn = ds.parse_key(key)
        expected = ('duration', 'Done')
        self.assertEqual(rtn, expected)

    @mock.patch('datasource.CardListDatasource.get_card_title')
    @mock.patch('datasource.CardListDatasource.get_card_members')
    @mock.patch('datasource.CardListDatasource.get_card_duration')
    def test_get_row(self, mk_duration, mk_members, mk_title):
        mk_duration.return_value = 'duration'
        mk_members.return_value = 'members'
        mk_title.return_value = 'title'

        keys = ['{title}', '{members}', '{duration[WIP]}']
        datasource = CardListDatasource('', '', '', '')
        card = mock.Mock()
        row = datasource.get_row(card, keys)
        kwargs = {
            'card': card,
            'column': 'WIP'
        }
        mk_duration.assert_called_with(**kwargs)
        del kwargs['column']
        mk_members.assert_called_with(**kwargs)
        mk_title.assert_called_with(**kwargs)

        expected = {
            '{title}': 'title',
            '{members}': 'members',
            '{duration[WIP]}': 'duration'
        }
        self.assertEqual(row, expected)

    @mock.patch('trello.TrelloClient.list_boards')
    def test_get_board(self, mk_list_boards):
        b1 = mock.Mock()
        b1.configure_mock(name='B1')
        b2 = mock.Mock()
        b2.configure_mock(name='B2')
        mk_list_boards.return_value = [b1, b2]
        datasource = CardListDatasource('','','','')
        board = datasource.get_board('B2')
        self.assertEqual(b2, board)

    @mock.patch('trello.TrelloClient.list_boards')
    def test_get_invalid_board(self, mk_list_boards):
        b1 = mock.Mock()
        b1.configure_mock(name='B1')
        b2 = mock.Mock()
        b2.configure_mock(name='B2')
        mk_list_boards.return_value = [b1, b2]
        datasource = CardListDatasource('','','','')
        board = datasource.get_board('B3')
        self.assertEqual(board, None)

    def test_get_cards(self):
        board = mock.Mock()
        board.all_cards.return_value = range(5)
        datasource = CardListDatasource('','','','')
        cards = datasource.get_cards(board)
        self.assertEqual(range(5), cards)

    def test_get_duration(self):
        card = mock.Mock()
        card.listCardMove_date.return_value = [
            [u'List 1', u'List 2', datetime(2015, 05, 03, 12, 00)],
            [u'List 2', u'List 3', datetime(2015, 05, 03, 13, 00)],
            [u'List 3', u'Done', datetime(2015, 05, 05, 0, 0)]
        ]
        datasource = CardListDatasource('','','','')
        expected = datetime(2015, 05, 05, 0, 0) - datetime(2015, 05, 03, 12, 00)
        rtn = datasource.get_card_duration(mock.Mock())
        self.assertEqual(rtn, expected)

if __name__ == '__main__':
    unittest.main()
