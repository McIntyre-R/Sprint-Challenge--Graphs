from room import Room
import random
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class World:
    def __init__(self):
        self.starting_room = None
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
    def load_graph(self, room_graph):
        num_rooms = len(room_graph)
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):
            x = room_graph[i][0][0]
            grid_size = max(grid_size, room_graph[i][0][0], room_graph[i][0][1])
            self.rooms[i] = Room(f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})",i, room_graph[i][0][0], room_graph[i][0][1])
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for i in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if 'n' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('n', self.rooms[room_graph[room_id][1]['n']])
            if 's' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('s', self.rooms[room_graph[room_id][1]['s']])
            if 'e' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('e', self.rooms[room_graph[room_id][1]['e']])
            if 'w' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('w', self.rooms[room_graph[room_id][1]['w']])
        self.starting_room = self.rooms[0]

    def print_rooms(self, visited):
        rotated_room_grid = []
        for i in range(0, len(self.room_grid)):
            rotated_room_grid.append([None] * len(self.room_grid))
        for i in range(len(self.room_grid)):
            for j in range(len(self.room_grid[0])):
                rotated_room_grid[len(self.room_grid[0]) - j - 1][i] = self.room_grid[i][j]
        print("#####")
        str = ""
        for row in rotated_room_grid:
            all_null = True
            for room in row:
                if room is not None:
                    all_null = False
                    break
            if all_null:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None and not room in visited:
                    str += f"{room.id}".zfill(3)
                elif room is not None and room in visited:
                    str += f"{bcolors.WARNING}{room.id}{bcolors.ENDC}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")


