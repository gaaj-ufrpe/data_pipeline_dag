
from dagster import asset

@asset
def teste_1():
    return 1

@asset
def teste_2(teste_1):
    return 2+teste_1

@asset
def teste_3(teste_1):
    return 3+teste_1

@asset
def teste_4(teste_2,teste_3):
    return 4+teste_2+teste_3

