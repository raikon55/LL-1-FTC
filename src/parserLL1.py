#!/usr/bin/env python

import re
import string
import sys
import os

"""
TODO: Criar um parser LL(1)
    - Desenvolver FOLLOW
    - Gerar tabela LL(1)
"""
def first(var: str, productions: dict) -> list:
    firstSet = set()
    i = 0

    if var.islower():       # Terminal
        firstSet.add(var)

    elif var == "@":        # Lambda
        firstSet.add(var)

    else:                   # First não-terminal
        for i in range(len(productions[var])):

            if productions[var][i][0].isupper():
                firstSet = first(productions[var][i][0], productions)

            elif productions[var][i].islower():

                if not productions[var][i].isalnum():
                    firstSet.add(re.split('[^a-z0-9]', productions[var][i])[0])

                else:
                    firstSet.add(productions[var][i])

            else:
                firstSet.add(productions[var][i][0])

    return firstSet

def follow(followDict: dict, var: str, productions: dict):
    nonTerm:str = ''
    if len(followDict) == 0:
        followDict.update({var : '$'})

    for i in range(len(productions[var])):

        for j in range(len(productions[var][i])):

            if productions[var][i][j] == var:
                if productions[var][i+1] != '@':
                    print(productions[var][i+1])
                if productions[var][i+1] != '@' and productions[var][i][0] != var:
                    follow(followDict, productions[var][i][0], productions)

    print(f'{var} -> {productions[var]}')
    print(followDict)

def getGrammar() -> dict:
    """
    Criar dicionário com as produções da linguagem
    """
    productions = {}

    with open(sys.argv[1]) as file:
        grammar = file.read()

        for lines in grammar.splitlines():
            line = re.split(r'((->)|(\|)|( ))', lines)

            var = line[0]
            line.remove(var)

            i = 0
            while i < len(trash):
                if line.count(trash[i]) > 0:
                    line.remove(trash[i])
                else:
                    i += 1

            productions.update({var: line})

    return productions

def removeRecursion(productions: dict):
    """
    Remove recursão a esquerda para possibilitar a criação da tabela
    """
    derivative = "'"
    newProduction = []
    newVar = ''
    tempDict = productions.copy()

    for var in tempDict.keys():
        tempDict[var] = productions[var].copy()

        for i in range(len(tempDict[var])):
            newVar = var + derivative

            if len(tempDict[var][i]) > 1:
                if var == tempDict[var][i][0]:
                    newProduction.append(tempDict[var][i].replace(var, '') + newVar)
                    productions[var].remove(tempDict[var][i])

            elif tempDict[var][i].isupper():
                productions[var].remove(tempDict[var][i])
                productions[var].append(tempDict[var][i] + newVar)

        if len(newProduction) != 0: 
            productions.update({newVar : newProduction.copy()})

        newProduction.clear()

def removeFactorization(productions: dict):
    """
    Remove fatoração a esquerda das regras
    """
    derivative = "'"
    newProduction = set()
    newVar = ''
    tempDict = productions.copy()

    for var in tempDict.keys():
        tempDict[var] = productions[var].copy()
        newVar = var + derivative

        for rule in tempDict[var]:
            for i in range(len(tempDict[var])):
                if rule in tempDict[var][i] and len(rule) != len(tempDict[var][i]):
                    newProduction.add(tempDict[var][i].replace(rule, ''))
                    newProduction.add('@')

    tempDict[var].append(rule + newVar)    
    tempDict.update({newVar: newProduction})

    newProduction.clear()

if __name__ == "__main__":
    trash = ['|', '->', ' ', '', None]
    grammar = []
    firstDict = {}
    followDict = {}
    productions = getGrammar()
    removeRecursion(productions)
    removeFactorization(productions)

    for i in productions.keys():
        firstDict.update({i : first(i, productions)})

    for var in productions.keys():
        follow(followDict, var, productions)