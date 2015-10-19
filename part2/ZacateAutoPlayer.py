# Automatic Zacate game player
# B551 Fall 2015
# PUT YOUR NAME AND USER ID HERE!
#
# Based on skeleton code by D. Crandall
#
# PUT YOUR REPORT HERE!
# In the problem of zakate it will be a tree with first level containing all the combinations of dices that user can hold
# The second level would contain all the possible outcome of dice thrown based on what user has chosen to hold.Similarly
# the next level ie 4th would contain all the possible hold user can do and level 5 would contain the possible outcome
# on the dice thrown. In my approach i traverse to 1st level and for each hold i sumed all the possible expected
# outcome for each possible hold user performs by multiplying probability for reaching that output with the best
# score possible at that level.For optimizing the code i tried to creat the matrix of probaility going from one state to
# another as follows. Now each row specifies going from one state to another and it probability
#1 0.2326 0.4093 0.2702 0.0792 0.0088
#2 0 0.3349 0.4421 0.1945 0.0285
#3 0 0 0.4823 0.4244 0.0934
#4 0 0 0 0.6944 0.3046
#5 0 0 0 0 1
#but i was not able to complete that approch so i limited to 1st level only.


# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#
import itertools

from ZacateState import Dice
from ZacateState import Scorecard
import random
import math
import numpy as np
from itertools import product


