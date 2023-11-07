'''
MIPS-32 Instruction Level Simulatr

CSE261 UNIST
run.py
'''

import util
import initialize
import ctypes


def OPCODE(INST):
    return INST.opcode


def SET_OPCODE(INST, VAL):
    INST.opcode = ctypes.c_short(VAL).value


def FUNC(INST):
    return INST.func_code


def SET_FUNC(INST, VAL):
    INST.func_code = ctypes.c_short(VAL).value


def RS(INST):
    return INST.rs


def SET_RS(INST, VAL):
    INST.rs = ctypes.c_ubyte(VAL).value


def RT(INST):
    return INST.rt


def SET_RT(INST, VAL):
    INST.rt = ctypes.c_ubyte(VAL).value


def RD(INST):
    return INST.rd


def SET_RD(INST, VAL):
    INST.rd = ctypes.c_ubyte(VAL).value


def FS(INST):
    return RD(INST)


def SET_FS(INST, VAL):
    SET_RD(INST, VAL)


def FT(INST):
    return RT(INST)


def SET_FT(INST, VAL):
    SET_RT(INST, VAL)


def FD(INST):
    return SHAMT(INST)


def SET_FD(INST, VAL):
    SET_SHAMT(INST, VAL)


def SHAMT(INST):
    return INST.shamt


def SET_SHAMT(INST, VAL):
    INST.shamt = ctypes.c_ubyte(VAL).value


def IMM(INST):
    return INST.imm


def SET_IMM(INST, VAL):
    INST.imm = ctypes.c_short(VAL).value


def BASE(INST):
    return RS(INST)


def SET_BASE(INST, VAL):
    SET_RS(INST, VAL)


def IOFFSET(INST):
    return IMM(INST)


def SET_IOFFSET(INST, VAL):
    SET_IMM(INST, VAL)


def IDISP(INST):
    X = INST.imm << 2
    return SIGN_EX(X)


def COND(INST):
    return RS(INST)


def SET_COND(INST, VAL):
    SET_RS(INST, VAL)


def CC(INST):
    return (RT(INST) >> 2)


def ND(INST):
    return ((RT(INST) & 0x2) >> 1)


def TF(INST):
    return (RT(INST) & 0x1)


def TARGET(INST):
    return INST.target


def SET_TARGET(INST, VAL):
    INST.target = VAL


def ENCODING(INST):
    return INST.encoding


def SET_ENCODIGN(INST, VAL):
    INST.encoding = VAL


def EXPR(INST):
    return INST.expr


def SET_EXPR(INST, VAL):
    INST.expr = VAL


def SOURCE(INST):
    return INST.source_line


def SET_SOURCE(INST, VAL):
    INST.source_line = VAL


# Sign Extension From 16 -> 32 bit
def SIGN_EX(X):
    if (X) & 0x8000:
        return X | 0xffff0000
    else:
        return X


COND_UN = 0x1
COND_EQ = 0x2
COND_LT = 0x4
COND_IN = 0x8

# Minimum and maximum values that fit in instruction's imm field
IMM_MIN = 0xffff8000
IMM_MAX = 0x00007fff

UIMM_MIN = 0
UIMM_MAX = (1 << 16)-1


def BRANCH_INST(TEST, TARGET):
    if TEST:
        target = TARGET
        JUMP_INST(target)


def JUMP_INST(TARGET):
    import util
    util.CURRENT_STATE.PC = TARGET


def LOAD_INST(LD, MASK):
    return (LD & (MASK))


# Procedure: get_inst_info
# Purpose: Read instruction information
def get_inst_info(pc):
    return initialize.INST_INFO[(pc - util.MEM_TEXT_START) >> 2]


inst_map = {(0, 32): 'ADD', (8, 0): 'ADDI', (9, 0): 'ADDIU', (0, 33): 'ADDU', (0, 36): 'AND', (12, 0): 'ANDI', (4, 0): 'BEQ', (5, 0): 'BNE', (2, 0): 'J', (3, 0): 'JAL', (0, 8): 'JR', (15, 0): 'LUI', (35, 0): 'LW', (0, 39): 'NOR', (0, 37): 'OR', (13, 0): 'ORI', (0, 42): 'SLT', (10, 0): 'SLTI', (11, 0): 'SLTIU', (0, 43): 'SLTU', (0, 0): 'SLL', (0, 2): 'SRL', (43, 0): 'SW', (0, 34): 'SUB', (0, 35): 'SUBU'}

R = ['ADD', 'ADDU', 'AND', 'JR', 'NOR', 'OR', 'SLT', 'SLTU', 'SLL', 'SRL', 'SUB', 'SUBU']
I = ['ADDI', 'ADDIU', 'ANDI', 'BEQ', 'BNE', 'LUI', 'LW', 'ORI', 'SLTI', 'SLTIU', 'SW']
J = ['J', 'JAL']

