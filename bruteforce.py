import csv
import time
from itertools import combinations
from typing import Callable, Tuple, List
from dataclasses import dataclass


@dataclass
class Action:
    """
    Class for keeping datas of an action\n
    name: str\n
    cost: float\n
    profit: float\n
    gains: float
    """
    name: str
    cost: float
    profit: float
    gains: float

    def __str__(self):
        return f"{self.name}"


@dataclass()
class Combination:
    """
    Class for checking the best combination of actions\n
    :param: actions: tuple\n
    max_cost: int\n
    best_costs: float (no mandatory)\n
    best_gains: float (no mandatory)\n
    best_actions: tuple (no mandatory)\n
    """
    actions: Tuple
    max_cost: int
    best_costs: float = 0.0
    best_gains: float = 0.0
    best_actions: Tuple = None

    def total_gains(self) -> float:
        """
        Calcul the total gains\n
        :return: The sum of total gains between several actions
        """
        return sum(float(action.gains) for action in self.actions)

    def total_costs(self) -> float:
        """
        Calcul the total costs\n
        :return: The sum of total costs between several actions
        """
        return sum(action.cost for action in self.actions)

    def check_best_gains(self) -> Tuple[float, float, tuple]:
        """
        Check if new gain is greater that actual gains\n
        :return: return the new cost, new gain and all actions
        """
        total_costs = self.total_costs()
        if total_costs < self.max_cost:
            total_gains = self.total_gains()
            if total_gains > self.best_gains:
                return total_costs, total_gains, self.actions
        return self.best_costs, self.best_gains, self.best_actions


def timing(function: Callable) -> Callable:
    """
    Get time of execution of  a function\n
    :param function: any function
    :return: Time of execution of a function
    """

    def wrapper(*args, **kwargs):
        start = int(round(time.time() * 1000))
        res = function(*args, **kwargs)
        print(f'Time algorithm: {int(round(time.time() * 1000)) - start}ms')
        return res

    return wrapper


def read_csv(filename: str) -> List[Action]:
    """
    A function which reads datas of csv file\n
    :param filename: A csv file
    :return: An objects list of type Action
    """
    datas = []
    with open(file=filename, newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            price = float(row['price'])
            if price > 0:
                profit = round(float(row['profit']) / 100, 2)
                gain = round(price * profit, 2)
                datas.append(Action(row['name'], price, profit, gain))
    return datas


def display(costs: float, gains: float, best_actions: Tuple[Action]) -> None:
    """
    Display information of actions with the total costs and gains
    :param costs: totals costs of best actions
    :param gains: totals gains of best action
    :param best_actions: information of best actions
    """
    print(f'Costs: {round(costs, 2)}€')
    print(f'Gains: {round(gains, 2)}€')
    print([action.name for action in best_actions])


def n_actions(dataset: List[Action], max_cost: int, reverse: bool = False) -> int:
    """
    Function for checking min actions and max actions with as max_costs
    :param dataset: List actions
    :param max_cost: Max costs possible
    :param reverse: Sort list ascendant (False) or descendant (True)
    :return: numbers of actions possible with max costs
    """
    total = 0
    i = 0
    dataset.sort(key=lambda x: x.cost, reverse=reverse)
    while i < len(dataset) - 1 and max_cost > 0:
        if max_cost - dataset[i].cost > 0:
            total += 1
            max_cost -= dataset[i].cost
        i += 1
    return total


@timing
def bruteforce(dataset: List[Action], max_cost: int) -> None:
    """
    Function for checking best actions with itertools combinations\n
    :param dataset: Objects list of type action
    :param max_cost: limit action costs
    """
    best_costs = 0.0
    best_gains = 0.0
    best_actions = None
    min_n = n_actions(dataset, 500, True)
    max_n = n_actions(dataset, 500)
    for n in range(min_n, max_n):
        for combination in combinations(dataset, n):
            best_costs, best_gains, best_actions = Combination(combination, max_cost, best_costs, best_gains,
                                                               best_actions).check_best_gains()
    display(best_costs, best_gains, best_actions)


if __name__ == '__main__':
    actions = read_csv('csv/actions.csv')
    bruteforce(actions, 500)
