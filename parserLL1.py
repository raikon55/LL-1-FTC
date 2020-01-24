import re
import string
import sys
import os

"""
TODO 1: Criar um parser LL(1)
    - Desenvolver FIRST
    - Desenvolver FOLLOW
    - Gerar tabela LL(1)

XXX:
    - grammar.txt: Gramática simples para testes rápidos 
    - grammar2.txt: Gramática maior, sem recursividade à esquerda e com
      produções-lambda
    - grammar3.txt: Recursividade à esquerda sem produções-lambda
"""
def first(var, productions):
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

    return list(firstSet)

def follow(followDict, firstDict, productions):
    for var in productions.keys():
        if len(followDict) == 0:
            followDict.update({var : '$'})
        
        for i in range(len(productions[var])):

            for j in range(len(productions[var][i])):

                if productions[var][i][j] in productions.keys():
                    nonTerm = productions[var][i][j]

                else:
                    continue

                if productions[var][i][j].isupper() and \
                    not set(firstDict[productions[var][i][j]]).issuperset({'@'}):
                   followDict.update({nonTerm: firstDict[productions[var][i][j+1]]})

                elif set(firstDict[productions[var][i][j]]).issuperset({'@'}):
                    try:
                        temp = firstDict[productions[var]] - {'@'}

                    except:
                        print("ERROR")

                    followDict.update({nonTerm: temp})
                    followDict.update({nonTerm: followDict[var]})

        print(f'{var} -> {productions[var]}')
    print(followDict)

def getGrammar():
    """
    Criar dicionário com as produções da linguagem
    """
    productions = dict()

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

def removeRecursion(productions):
    """
    Remover recursão a esquerda para ser possível criar a tabela
    """
    derivative = "'"
    newProduction = list()
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

def removeFactorization(productions):
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
    grammar = list()
    firstDict = dict()
    followDict = dict()
    productions = getGrammar()
    removeRecursion(productions)
    removeFactorization(productions)

    for i in productions.keys():
        firstDict.update({i : first(i, productions)})

    follow(followDict, firstDict, productions)