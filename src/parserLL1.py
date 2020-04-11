#!/usr/bin/env python3

import os
import re
import string
import sys


"""
TODO: Criar um parser LL(1)
    - Desenvolver FOLLOW
    - Gerar tabela LL(1)
"""


def follow(var: str, productions: dict, followDict: dict):
    if len(var) != 1:
        return {}

    for key in productions:
        for value in productions[key]:
            found = value.find(var)

            if found != -1:
                if found == (len(value)-1):
                    if key != var:
                        if key in followDict:
                            temp = followDict[key]
                        else:
                            followDict = follow(key, productions, followDict)
                            temp = followDict[key]
                        followDict[var] = followDict[var].union(temp)

                else:
                    first_of_next = first(value[found+1:], productions)

                    if '@' in first_of_next:
                        if key != var:
                            if key in followDict:
                                temp = followDict[key]
                            else:
                                followDict = follow(
                                    key, productions, followDict)
                                temp = followDict[key]
                            followDict[var] = followDict[var].union(temp)
                            followDict[var] = followDict[var].union(
                                first_of_next) - {'@'}
                    else:
                        followDict[var] = followDict[var].union(first_of_next)

    print(f'{var} -> {productions[var]}')
    print(followDict)

    return followDict


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

<<<<<<< HEAD
=======
def follow(followDict: dict, var: str, productions: dict):
    if len(followDict) == 0:
        followDict.update({var: '$'})

    # for i in range(len(productions[var])):
    #     if var in productions[var][i]:
    #         temp = list(productions[var][i])
    #         test = temp.index(var)
    #         if test == (len(temp)-1):
    #             followDict[var].extend(
    #                 followDict[list(productions.keys())[0]])
    #         else:
    #             followDict[var].extend(
    #                 first(var, productions))

    print(f'{var} -> {productions[var]}')
    print(followDict)
>>>>>>> 8581972e7f16e7cb3b5af906dead16403ce7d902

def getGrammar() -> dict:
    """
    Criar dicionário com as produções da linguagem
    """
    productions = {}
    start = ""

    with open(sys.argv[1]) as file:
        grammar = file.read()

        for lines in grammar.splitlines():
            line = re.split(r'((->)|(\|)|( ))', lines)

            var = line[0]
            if len(start) == 0:
                start = var
            line.remove(var)

            i = 0
            while i < len(trash):
                if line.count(trash[i]) > 0:
                    line.remove(trash[i])
                else:
                    i += 1

            productions.update({var: line})

    return (start, productions)


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
                    newProduction.append(
                        tempDict[var][i].replace(var, '') + newVar)
                    productions[var].remove(tempDict[var][i])

            elif tempDict[var][i].isupper():
                productions[var].remove(tempDict[var][i])
                productions[var].append(tempDict[var][i] + newVar)

        if len(newProduction) != 0:
            productions.update({newVar: newProduction.copy()})

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
    start, productions = getGrammar()
    removeRecursion(productions)
    removeFactorization(productions)

    for i in productions.keys():
<<<<<<< HEAD
        firstDict.update({i: first(i, productions)})

    followDict.update({start: '$'})
    for var in productions.keys():
        followDict = follow(var, productions, followDict)

    print(f"{firstDict}\n{followDict}")
=======
        firstDict.update({i : first(i, productions)})
>>>>>>> 8581972e7f16e7cb3b5af906dead16403ce7d902
