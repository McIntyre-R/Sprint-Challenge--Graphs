from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from queue import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map


player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
visited = set()
explored = {}
explored[player.current_room.id] = {e:'?' for e in player.current_room.get_exits()}
reverse_move = {'n':'s',"w":"e","s":"n","e":"w"}
movement = None
prev_room = None

traversal_path = []

# helper function to set back on track if ran out of options
def find(explored, start_id):
    # Set up checked set, and queue for bfs
    checked = set()
    unchecked = Queue()
    unchecked.put(([], start_id))

    # run until no rooms to check
    while not unchecked.empty():
        # retrieve path/room from unchecked
        path, room = unchecked.get()
        # check if we've found an unexplored room
        if room == '?':
            # return the path if we do
            return path
        # else if room isn't in checked
        elif room not in checked:
            # log room as checked
            checked.add(room)
            # iterate throught the room in our explored log
            for (move, room) in explored[room].items():
                # add each of its rooms to our queue
                unchecked.put(([*path, move], room))

# run until all rooms are visited
while len(visited) != len(room_graph):
    # Add current room to visited rooms
    visited.add(player.current_room.id)
    # Log current room for later use
    prev_room = player.current_room.id
    # gather list of unchecked rooms from current room
    options = [e for (e, k) in explored[player.current_room.id].items() if k == '?']
    # check if there's no current unchecked rooms
    if len(options) == 0:
        # run helper function to find closest unchecked room
        moves = find(explored, player.current_room.id)
        # if unable to find unchecked room break
        if moves is None:
            break
        # add path to unchecked room to traversal path
        traversal_path += moves
        # itrate through the list of moves to the unchecked room 
        for e in moves:
            movement = e
            prev_room = player.current_room.id
            player.travel(movement)

    # if there are unchecked rooms choose a random one and move there
    else:   
        movement = random.choice(options)
        traversal_path.append(movement)
        player.travel(movement)

    
    # add current room to explored dict if not already there
    if not player.current_room.id in explored:
        explored[player.current_room.id] = {e:'?' for e in player.current_room.get_exits()}
    # update explored to log rooms
    explored[prev_room][movement] = player.current_room.id
    explored[player.current_room.id][reverse_move[movement]] = prev_room
    





# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)


if len(visited_rooms) == len(room_graph):
    world.print_rooms(visited_rooms)
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    world.print_rooms(visited_rooms)
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
