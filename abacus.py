#!/usr/bin/env python3

import random
import datetime
import argparse


def cmd_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    parser_times_table = subparsers.add_parser("timestable",
                                               help="Times table")
    parser_times_table.add_argument("tables",
                                    nargs="+",
                                    help="List of tables for practice")
    parser_times_table.add_argument("-r, --random",
                                    dest="do_random",
                                    action="store_true",
                                    help="Randomize the sequence in times \
                                    table")

    parser_mult = subparsers.add_parser("mult",
                                        help="Multiple questions")
    parser_mult.add_argument("maxVal",
                             nargs="+",
                             type=int,
                             help="Maxium value of arguments")
    parser_mult.add_argument("--questions",
                             type=int,
                             dest="questions",
                             default=30,
                             help="Number of questions")
    parser_mult.add_argument("--operands",
                             type=int,
                             dest="operands",
                             default=2,
                             help="Number of operands")
    parser_plus = subparsers.add_parser("plus",
                                        help="Plus and Minus")
    parser_plus.add_argument("--questions",
                             type=int,
                             dest="questions",
                             default=30,
                             help="Number of questions")
    parser_plus.add_argument("--operands",
                             type=int,
                             dest="operands",
                             default=5,
                             help="Number of operands")
    args = parser.parse_args()
    return args


def gen_questions(num_operands, max_operand=100):
    """
    Generate abacus question with given number of operands
    """
    operand = 0
    sum = 0
    tmp_sum = 0
    questions = {"operands": [],
                 "result": []}

    for i in range(num_operands):
        operandGet = False
        while (not operandGet):
            operand = random.randint(-max_operand+1, max_operand-1)
            tmp_sum = sum + operand
            if tmp_sum >= 0:
                operandGet = True
                questions["operands"].append(operand)
                sum = tmp_sum
    questions["result"] = sum
    return questions


def print_operands(operands):
    """
    Print the operands in formula format
    """
    for i in range(len(operands)):
        if (i == 0):
            print(operands[i], end="")
        else:
            if (operands[i] >= 0):
                print(" + ", end="")
                print(operands[i], end="")
            else:
                print(" - ", end="")
                print(-operands[i], end="")
    print(" = ")


def repr_operands(operands):
    """
    Covert the operands to formula format
    """
    rslt = []
    for i in range(len(operands)):
        if (i == 0):
            rslt.append("{0:>2}".format(operands[i]))
        else:
            if (operands[i] >= 0):
                rslt.append("+ {0:>2}".format(operands[i]))
            else:
                rslt.append("- {0:>2}".format(-operands[i]))
    rslt.append("= ")
    return " ".join(rslt)


def generate_table(strTable):
    """
    Generate table list from give table stings
    """
    timesTable = []
    for t in strTable:
        if '-' in t:
            items = t.split('-')
            timesTable += [x for x in range(int(items[0]), int(items[1])+1)]
        else:
            timesTable.append(int(t))

    return timesTable


def timestable_questions(tables, do_random=False):
    """
    Generate questions for multiple
    """

    baseTable = [x for x in range(1, 13)]

    questions = []

    for t in tables:
        for a in baseTable:
            questions.append((a, t))

    if do_random:
        random.shuffle(questions)

    for a, b in questions:
        correct = False
        while not correct:
            ans = input("{} x {} = ".format(a, b))
            try:
                iAns = int(ans)
                if (iAns == a * b):
                    correct = True
                else:
                    print("The answer is wrong, try again")
            except:
                print("Can't understand what do you mean, try it again")


def ShowReport():
    """
    Display report
    """
    pass


def genMultQuestions(max_vals, numQuestions=10, numOperands=2):
    """
    Generate multiple questions.
    """
    questions = []
    maxVal = 10

    shiftCnt = 0
    
    for q in range(numQuestions):
        multOps = {"ops": [],
                   "rslt": 1}
        rslt = 1
        for i in range(numOperands):
            if max_vals[i]:
                maxVal = max_vals[i]
            else:
                maxVal = 10
            operand = random.randint(1, maxVal-1)
            rslt *= operand
            multOps["ops"].append(operand)
        multOps["rslt"] = rslt
        questions.append(multOps)
        shiftCnt += 1
        if shiftCnt == numQuestions / numOperands:
            shiftCnt = 0
            max_vals = max_vals[1:] + max_vals[:1]

    return questions


def doMultQuestions(questions):
    numWrongAnswer = 0
    for question in questions:
        operands = [str(x) for x in question["ops"]]
        isCorrect = False
        while not isCorrect:
            ans = input("{} = ".format(" * ".join(operands)))
            if ans.isdecimal():
                if int(ans) == question["rslt"]:
                    isCorrect = True
                    
            if not isCorrect:
                numWrongAnswer += 1
                print("The answer is wrong, try again")
    return numWrongAnswer


def main():
    """
    Main function
    """
    args = cmd_parser()

    startTime = datetime.datetime.now()

    numWrongAnswer = 0
    numQuestions = args.questions
    
    # Execute Commands
    if args.cmd == "timestable":
        tables = generate_table(args.tables)
        numQuestions = len(tables) * 12
        timestable_questions(tables, args.do_random)
    elif args.cmd == "plus":
        num_questions = args.questions
        num_operands = args.operands

        for i in range(num_questions):
            questions = gen_questions(num_operands)
            correct = False
            while not correct:
                ans = input(repr_operands(questions["operands"]))
                if (ans.isdecimal()):
                    if (int(ans) == questions["result"]):
                        correct = True
                if (not correct):
                    numWrongAnswer += 1
                    print("The answer is wrong, try again")

    elif args.cmd == "mult":
        questions = genMultQuestions(args.maxVal,
                                     args.questions,
                                     args.operands)
        numWrongAnswer = doMultQuestions(questions)

    endTime = datetime.datetime.now()

    print("Score: {} : {}".format(numQuestions, numWrongAnswer))
    print("Total time:", endTime - startTime)
    ShowReport()


if __name__ == '__main__':
    main()