class ZacateAutoPlayer:
    def __init__(self):
        pass

    def first_roll(self, dice, scorecard):
        l = tuple(dice.dice)
        all_holds = self.get_all_hld(l)
        sum = {}
        i = 0
        global_max = 0;
        final_hold = []
        for hold in all_holds:
            temp_val = []
            temp_val.append(self.expected_value(hold, len(l) - len(hold)))
            s = 0
            for j in temp_val[0]:
                # p=self.separate(list(hold))
                # m=self.check_kind(p)
                # self.identity_matrix = self.matmult(self.probability_matrix, m)
                s += self.calculate_expected_val(hold, j, len(l) - len(hold), scorecard)

            if global_max < s:
                final_hold = list(hold)
        hld=[0,1,2,3,4,5]
        q=final_hold
        for i in range(0, len(list(l))):
            p=list(l)
            n=q.count(p[i])
            if(n>0):
                q.remove(p[i])
                hld[i]=-1
        final_hld=[]
        for k in range(0,len(hld)):
            if(hld[k]!=-1):
                final_hld.append(hld[k])

        return final_hld


    def calculate_total_sum(self, total_outcome, scorecard, l):
        summation = []
        bonus_sum = 0
        total_sum = 0
        counts = [total_outcome.count(i) for i in range(1, 7)]
        if "unos" not in scorecard.scorecard.keys():
            summation.append(1 * counts[0])
        else:
            bonus_sum += scorecard.scorecard["unos"]
        if "doses" not in scorecard.scorecard.keys():
            summation.append(2 * counts[1])
        else:
            bonus_sum += scorecard.scorecard["doses"]
        if "treses" not in scorecard.scorecard.keys():
            summation.append(3 * counts[2])

        else:
            bonus_sum += scorecard.scorecard["treses"]
        if "cuatros" not in scorecard.scorecard.keys():
            summation.append(4 * counts[3])

        else:
            bonus_sum += scorecard.scorecard["cuatros"]
        if "cincos" not in scorecard.scorecard.keys():
            summation.append(5 * counts[4])

        else:
            bonus_sum += scorecard.scorecard["cincos"]
        if "seises" not in scorecard.scorecard.keys():
            summation.append(6 * counts[5])
        else:
            bonus_sum += scorecard.scorecard["seises"]
            if(len(summation)>0):
                total_sum = max(summation)
        bonus_sum += total_sum
        if not (scorecard.bonusflag) and bonus_sum > 63:
            total_sum += 35
        summation = []
        if "pupusa de queso" not in scorecard.scorecard.keys() and (
                        sorted(total_outcome) == [1, 2, 3, 4, 5] or sorted(total_outcome) == [2, 3, 4, 5, 6]):
            summation.append(40)
        if "pupusa de frijol" not in scorecard.scorecard.keys() and (
                            len(set([1, 2, 3, 4]) - set(total_outcome)) == 0 or len(
                            set([2, 3, 4, 5]) - set(total_outcome)) == 0 or len(
                        set([3, 4, 5, 6]) - set(total_outcome)) == 0):
            summation.append(30)
        if "elote" not in scorecard.scorecard.keys() and (2 in counts) and (3 in counts):
            summation.append(25)
        if "triple" not in scorecard.scorecard.keys() and max(counts) >= 3:
            summation.append(sum(total_outcome))
        if "cuadruple" not in scorecard.scorecard.keys() and max(counts) >= 4:
            summation.append(sum(total_outcome))
        if "quintupulo" not in scorecard.scorecard.keys() and max(counts) == 5:
            summation.append(50)
        if "tamal" not in scorecard.scorecard.keys():
            summation.append(sum(total_outcome))

        if l == 0 and max(summation) > total_sum:
            return max(summation)
        elif l == 0 and max(summation) < total_sum:
            return total_sum

        if summation.__len__() > 0 and l > 0:
            #total_sum += max(summation)
            if total_sum < max(summation):
                total_sum=max(summation)

        return total_sum

    def calculate_expected_val(self, intial_hold, expected_out, num_free_dices, scorecard):
        total_combi = 1
        prob = 1.0
        for j in range(0, num_free_dices):
            total_combi *= 6
        prob = prob / 6;
        prob = prob ** num_free_dices
        p = list(itertools.permutations(expected_out))
        total_outcome = list(intial_hold) + expected_out
        total_outcome.sort()
        q = self.calculate_total_sum(total_outcome, scorecard, len(p))
        if (len(p) == 0):
            return q
        return ((p.__len__() / prob) * q)

    def second_roll(self, dice, scorecard):
        l = tuple(dice.dice)
        all_holds = self.get_all_hld(l)
        sum = {}
        i = 0
        global_max = 0;
        final_hold = []
        for hold in all_holds:
            temp_val = []
            temp_val.append(self.expected_value(hold, len(l) - len(hold)))
            s = 0.0
            for j in temp_val[0]:
                # p=self.separate(list(hold))
                # m=self.check_kind(p)
                # self.identity_matrix = self.matmult(self.probability_matrix, m)
                #all_holds = self.get_all_hld(list(hold)+j)
                s += self.calculate_expected_val(hold, j, len(l) - len(hold), scorecard)

            s= s / len(temp_val[0])
            if global_max < s:
                final_hold = hold
        hld=[0,1,2,3,4,5]
        q=list(final_hold)
        for i in range(0, len(list(l))):
            p=list(l)
            n=q.count(p[i])
            if(n>0):
                q.remove(p[i])
                hld[i]=-1
        final_hld=[]
        for k in range(0,len(hld)):
            if(hld[k]!=-1):
                final_hld.append(hld[k])

        return final_hld
         # always re-roll first die (blindly)  # always re-roll second and third dice (blindly)

    def third_roll(self, dice, scorecard):
        # stupidly just randomly choose a category to put this in
        summation = []
        bonus_sum = 0
        total_outcome=dice.dice
        counts = [total_outcome.count(i) for i in range(1, 7)]
        cat=""
        max_val=0
        if "unos" not in scorecard.scorecard.keys():
            l =1 * counts[0]
            if (max_val <l):
                max_val=l
                cat="unos"
        else:
            bonus_sum += scorecard.scorecard["unos"]
        if "doses" not in scorecard.scorecard.keys():
            l =1 * counts[1]
            if (max_val <l):
                max_val=l
                cat="doses"
        else:
            bonus_sum += scorecard.scorecard["doses"]
        if "treses" not in scorecard.scorecard.keys():
            l =1 * counts[2]
            if (max_val <l):
                max_val=l
                cat="treses"

        else:
            bonus_sum += scorecard.scorecard["treses"]
        if "cuatros" not in scorecard.scorecard.keys():
           l =1 * counts[3]
           if (max_val <l):
                max_val=l
                cat="cuatros"

        else:
            bonus_sum += scorecard.scorecard["cuatros"]
        if "cincos" not in scorecard.scorecard.keys():
            l =1 * counts[4]
            if (max_val <l):
                max_val=l
                cat="cincos"
        else:
            bonus_sum += scorecard.scorecard["cincos"]

        if "seises" not in scorecard.scorecard.keys():
            l =1 * counts[5]
            if (max_val <l):
                max_val=l
                cat="seises"
        else:
            bonus_sum += scorecard.scorecard["seises"]

        bonus_sum += max_val
        if not (scorecard.bonusflag) and bonus_sum > 63:
            return cat

        if "pupusa de queso" not in scorecard.scorecard.keys() and (
                        sorted(total_outcome) == [1, 2, 3, 4, 5] or sorted(total_outcome) == [2, 3, 4, 5, 6]):
            if (max_val <40):
                max_val=40
                cat="pupusa de queso"
        if "pupusa de frijol" not in scorecard.scorecard.keys() and (
                            len(set([1, 2, 3, 4]) - set(total_outcome)) == 0 or len(
                            set([2, 3, 4, 5]) - set(total_outcome)) == 0 or len(
                        set([3, 4, 5, 6]) - set(total_outcome)) == 0):
            if (max_val <30):
                max_val=30
                cat="pupusa de frijol"
        if "elote" not in scorecard.scorecard.keys() and (2 in counts) and (3 in counts):
            if (max_val <25):
                max_val=25
                cat="elote"
        if "triple" not in scorecard.scorecard.keys() and max(counts) >= 3:
            t=sum(total_outcome)
            if (max_val <t):
                max_val=t
                cat="triple"
        if "cuadruple" not in scorecard.scorecard.keys() and max(counts) >= 4:
            t=sum(total_outcome)
            if (max_val <t):
                max_val=t
                cat="cuadruple"
        if "quintupulo" not in scorecard.scorecard.keys() and max(counts) == 5:
            if (max_val <50):
                max_val=50
                cat="quintupulo"
        if "tamal" not in scorecard.scorecard.keys():
            t=sum(total_outcome)
            if (max_val <t):
                max_val=t
                cat="tamal"
        if cat=="":
            return "tamal"
        return cat

    def select(n, m):
        C = math.factorial(n) / (math.factorial(m) * math.factorial(n - m))
        return C

    def get_all_hld(self, hand):

        if len(hand) == 0:
            return set([()])

        h = list(hand)
        m = h.pop()
        prv_hlds = self.get_all_hld(tuple(h))
        hlds = set([()])
        for hold in prv_hlds:
            temp = list(hold)
            temp.append(m)
            hlds.add(tuple(temp))
        hlds.update(prv_hlds)
        return hlds

    def expected_value(self, hld, num_free_dice):
        t = set([])
        for p in product([1, 2, 3, 4, 5, 6], repeat=num_free_dice):
            p = list(p)  # + list(hld)
            p.sort()
            t.add(tuple(p))
        p = []
        for i in t:
            p.append(list(i))
        return p

    def separate(self, state):
        current_kind = None
        groups = [[]]
        for item in sorted(state):
            current_kind = current_kind or item
            is_equal = item == current_kind
            (groups, groups[-1])[is_equal].append(([item], item)[is_equal])
            current_kind = is_equal and current_kind or item
        return groups

    def check_kind(self, state):
        p = 1
        for group in state:
            l = len(group)
            if l == 2 and p == 3:
                p = 2
            elif l == 3 and p == 2:
                continue
            elif l > p:
                p = l
        if p == 5:
            return [[0], [0], [0], [0], [1]]
        elif p == 3:
            return [[0], [0], [1], [0], [0]]
        elif p == 2:
            return [[0], [1], [0], [0], [0]]
        elif p == 4:
            return [[0], [0], [0], [1], [0]]
        elif p == 1:
            return [[1], [0], [0], [0], [0]]

'''
d = Dice()
z = ZacateAutoPlayer()
s = Scorecard()
d.dice = sorted(d.roll())
which_to_reroll = z.first_roll(d, s)

l = tuple([1, 1, 3, 4, 5])
'''