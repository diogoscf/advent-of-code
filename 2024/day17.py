import os
import re
import numpy as np

filename = "day17.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

registers_pattern = r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)"
program_pattern = r"Program: ([\d,]+)"

A_i, B_i, C_i = [int(x) for x in re.findall(registers_pattern, txt)[0]]
program = [int(x) for x in re.findall(program_pattern, txt)[0].split(",")]


def combo(operand, A, B, C):
    return [0, 1, 2, 3, A, B, C][operand]


def adv(operand, A, B, C, pointer):
    A = A // (2 ** combo(operand, A, B, C))
    return A, B, C, pointer + 2, None


def bxl(operand, A, B, C, pointer):
    B = B ^ operand
    return A, B, C, pointer + 2, None


def bst(operand, A, B, C, pointer):
    B = combo(operand, A, B, C) % 8
    return A, B, C, pointer + 2, None


def jnz(operand, A, B, C, pointer):
    if A == 0:
        return A, B, C, pointer + 2, None
    else:
        pointer = operand
        return A, B, C, pointer, None


def bxc(operand, A, B, C, pointer):
    B = B ^ C
    return A, B, C, pointer + 2, None


def out(operand, A, B, C, pointer):
    return A, B, C, pointer + 2, (combo(operand, A, B, C) % 8)


def bdv(operand, A, B, C, pointer):
    B = A // (2 ** combo(operand, A, B, C))
    return A, B, C, pointer + 2, None


def cdv(operand, A, B, C, pointer):
    C = A // (2 ** combo(operand, A, B, C))
    return A, B, C, pointer + 2, None


instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def run_program(A, B, C, program):
    pointer = 0
    output = []
    while True:
        if pointer >= len(program):
            return ",".join([str(x) for x in output])
        opcode = program[pointer]
        operand = program[pointer + 1]
        A, B, C, pointer, out_curr = instructions[opcode](operand, A, B, C, pointer)
        if out_curr is not None:
            output.append(out_curr)

# this involved a lot of sorcery, probably wouldn't work for any other input
def find_A(desired_out):
    A_ok = list(range(2**7))
    operation = lambda x: (x & 7) ^ ((x >> ((x & 7) ^ 3)) & 7) ^ 6
    for i, out in enumerate(desired_out):
        new_accept = []
        for left3 in range(2**3):
            for okA in A_ok:
                # we only care about 10 bits at a time due to the way the program works
                A = left3 << 7 | (okA >> (3 * i))
                if operation(A) == out:
                    new_accept.append(left3 << (7 + 3 * i) | okA)
        A_ok = new_accept
    return min(A_ok)


print("Part 1:", run_program(A_i, B_i, C_i, program))
print("Part 2:", find_A(program))
