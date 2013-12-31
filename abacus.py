#!/usr/bin/env python3

import logging
import random
import datetime
import argparse


FILE_NAME = "abacus"


def cmd_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--questions",
                        type=int,
                        dest="questions",
                        default=10,
                        help="Number of questions")
    parser.add_argument("--operands",
                        type=int,
                        dest="operands",
                        default=4,
                        help="Number of operands")
    parser.add_argument("--repeat",
                        action="store_true",
                        default=False,
                        dest="repeat",
                        help="Repeat the question with wrong answer until get it right")
    parser.add_argument("-l", "--log",
                        default="abacus.log",
                        dest="log_file",
                        help="Name of log file")
    parser.add_argument("--log-level",
                        default="warning",
                        dest="log_level",
                        help="Setup the logging level")

    parsed_args = parser.parse_args()
    return parsed_args


def gen_questions(num_operands, max_operand=100):
    """
    Generate abacus question with given number of operands
    """
#    operand = 0
    sum = 0
#    tmp_sum = 0
    operands = []

    for i in range(num_operands):
        get_operand = False
        while not get_operand:
            operand = random.randint(-sum, max_operand - 1)
            tmp_sum = sum + operand
            if tmp_sum in range(max_operand):
                get_operand = True
                operands.append(operand)
                sum = tmp_sum

    return operands, sum


def print_operands(operands):
    """
    Print the operands in formula format
    """
    for i in range(len(operands)):
        if i == 0:
            print(operands[i], end="")
        else:
            if operands[i] >= 0:
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
    rslt = ""
    for i in range(len(operands)):
        if i == 0:
            rslt = "{0:>2}".format(operands[i])
        else:
            if operands[i] >= 0:
                rslt += " + {0:>2}".format(operands[i])
            else:
                rslt += " - {0:>2}".format(-operands[i])
    rslt += " = "
    return rslt


if __name__ == '__main__':
    args = cmd_parser()

    # Setup logging level
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level %s!" % args.log_level.upper())

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filename="info.log")
    logging.basicConfig(level=logging.WARNING, filename="warning.log")
    logging.info("Test for logging")
    logging.warning("warning message for logging")
    logging.debug("debug message")

    num_questions = args.questions

    # Initialize a dictionary to store error numbers for each question
    errDict = dict()
    for i in range(1, num_questions+1):
        errDict[i] = 0

    not_repeat = not args.repeat
    num_operands = args.operands

    total_mark = 0
    wrong_ans = []

    logFileName = "wrong_questions.txt"
    log_fhd = open(logFileName, 'w')

    start_time = datetime.datetime.now()

    for i in range(num_questions):
        mark = 1
        operands, rslt = gen_questions(num_operands)
        correct = False
        while not correct:
            ans = input(repr_operands(operands))
            if ans.isdecimal():
                if int(ans) == rslt:
                    correct = True
                else:
                    errDict[i+1] += 1
                    log_fhd.write(repr_operands(operands))
                    log_fhd.write(ans.strip())
                    log_fhd.write("\t" + "[{0:>2d}]".format(rslt))
                    log_fhd.write("\n")
                    mark = 0
                    if not_repeat:
                        correct = True
                    else:
                        print("The answer is wrong, try again")
            else:
                print("Sorry, give me the answer please")
                mark = 0
        total_mark += mark

    end_time = datetime.datetime.now()

    delta_time = end_time - start_time
    log_fhd.close()

    print("Time		  : %s" % delta_time)
    print("Total Mark : {0:>2.2f}%".format(total_mark / num_questions * 100))
    print("Errors: {}".format(errDict))
    input()
