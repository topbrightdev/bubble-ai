import heapq

def a_star(start, goal):
    visited_set = list()
    fringe_set = [start]
    cameFrom = {}
    g_function = {}
    f_function = {}
    g_function[start] = 0
    f_function[start] = - zero_heuristic(start, goal)

    while len(fringe_set):
        current = heapq.heappop(fringe_set)
        path, size_path = reconstruct_path(cameFrom, current)
        if is_goal(start, current, size_path):
            return path, size_path
        elif current.dead_player:
            continue
        elif size_path >= 5:
            # TODO change
            continue
        # fringe_set.remove(current) # TODO pop delete automaticlly
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
            g_function[child_node] = tentative_g
            f_function[child_node] = - g_function[child_node] - zero_heuristic(child_node, goal) # TODO we need to do it with minus?

            child_path, child_size_path = reconstruct_path(cameFrom, child_node)
            if is_goal(start, child_node, child_size_path):
                return child_path, child_size_path
    # TODO we are here if every path is more then 5
    return path, size_path


def reconstruct_path(cameFrom, current):
    total_path = []
    while current in cameFrom.keys():
        total_path.insert(0, cameFrom[current][1])
        current = cameFrom[current][0]
    return total_path, len(total_path)


def zero_heuristic(start, goal):
    return 0


def is_goal(start, game, path_size):
    return is_score_added(start, game, path_size)
    # return is_max_path_size_reached(game, path_size)


def is_max_path_size_reached(game, path_size):
    if path_size >= 5:
        return True
    return False


def is_score_added(start, game, path_size):
    if game.get_score() - start.get_score() > 0:
        return True
    return False
