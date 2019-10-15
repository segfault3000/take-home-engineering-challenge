FROM python:3

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY ./src/food_trucks.py /
COPY ./src/food_trucks_cli.py /

ENTRYPOINT [ "python", "/food_trucks_cli.py" ]
