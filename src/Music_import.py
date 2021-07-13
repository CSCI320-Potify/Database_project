from src.db_utils import *
import csv


def csv_import(filename):
    csv = os.path.join(os.path.dirname(__file__), f'../{path}')
    with open(csv, "r") as file:
        next(file)
        for line in csv.reader(file, delimiter=","):
            connection = connect()
            cursor = connection.cursor()
            song, artist, album, duration, genre, year = [item for item in line]