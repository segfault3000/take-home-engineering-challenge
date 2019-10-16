import click
from tabulate import tabulate
from food_trucks import FoodTrucks


@click.command()
@click.option('--count', '-c', default=20)
@click.option('--location', '-l', default=None)
def suggest(count, location):
    ft = FoodTrucks()
    sugg = ft.suggest(location, count)

    print(tabulate(sugg, headers="keys", showindex="never"))

if __name__ == '__main__':
    suggest()

