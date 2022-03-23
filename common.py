import csv
import time
from typing import Callable
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


def read_csv(filename: str) -> list[Action]:
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


def display(costs: float, gains: float, best_actions: tuple[Action]) -> None:
    """
    Display information of actions with the total costs and gains
    :param costs: totals costs of best actions
    :param gains: totals gains of best action
    :param best_actions: information of best actions
    """
    print(f'Costs: {round(costs, 2)}€')
    print(f'Gains: {round(gains, 2)}€')
    print([action.name for action in best_actions])