import csv
import time
from itertools import combinations
from typing import Callable, Tuple
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
        return f"Name: {self.name} => Cost: {self.cost} => Profit: {self.profit} => Gains: {self.gains}"


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
        return sum(float(action.cost) for action in self.actions)

    def check_best_gains(self) -> Tuple[float, float, tuple]:
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
        print(f'Time bruteforce: {int(round(time.time() * 1000)) - start}ms')
        return res

    return wrapper


def read_csv(filename: str) -> list[Action]:
    """
    A function which reads datas of csv file\n
    :param filename: A csv file
    :return: An objects list of type Action
    """
    datas = []
    with open(file=filename, newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            datas.append(Action(row['name'], row['price'], row['profit'], row['gains']))
    return datas


def display(costs: float, gains: float, best_actions: Tuple) -> None:
    """
    Display information of actions with the total costs and gains\n
    :param costs: totals costs of best actions
    :param gains: totals gains of best actions
    :param best_actions: information of best actions
    """
    print(f'Costs: {round(costs, 2)}€')
    print(f'Gains: {round(gains, 2)}€')
    print('Description actions')
    for action in best_actions:
        print(action.__str__())


@timing
def bruteforce(dataset: list[Action], max_cost: int) -> None:
    """
    Function for checking best actions with itertools combinations\n
    :param dataset: Objects list of type action
    :param max_cost: limit action costs
    """
    best_costs = 0.0
    best_gains = 0.0
    best_actions = None
    for n in range(1, len(dataset) + 1):
        for combination in combinations(dataset, n):
            if n == 1:
                best_costs, best_gains, best_actions = Combination(combination, max_cost).check_best_gains()
            else:
                best_costs, best_gains, best_actions = Combination(combination, max_cost, best_costs, best_gains,
                                                                   best_actions).check_best_gains()
    display(best_costs, best_gains, best_actions)


if __name__ == '__main__':
    actions = read_csv('csv/actions.csv')
    bruteforce(actions, 500)
