from bruteforce import read_csv, timing, Action, display


def total_costs(list_actions: list[Action]) -> float:
    """
    Calcul the total costs
    :return: The sum of total costs between several actions
    """
    return sum(float(action.cost) for action in list_actions)


def total_gains(list_actions: list[Action]) -> float:
    """
    Calcul the total costs
    :return: The sum of total costs between several actions
    """
    return sum(float(action.gains) for action in list_actions)


def find_actions(max_cost: int, list_actions: list[Action], tab: list[list[int]]):
    w = max_cost
    n = len(list_actions)
    best_actions = []

    while w >= 0 and n >= 0:
        e = list_actions[n - 1]
        if tab[n][w] == tab[n - 1][w - int(e.cost)] + e.gains:
            best_actions.append(e)
            w -= int(e.cost)
        n -= 1
    for action in best_actions:
        action.cost /= 100
    display(total_costs(best_actions), total_gains(best_actions), tuple(best_actions))


def prepare_data(list_actions: list[Action]):
    for action in list_actions:
        action.cost *= 100
    return list_actions


@timing
def backpack(max_cost: int, list_actions: list[Action]):
    max_cost *= 100
    tab = [[0 for _ in range(max_cost + 1)] for _ in range(len(list_actions) + 1)]
    list_actions = prepare_data(list_actions)
    for i in range(1, len(list_actions) + 1):
        for w in range(1, max_cost + 1):
            if list_actions[i - 1].cost < w:
                tab[i][w] = max(list_actions[i - 1].gains +
                                tab[i - 1][int(w - list_actions[i - 1].cost)], tab[i - 1][w])
            else:
                tab[i][w] = tab[i - 1][w]
    find_actions(max_cost, list_actions, tab)


if __name__ == '__main__':
    actions = read_csv('csv/dataset2_Python+P7.csv')
    backpack(500, actions)
