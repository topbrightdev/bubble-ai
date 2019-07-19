import heapq

def a_star(start, goal):
    visited_set = list()
    fringe_set = [start]
    cameFrom = {}
    g_function = {}
    f_function = {}

    start.update_g_function(0)
    path_size = 0
    starting_score = start.get_score()
    start.update_f_function(is_goal_heuristic(start, starting_score, path_size))
    # g_function[start] = 0
    # f_function[start] = - zero_heuristic(start, goal)

    while len(fringe_set):
        current = heapq.heappop(fringe_set)
        path, path_size = reconstruct_path(cameFrom, current)
        if is_goal(current, starting_score, path_size):
            return path, path_size
        elif current.dead_player:
            continue
        elif path_size >= 5:
            # TODO change
            continue
        # fringe_set.remove(current) # pop delete automaticlly
        visited_set.append(current)

        list_of_childs = current.get_successors()

        for child in list_of_childs:
            child_node, child_action = child
            if child_node in visited_set:
                continue # Ignore the childs which is already evaluated
            tentative_g = child_node.get_score()

            if child_node not in fringe_set:
                fringe_set.append(child_node)
                # TODO we need to check if we get the same state from two or more other ways?
            elif tentative_g <= g_function[child_node]: # if we already discovered in this node
                continue

            # This path is the best until now
            cameFrom[child_node] = [current, child_action]
            child_path, child_path_size = reconstruct_path(cameFrom, child_node)

            # TODO notice that we take negative value, and use min heap
            child_node.update_g_function(-tentative_g)
            child_node.update_f_function(child_node.get_g_score() + is_goal_heuristic(child_node, starting_score, child_path_size))
            # g_function[child_node] = tentative_g
            # f_function[child_node] = - g_function[child_node] - zero_heuristic(child_node, goal) # TODO we need to do it with minus?

    # TODO we are here if every path is more then 5
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
