import click
from tabulate import tabulate
from food_trucks import FoodTrucks


@click.command()
@click.option('--count', '-c', default=20)
def suggest(count):
    ft = FoodTrucks()
    print(tabulate(ft.suggest(count)))

if __name__ == '__main__':
    suggest()

