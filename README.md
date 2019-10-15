# Food Truck Selector
Geosearch for food trucks near your location!
This app will display a list of "local" food trucks with active permits.
The actual location of the food truck may vary as there are many permits requested
for any given food truck, but the list should be enough to venture out for food.

## Running
### Docker
Run `docker run msft-foodtrucks`
### Local Python
You must follow the steps for Building first as this requires a functional python environment.
```. ./.venv/bin/activate
python ./src/food_trucks_cli.py
```

## Building
### Docker
Run `docker build -t msft-foodtrucks:latest .` from the checkout directory.
### Local Python
Create a virtual environment for development. On linux this would be `virtualenv .venv` for example.
Once that's complete, activate the environment and install the required packages.
Example from linux: 
```virtualenv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

## Testing
### Local Python
You must follow the steps for Building first as this requires a functional python environment.
```. ./.venv/bin/activate
python ./src/food_trucks_tests.py
```
