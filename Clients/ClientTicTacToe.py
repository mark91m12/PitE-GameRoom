#ClientTicTacToe
#Authors Mario Carricato & Marco Amato

import json
import os
from TicTacToe.Grid import Grid
from Clients.FactoryClient import AbstractClient
from Utility.Common import *
from Utility import Common


class ClientTicTacToe(AbstractClient):
    def __init__(self):
        self.client_socket = None
        self.grid = Grid()
        self.type_of_client = GamesType.TicTacToe.value

    def get_type_of_client(self):
        return self.type_of_client

    def set_client_socket(self, client_socket):
        self.client_socket = client_socket

    def start_client(self):

        welcome_message = self.client_socket.recv(1024)
        print(welcome_message.decode())

        is_game_ended = False

        while not is_game_ended:

            response = self.client_socket.recv(1024)

            try:
                json_object = json.loads(response.decode())
                type_message = json_object.get("type")
                grid_list = json_object.get("grid")

                if type_message == MessageType.MOVE_REQUEST.value:

                    valid_input = False
                    os.system("clear")
                    self.grid.draw_grid(grid_list)
                    name = json_object.get("name")
                    message = json_object.get("message")
                    print("\n"+name + " " + message+"\n")

                    while not valid_input:
                        player_choice = input()
                        if int(player_choice) in [Common.LEFT, Common.RIGHT, Common.CENTER, Common.UP, Common.DOWN, Common.UP_LEFT_CORNER, Common.UP_RIGHT_CORNER, Common.DOWN_LEFT_CORNER, Common.DOWN_RIGHT_CORNER]:
                            valid_input = True
                            self.client_socket.send(player_choice.encode())
                        else:
                            os.system("clear")
                            self.grid.draw_grid(grid_list)
                            print("\nyou have inserted invalid input")
                            print("Try Again")

                elif type_message == MessageType.END_GAME.value:

                    os.system("clear")
                    self.grid.draw_grid(grid_list)
                    message = json_object.get("message")
                    print("\n"+message)
                    is_game_ended = True

                else:

                    os.system("clear")
                    self.grid.draw_grid(grid_list)
                    message = json_object.get("message")
                    print("\n" + message)

            except:
                print('Lost Connection..')
                break