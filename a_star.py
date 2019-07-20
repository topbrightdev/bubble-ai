import heapq

def a_star(start, goal, heuristic):
    visited_set = set()
    fringe_set = [start]
    cameFrom = {}

    path_size = 0
    starting_score = start.get_score()
    start.update_g_function(0)
    start.update_f_function(heuristic(start, starting_score, path_size))

    while len(fringe_set):
        current = heapq.heappop(fringe_set)
        path, path_size = reconstruct_path(cameFrom, current)
        if len(visited_set) == 500 or path_size >= 10:
            return path, path_size
        # elif path_size >= 5:
        #     # TODO change
        #     continue
        visited_set.add(current)

        list_of_childs = current.get_successors()

        for child in list_of_childs:
            child_node, child_action = child
            if child_node.dead_player:
                continue
            elif child_node in visited_set:
                continue # Ignore the childs which is already evaluated
            tentative_g = 0 #TODO change

            if child_node not in fringe_set:
                fringe_set.append(child_node)
                # TODO we need to check if we get the same state from two or more other ways?
            # TODO return this lines when g score mean something
            # elif tentative_g <= child_node.get_g_score(): # if we already discovered in this node
            #     continue

            # This path is the best until now
            cameFrom[child_node] = [current, child_action]
            child_path, child_path_size = reconstruct_path(cameFrom, child_node)

            # TODO notice that we take negative value, and use min heap
            child_node.update_g_function(-tentative_g)
            child_node.update_f_function(child_node.get_g_score() + heuristic(child_node, starting_score, child_path_size))

    # TODO we are here if every path is more then 5, and then take the last (random) path we checked
    return path, path_size


def reconstruct_path(cameFrom, current):
    total_path = []
    while current in cameFrom.keys():
        total_path.insert(0, cameFrom[current][1])
        current = cameFrom[current][0]
    return total_path, len(total_path)


def zero_heuristic(current, goal, path_size):
    return 0


def is_goal_heuristic(game, starting_score, path_size):
    if is_goal(game, starting_score, path_size):
        return -1000
    return 0


def is_max_path_size_reached(game, path_size):
    if path_size >= 5:
        return True
    return False


def is_goal(game, starting_score, path_size):
    return check_if_goal_by_score(game, starting_score)


def check_if_goal_by_score(game, starting_score):
    return (game.get_score() > starting_score)
