from bruteforce import read_csv, timing, Action, display


def total_costs(list_actions: list[Action]) -> float:
    """
    Calcul the total costs\n
    :return: The sum of total costs between several actions
    """
    return sum(float(action.cost) for action in list_actions)


def total_gains(list_actions: list[Action]) -> float:
    """
    Calcul the total costs\n
    :return: The sum of total costs between several actions
    """
    return sum(float(action.gains) for action in list_actions)


@timing
def glouton(max_cost: int, list_actions: list[Action]):
    costs = 0
    best_actions = []
    list_actions.sort(key=lambda x: x.profit, reverse=True)
    for action in list_actions:
        if action.cost + costs <= max_cost:
            costs += action.cost
            best_actions.append(action)
    display(total_costs(best_actions), total_gains(best_actions), tuple(best_actions))


if __name__ == '__main__':
    actions = read_csv('csv/dataset2_Python+P7.csv')
    glouton(500, actions)
