import enum
import random
import math

class GridCell(enum.Enum):
    E = 0
    X = 1
    O = 2


class Outcome(enum.Enum):
    Xwin = 765
    Owin = 766
    Tie = 767


class Rank(enum.Enum):
    Best = 0
    Worst = 1


class Pair:
    def __init__(self, result, bestStrategy):
        self.bestStrategy = bestStrategy
        self.result = result


class Agent:

    def __init__(self):
        self.InputFile = "base_matrix"
        self.BoardSize = 9
        self.IndividualSize = 765
        self.PopulationSize = 50
        self.CrossoverChance = 0.95
        self.MutationChance = 0.03
        self.GenerationsCount = 100
        self.baseStateMatrix = []
        for z in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    for l in range(0, 3):
                        for m in range(0, 3):
                            for n in range(0, 3):
                                for p in range(0, 3):
                                    for q in range(0, 3):
                                        for r in range(0, 3):
                                            level = 0
                                            temp = [GridCell(z), GridCell(j), GridCell(k), GridCell(l), GridCell(m), GridCell(n), GridCell(p), GridCell(q), GridCell(r)]
                                            for idx in range(len(temp)):
                                                if temp[idx] != GridCell.E:
                                                    level += 1
                                            if self.stateIsAcceptable(temp):
                                                temp = self.getBaseCaseMatrix(temp)
                                                temp.append(level)
                                                flag = False
                                                for x in self.baseStateMatrix:
                                                    flag = True
                                                    for s in range(len(x)):
                                                        if x[s] != temp[s]:
                                                            flag = False
                                                            break
                                                    if flag:
                                                        break

                                                if not flag:
                                                    self.baseStateMatrix.append(temp)



        self.sortEnum(self.baseStateMatrix)
        self.Population = []
        for i in range(self.PopulationSize):
            Individuals = []
            for s in range(self.IndividualSize):
                cureState = self.baseStateMatrix[s]
                Individuals.append(self.nextMove(cureState))

            self.Population.append(Individuals)

    def sortEnum(self, list):
        for i in range(len(list)):
            for j in range(i + 1, len(list)):
                if list[j] == GridCell.O and list[i] != GridCell.O:
                    temp = list[j]
                    list[j] = list[i]
                    list[i] = temp

                elif list[j] == GridCell.X and list[i] == GridCell.E:
                    temp = list[j]
                    list[j] = list[i]
                    list[i] = temp


    def lexicographicalCompare(self, board1, board2):
        for i in range(9):
            if board1[i] == GridCell.O and board2[i] != GridCell.O:
                return True

            elif board1[i] == GridCell.X and board2[i] == GridCell.E:
                return True

            elif board2[i] == GridCell.O and board1[i] != GridCell.O:
                return False

            elif board2[i] == GridCell.X and board1[i] == GridCell.E:
                return False

        return True

    def hasPriority(self, board1, board2):
        sumX1 = 0
        sumO1 = 0
        sumX2 = 0
        sumO2 = 0
        mulX1 = 1
        mulO1 = 1
        mulX2 = 1
        mulO2 = 1
        for i in range(9):
            sumX1 += i * (board1[i] == GridCell.X)
            sumX2 += i * (board2[i] == GridCell.X)
            sumO1 += i * (board1[i] == GridCell.O)
            sumO2 += i * (board2[i] == GridCell.O)
            mulX1 *= i * (board1[i] == GridCell.X)
            mulX2 *= i * (board2[i] == GridCell.X)
            mulO1 *= i * (board1[i] == GridCell.O)
            mulO2 *= i * (board2[i] == GridCell.O)

        if sumX1 == sumX2:
            if sumO1 == sumO2:
                if mulX1 == mulX2:
                    if mulO1 == mulO2:
                        return self.lexicographicalCompare(board1, board2)
                    else:
                        return mulO1 < mulO2
                else:
                    return mulX1 < mulX2
            else:
                return sumO1 < sumO2
        else:
            return sumX1 < sumX2

    def isWinner(self, board, player):
        if board[0] == player and board[0] == board [1] and board[1] == board [2]:
            return True
        elif board[3] == player and board[3] == board [4] and board[4] == board [5]:
            return True
        elif board[6] == player and board[6] == board [7] and board[7] == board [8]:
            return True
        elif board[0] == player and board[0] == board [4] and board[4] == board [8]:
            return True
        elif board[2] == player and board[2] == board [4] and board[4] == board [6]:
            return True
        elif board[0] == player and board[0] == board [3] and board[3] == board [6]:
            return True
        elif board[1] == player and board[1] == board [4] and board[4] == board [7]:
            return True
        elif board[2] == player and board[2] == board [5] and board[5] == board [8]:
            return True
        else:
            return False

    def stateIsAcceptable(self, board):
        xCount = 0
        oCount = 0
        for i in range(len(board)):
            if board[i] == GridCell.X:
                xCount += 1
            elif board[i] == GridCell.O:
                oCount += 1
        if xCount == oCount or xCount == oCount + 1:
            if not self.isWinner(board, GridCell.X) and not self.isWinner(board, GridCell.O):
                return True
            elif not self.isWinner(board, GridCell.X) and self.isWinner(board, GridCell.O) and oCount == xCount:
                return True
            elif self.isWinner(board, GridCell.X) and not self.isWinner(board, GridCell.O) and xCount == oCount + 1:
                return True
            else:
                return False
        else:
            return False

    def getBaseCaseMatrix(self, state):

        states = [
            [state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7], state[8]],
            [state[6], state[3], state[0], state[7], state[4], state[1], state[8], state[5], state[2]],
            [state[8], state[7], state[6], state[5], state[4], state[3], state[2], state[1], state[0]],
            [state[2], state[5], state[8], state[1], state[4], state[7], state[0], state[3], state[6]],
            [state[6], state[7], state[8], state[3], state[4], state[5], state[0], state[1], state[2]],
            [state[8], state[5], state[2], state[7], state[4], state[1], state[6], state[3], state[0]],
            [state[2], state[1], state[0], state[5], state[4], state[3], state[8], state[7], state[6]],
            [state[0], state[3], state[6], state[1], state[4], state[7], state[2], state[5], state[8]]
        ]
        baseState = 0
        for i in range (len(states)):
            if self.hasPriority(states[i], states[baseState]):
                baseState = i

        return states[baseState]

    def play(self, player1, player2):
        step = 0
        state = []

        while True:

            if player1[step] != Outcome.Xwin and player1[step] != Outcome.Owin and player1[step] != Outcome.Tie:
                if player1[step] < self.IndividualSize:
                    state = self.baseStateMatrix[player1[step]]
                    step = player1[step]

            else:
                return Outcome(player1[step])

            if player2[step] != Outcome.Xwin and player2[step] != Outcome.Owin and player2[step] != Outcome.Tie:
                if player2[step] < self.IndividualSize:
                    state = self.baseStateMatrix[player2[step]]
                    step = player2[step]

            else:
                return Outcome(player2[step])

    def nextMove(self, cureState):
        diff = 0
        empty = 0
        for b in range(self.BoardSize):
            if cureState[b] == GridCell.X:
                diff += 1

            elif cureState[b] == GridCell.O:
                diff -= 1

            elif cureState[b] == GridCell.E:
                empty += 1

        if self.isWinner(cureState, GridCell.X):
            return Outcome.Xwin

        elif self.isWinner(cureState, GridCell.O):
            return Outcome.Owin

        elif empty == 0:
            return Outcome.Tie

        else:
            nextLevel = cureState[9] + 1
            possibleStates = set()
            for i in range(self.BoardSize):
                tempBoard = cureState[0:9]
                if tempBoard[i] == GridCell.E:
                    tempBoard[i] = GridCell(diff + 1)
                    tempBoard[0:9] = self.getBaseCaseMatrix(tempBoard[0:9])
                    tempBoard.append(nextLevel)
                    index = self.baseStateMatrix.index(tempBoard)
                    if index != self.IndividualSize:
                        possibleStates.add(index)

            step = random.randint(0, len(possibleStates) - 1)
            return list(possibleStates)[step]

    def fitness(self, candidate):
        loseCount = 0
        for i in range(len(self.Population)):
            player = self.Population[i]
            result = self.play(player, candidate)
            if result == Outcome.Owin:
                loseCount += 1

            result = self.play(candidate, player)
            if result == Outcome.Xwin:
                loseCount += 1
        f = loseCount / (2 * len(self.Population))
        return f

    def choose(self, rank):
        if rank == Rank.Best:
            result = self.PopulationSize * 2.0
        else:
            result = 0.0
        bestStrategy = 0

        for i in range(len(self.Population)):
            f = self.fitness(self.Population[i])

            if rank == Rank.Best:
                if f < result:
                    result = f
                    bestStrategy = i

            else:
                if f > result:
                    result = f
                    bestStrategy = i

        return Pair(result, bestStrategy)

    def selection(self):
        candidates = []
        for i in  range(int(len(self.Population)/2)):
            index = random.randint(0, len(self.Population) - 1)
            c = Pair(self.fitness(self.Population[index]), self.Population[index])
            candidates.append(c)
        candidates.sort(key=lambda x: x.result)
        #return Pair(candidates[0].bestStrategy, candidates[1].bestStrategy)
        returnValue = []
        for i in range(5):
            returnValue.append(candidates[i].bestStrategy)
        return returnValue

    def crossover(self, individuals):
        for i in range(len(individuals)):
            r = random.uniform(0, 1)
            if r < self.CrossoverChance:
                p1 = random.randint(0, len(individuals) - 1)
                p2 = random.randint(0, len(individuals) - 1)
                rand1 = random.randint(0, len(individuals[p1]))
                rand2 = random.randint(0, len(individuals[p2]))
                cutpoint1 = min(rand1, rand2)
                cutpoint2 = max(rand1, rand2)
                for i in range(cutpoint1, cutpoint2):
                    temp = individuals[p1][i]
                    individuals[p1][i] = individuals[p2][i]
                    individuals[p2][i] = temp

        return individuals

    def mutation(self, individuals):
        r = random.uniform(0, 1)
        if r < self.MutationChance:
            index = random.randint(0, len(individuals))
            state = self.baseStateMatrix[index]
            nxtMove = self.nextMove(state)
            individuals[index] = nxtMove

        return individuals


agent = Agent()
for i in range(agent.GenerationsCount):
    p = agent.selection()
    c = agent.crossover(p)
    for j in range(len(c)):
        agent.Population[agent.choose(Rank.Worst).bestStrategy] = c[j]
    for k in range(len(p)):
        agent.Population[agent.choose(Rank.Worst).bestStrategy] = p[k]
    for l in range(len(agent.Population)):
        agent.mutation(agent.Population[l])

result = agent.choose(Rank.Best)
print("The Percentage of Lost Games is = ", result.result * 100)
print("The Strategy is :")
bestAnswer = agent.Population[result.bestStrategy]
for i in range(len(bestAnswer)):
    print(i, " --> ", bestAnswer[i])

print()