def neg_to_nbits(v, n = 32):
    return v if v>=0 else (1<<n) + v

def nbits_to_int(v, n = 32):
    return v if v & (1 << n-1) == 0 else v - (1 << n)

DEBUG = False

# Procedure: process_instruction
# Purpose: Process one instruction
def process_instruction():
    # Implement this function
    # erase "pass" to start implementing
    cur_inst = get_inst_info(util.CURRENT_STATE.PC)
    op = OPCODE(cur_inst)
    fn = FUNC(cur_inst) if op == 0 else 0
    global DEBUG
    if DEBUG:
        util.inst_file.write(f"opcode: {hex(op)}, func_code: {hex(fn)}, PC: {hex(util.CURRENT_STATE.PC)}\n")
    else:
        util.inst_file.write(f"opcode: {hex(op)}, func_code: {hex(fn)}\n")

    global inst_map
    global R
    global I
    global J
    inst_str = inst_map[(op, fn)]
    inst_type = 'R' if op==0 else ('I' if inst_str in I else 'J')

    regs = util.CURRENT_STATE.REGS

    if inst_type == 'R':
        rs, rt, rd, shamt = cur_inst.rs, cur_inst.rt, cur_inst.rd, cur_inst.shamt
        vs, vt, vd = map(nbits_to_int, [regs[rs], regs[rt], regs[rd]])
        if inst_str == 'ADD':
            regs[rd] = neg_to_nbits(vs + vt)
        if inst_str == 'SUB':
            regs[rd] = neg_to_nbits(vs - vt)
        if inst_str == 'ADDU':
            regs[rd] = regs[rs] + regs[rt] & 0xffffffff
        if inst_str == 'SUBU':
            regs[rd] = regs[rs] + ~regs[rt] + 1 & 0xffffffff
        if inst_str == 'AND':
            regs[rd] = regs[rs] & regs[rt]
        if inst_str == 'OR':
            regs[rd] = regs[rs] | regs[rt]
        if inst_str == 'NOR':
            regs[rd] = neg_to_nbits(~ (regs[rs] | regs[rt])) & 0xffffffff
        if inst_str == 'SLL':
            regs[rd] = regs[rt] << shamt & 0xffffffff
        if inst_str == 'SRL':
            regs[rd] = regs[rt] >> shamt & 0xffffffff
        if inst_str == 'SLT':
            regs[rd] = 1 if nbits_to_int(regs[rs]) < nbits_to_int(regs[rt]) else 0
        if inst_str == 'SLTU':
            regs[rd] = 1 if regs[rs] < regs[rt] else 0
        if inst_str == 'JR':
            util.CURRENT_STATE.PC = regs[rs]
        else: util.CURRENT_STATE.PC += 4
    elif inst_type == 'I':
        rs, rt, imm = cur_inst.rs, cur_inst.rt, cur_inst.imm
        vs, vt = map(nbits_to_int, [regs[rs], regs[rt]])
        if inst_str == 'ADDI':
            regs[rt] = neg_to_nbits(vt) + SIGN_EX(imm) & 0xffffffff
        if inst_str == 'ADDIU':
            regs[rt] = regs[rs] + SIGN_EX(imm) & 0xffffffff
        if inst_str == 'ANDI':
            regs[rt] = regs[rs] & imm
        if inst_str == 'ORI':
            regs[rt] = regs[rs] | imm
        if inst_str == 'SLTI':
            regs[rt] = 1 if nbits_to_int(regs[rs]) < nbits_to_int(SIGN_EX(imm)) else 0
        if inst_str == 'SLTIU':
            regs[rt] = 1 if regs[rs] < SIGN_EX(imm) else 0
        if inst_str == 'LW':
            regs[rt] = util.mem_read(regs[rs]+nbits_to_int(imm, 16))
        if inst_str == 'SW':
            util.mem_write(regs[rs] + imm, regs[rt])
        if inst_str == 'LUI':
            regs[rt] = imm << 16
        if (inst_str == 'BEQ' and regs[rt] == regs[rs]) or (inst_str == 'BNE' and regs[rt] - regs[rs]):
            util.CURRENT_STATE.PC = util.CURRENT_STATE.PC + 4 + (nbits_to_int(imm, 16)<<2)
        else: util.CURRENT_STATE.PC += 4
    elif inst_type == 'J':
        #addr = cur_inst.value & 0b111111111111111111111111
        if inst_str == 'JAL':
            regs[31] = util.CURRENT_STATE.PC + 8
        util.CURRENT_STATE.PC = cur_inst.target << 2 #((util.CURRENT_STATE.PC+4) & (0b1111<<28)) | (addr<<2)
    if util.CURRENT_STATE.PC == initialize.text_size + util.MEM_TEXT_START:
        util.RUN_BIT = False
