# Food Truck Selector
## Building
### Docker
Run `docker build -t msft-foodtrucks:latest .` from the checkout directory.
### Local Python
Create a virtual environment for development. On linux this would be `virtualenv .venv` for example.
Once that's complete, activate the environment and install the required packages.
Example from linux: ```virtualenv .venv
. ./.venv/bin/activate
pip install -r requirements.txt```
## Running
### Docker
Run `docker run msft-foodtrucks`
### Local Python
Run `python ./src/food_trucks.py`
