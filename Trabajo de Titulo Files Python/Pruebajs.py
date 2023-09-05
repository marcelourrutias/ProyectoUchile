import sys, re

registers = {
	"zero": "00000",
	"ra": "00001",
	"sp": "00010",
	"gp": "00011",
	"tp": "00100",
	"t0": "00101",
	"t1": "00110",
	"t2": "00111",
	"s0": "01000",
	"s1": "01001",
	"a0": "01010",
	"a1": "01011",
	"a2": "01100",
	"a3": "01101",
	"a4": "01110",
	"a5": "01111",
	"a6": "10000",
	"a7": "10001",
	"s2": "10010",
	"s3": "10011",
	"s4": "10100",
	"s5": "10101",
	"s6": "10110",
	"s7": "10111",
	"s8": "11000",
	"s9": "11001",
	"s10": "11010",
	"s11": "11011",
	"t3": "11100",
	"t4": "11101",
	"t5": "11110",
	"t6": "11111"
}

registers_float = {
    "ft0": "00000",
	"ft1": "00001",
	"ft2": "00010",
	"ft3": "00011",
	"ft4": "00100",
	"ft5": "00101",
	"ft6": "00110",
	"ft7": "00111",
	"fs0": "01000",
	"fs1": "01001",
	"fa0": "01010",
	"fa1": "01011",
	"fa2": "01100",
	"fa3": "01101",
	"fa4": "01110",
	"fa5": "01111",
	"fa6": "10000",
	"fa7": "10001",
	"fs2": "10010",
	"fs3": "10011",
	"fs4": "10100",
	"fs5": "10101",
	"fs6": "10110",
	"fs7": "10111",
	"fs8": "11000",
	"fs9": "11001",
	"fs10": "11010",
	"fs11": "11011",
	"ft8": "11100",
	"ft9": "11101",
	"ft10": "11110",
	"ft11": "11111"
}

def is_binary(num_str):
	return len(num_str) >= 2 and num_str[0:2] == "0b"

def is_hex(num_str):
	return len(num_str) >= 2 and num_str[0:2] == "0x"

def is_int(num_str):
	for chr in num_str:
		if not(chr.isdigit() or chr == '-'):
			return False

	return True

def num_str_to_bin(num_str, base, pad, signed):
	bytes_num = int(num_str, base).to_bytes(4, byteorder="big", signed=signed)
	bin_num = "".join(format(x, '08b') for x in bytes_num)
	
	return bin_num[-pad:]

def val_to_bin(num_str, pad, signed, ref_dict=None):
	if is_binary(num_str):
		return num_str_to_bin(num_str[2:], 2, pad, signed)
	elif is_hex(num_str):
		return num_str_to_bin(num_str[2:], 16, pad, signed)
	elif is_int(num_str):
		return num_str_to_bin(num_str, 10, pad, signed)
	elif ref_dict and num_str in ref_dict:
		return ref_dict[num_str]
	
	raise ValueError(f"{num_str} can not be converted to binary")

def reg_to_bin(num_str):
	if num_str[0] == 'x':
		return num_str_to_bin(num_str[1:], 10, 5, False)
	else:
		return val_to_bin(num_str, 5, False, ref_dict=registers)

def reg_float_to_bin(num_str):
	if num_str[0] == 'f':
		return num_str_to_bin(num_str[1:], 10, 5, False)
	else:
		return val_to_bin(num_str, 5, False, ref_dict=registers_float)


def parse_reg_imm(cmd, data):
	groups = re.match(r"([^,]+),(.+)", cmd).groups()
	data.rd = groups[0]
	data.imm = groups[1]

def parse_reg_off_reg(cmd, data):
	groups = re.match(r"([^,]+),([^(]+)\(([^)]+)\)", cmd).groups()
	data.rd = groups[0]
	data.imm = groups[1]
	data.rs1 = groups[2]

def parse_reg_reg_imm(cmd, data):
	groups = re.match(r"([^,]+),([^,]+),(.+)", cmd).groups()
	data.rd = groups[0]
	data.rs1 = groups[1]
	data.imm = groups[2]

def parse_ecall(cmd, data):
	#groups = re.match(r"([^,]+),([^,]+),(.+)", cmd).groups()
	data.rd = '00000'
	data.rs1 = '00000'
	data.imm = '000000000000'

def parse_ebreak(cmd, data):
	#groups = re.match(r"([^,]+),([^,]+),(.+)", cmd).groups()
	data.rd = '00000'
	data.rs1 = '00000'
	data.imm = '000000000001'

def parse_reg_reg_reg(cmd, data):
	groups = re.match(r"([^,]+),([^,]+),(.+)", cmd).groups()
	data.rd = groups[0]
	data.rs1 = groups[1]
	data.rs2 = groups[2]

def parse_reg_reg_reg_reg(cmd, data):
	groups = re.match(r"([^,]+),([^,]+),([^,]+),(.+)", cmd).groups()
	data.rd = groups[0]
	data.rs1 = groups[1]
	data.rs2 = groups[2]
	data.rs3 = groups[3]

def parse_reg_reg(cmd, data):
	groups = re.match(r"([^,]+),([^,]+)", cmd).groups()
	data.rd = groups[0]
	data.rs1 = groups[1]
	data.rs2 = '00000'


def parse_reg_reg_1(cmd, data):
	groups = re.match(r"([^,]+),([^,]+)", cmd).groups()
	data.rd = groups[0]
	data.rs1 = groups[1]
	data.rs2 = '00001'





def ex_rtype(data):
	rd_bin = reg_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rs1)
	rs2_bin = reg_to_bin(data.rs2)

	return data.funct7 + rs2_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_r4type(data):
	rd_bin = reg_float_to_bin(data.rd)
	rs1_bin = reg_float_to_bin(data.rs1)
	rs2_bin = reg_float_to_bin(data.rs2)
	rs3_bin = reg_float_to_bin(data.rs3)

	return rs3_bin + '00' + rs2_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_rtype_float(data):
	rd_bin = reg_float_to_bin(data.rd)
	rs1_bin = reg_float_to_bin(data.rs1)
	rs2_bin = reg_float_to_bin(data.rs2)

	return data.funct7 + rs2_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_rtype_float_int(data):
	rd_bin = reg_float_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rs1)
	rs2_bin = reg_float_to_bin(data.rs2)

	return data.funct7 + rs2_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_rtype_int_float(data):
	rd_bin = reg_to_bin(data.rd)
	rs1_bin = reg_float_to_bin(data.rs1)
	rs2_bin = reg_float_to_bin(data.rs2)

	return data.funct7 + rs2_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_itype(data):
	rd_bin = reg_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rs1)
	imm_bin = val_to_bin(data.imm, 12, True)

	return imm_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_itype_float(data):
	rd_bin = reg_float_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rs1)
	imm_bin = val_to_bin(data.imm, 12, True)

	return imm_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_sitype(data):
	rd_bin = reg_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rs1)
	imm_bin = val_to_bin(data.imm, 5, False)

	return data.funct7 + imm_bin + rs1_bin + data.funct3 + rd_bin + data.opcode

def ex_stype(data):
	rs1_bin = reg_to_bin(data.rs1)
	rs2_bin = reg_to_bin(data.rd)
	imm_bin = val_to_bin(data.imm, 12, True)

	return imm_bin[-12:-5] + rs2_bin + rs1_bin + data.funct3 + imm_bin[-5:] + data.opcode

def ex_stype_float(data):
	rs1_bin = reg_to_bin(data.rs1)
	rs2_bin = reg_float_to_bin(data.rd)
	imm_bin = val_to_bin(data.imm, 12, True)

	return imm_bin[-12:-5] + rs2_bin + rs1_bin + data.funct3 + imm_bin[-5:] + data.opcode

def ex_btype(data):
	rd_bin = reg_to_bin(data.rd)
	rs1_bin = reg_to_bin(data.rd)
	rs2_bin = reg_to_bin(data.rs1)
	imm_bin = val_to_bin(data.imm, 13, True)

	return imm_bin[-13] + imm_bin[-11:-5] + rs2_bin + rs1_bin + data.funct3 + imm_bin[-5:-1] + imm_bin[-12] + data.opcode

def ex_utype(data):
	rd_bin = reg_to_bin(data.rd)
	imm_bin = val_to_bin(data.imm, 32, True)

	return imm_bin[-32:-12] + rd_bin + data.opcode

def ex_jtype(data):
	rd_bin = reg_to_bin(data.rd)
	imm_bin = val_to_bin(data.imm, 21, True)

	return imm_bin[-21] + imm_bin[-11:-1] + imm_bin[-12] + imm_bin[-20:-12] + rd_bin + data.opcode


class CommandData:
	def __init__(self, opcode, funct3=None, funct7=None):
		self.opcode = opcode
		self.funct3 = funct3
		self.funct7 = funct7
		self.rd = None
		self.rs1 = None
		self.rs2 = None
		self.rs3 = None
		self.imm = None


class CommandHandler:
	def __init__(self, parser, executor, data):
		self.parser = parser
		self.executor = executor
		self.data = data

	def parse(self, command):
		self.parser(command, self.data)

	def execute(self):
		return self.executor(self.data)

handlers = {
	"lui":		CommandHandler(parse_reg_imm, ex_utype, CommandData("0110111")),
	"auipc": 	CommandHandler(parse_reg_imm, ex_utype, CommandData("0010111")),
	"jal": 		CommandHandler(parse_reg_imm, ex_jtype, CommandData("1101111")),
	"jalr": 	CommandHandler(parse_reg_off_reg, ex_itype, CommandData("1100111", "000")),
	"beq": 		CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "000")),
	"bne": 		CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "001")),
	"blt": 		CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "100")),
	"bge": 		CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "101")),
	"bltu": 	CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "110")),
	"bgeu": 	CommandHandler(parse_reg_reg_imm, ex_btype, CommandData("1100011", "111")),
	"lb": 		CommandHandler(parse_reg_off_reg, ex_itype, CommandData("0000011", "000")),
	"lh": 		CommandHandler(parse_reg_off_reg, ex_itype, CommandData("0000011", "001")),
	"lw": 		CommandHandler(parse_reg_off_reg, ex_itype, CommandData("0000011", "010")),
	"lbu": 		CommandHandler(parse_reg_off_reg, ex_itype, CommandData("0000011", "100")),
	"lhu": 		CommandHandler(parse_reg_off_reg, ex_itype, CommandData("0000011", "101")),
	"sb": 		CommandHandler(parse_reg_off_reg, ex_stype, CommandData("0100011", "000")),
	"sh": 		CommandHandler(parse_reg_off_reg, ex_stype, CommandData("0100011", "001")),
	"sw": 		CommandHandler(parse_reg_off_reg, ex_stype, CommandData("0100011", "010")),
	"addi": 	CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "000")),
	"slti": 	CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "010")),
	"sltiu": 	CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "011")),
	"xori": 	CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "100")),
	"ori": 		CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "110")),
	"andi": 	CommandHandler(parse_reg_reg_imm, ex_itype, CommandData("0010011", "111")),
	"slli": 	CommandHandler(parse_reg_reg_imm, ex_sitype, CommandData("0010011", "000", "0000000")),
	"srli": 	CommandHandler(parse_reg_reg_imm, ex_sitype, CommandData("0010011", "000", "0000000")),
	"srai": 	CommandHandler(parse_reg_reg_imm, ex_sitype, CommandData("0010011", "000", "0100000")),
	"add": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"sub": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0100000")),
	"sll": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"slt": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"sltu": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"xor": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"srl": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"sra": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0100000")),
	"or": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),
	"and": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000000")),

	"ecall": 	CommandHandler(parse_ecall, ex_itype, CommandData("1110011", "000")),
	"ebreak": 	CommandHandler(parse_ebreak, ex_itype, CommandData("1110011", "000")),


	"mul": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "000", "0000001")),
	"mulh": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "001", "0000001")),
	"mulhsu": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "010", "0000001")),
	"mulhu": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "011", "0000001")),
	"div": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "100", "0000001")),
	"divu": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "101", "0000001")),
	"rem": 		CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "110", "0000001")),
	"remu": 	CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0110011", "111", "0000001")),


	
	"flw": 		CommandHandler(parse_reg_off_reg, ex_itype_float, CommandData("0000111", "010")),
	"fsw": 		CommandHandler(parse_reg_off_reg, ex_stype_float, CommandData("0100111", "010")),

	
	"fmadd.s":	CommandHandler(parse_reg_reg_reg_reg, ex_r4type, CommandData("1000011", "111")),
	"fmsub.s":	CommandHandler(parse_reg_reg_reg_reg, ex_r4type, CommandData("1000111", "111")),
	"fnmadd.s":	CommandHandler(parse_reg_reg_reg_reg, ex_r4type, CommandData("1001011", "111")),
	"fnmsub.s":	CommandHandler(parse_reg_reg_reg_reg, ex_r4type, CommandData("1001111", "111")),

	"fadd.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "111", "0000000")),
	"fsub.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "111", "0000100")),
	"fmul.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "111", "0001000")),
	"fdiv.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "111", "0001100")),
	"fsqrt.s":	CommandHandler(parse_reg_reg, ex_rtype_float, CommandData("1010011", "111", "0101100")),
	"fsgnj.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "000", "0010000")),
	"fsgnjn.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "001", "0010000")),
	"fsgnjx.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "010", "0010000")),
	"fmin.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "000", "0010100")),
	"fmax.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "001", "0010100")),
	"fcvt.w.s":	CommandHandler(parse_reg_reg, ex_rtype_int_float, CommandData("1010011", "111", "1100000")),
	"fcvt.wu.s":CommandHandler(parse_reg_reg_1, ex_rtype_int_float, CommandData("1010011", "111", "1100000")),
	"fmv.x.w":	CommandHandler(parse_reg_reg, ex_rtype_int_float, CommandData("1010011", "000", "1110000")),
	"feq.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "010", "1010000")),
	"flt.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "001", "1010000")),
	"fle.s":	CommandHandler(parse_reg_reg_reg, ex_rtype_float, CommandData("1010011", "000", "1010000")),
	"fclass.s":	CommandHandler(parse_reg_reg, ex_rtype_int_float, CommandData("1010011", "001", "1110000")),
	"fcvt.s.w":	CommandHandler(parse_reg_reg, ex_rtype_float_int, CommandData("1010011", "111", "1101000")),
	"fcvt.s.wu":CommandHandler(parse_reg_reg_1, ex_rtype_float_int, CommandData("1010011", "111", "0000001")),
	"fmv.w.x":	CommandHandler(parse_reg_reg, ex_rtype_float_int, CommandData("1010011", "000", "1111000")),




    "lr.w": CommandHandler(parse_reg_reg, ex_rtype, CommandData("0101111", "010", "0001000")),
    "lr.w.aq": CommandHandler(parse_reg_reg, ex_rtype, CommandData("0101111", "010", "0001010")),
    "lr.w.rl": CommandHandler(parse_reg_reg, ex_rtype, CommandData("0101111", "010", "0001001")),
    "lr.w.aq.rl": CommandHandler(parse_reg_reg, ex_rtype, CommandData("0101111", "010", "0001011")),
    "sc.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0001100")),
    "sc.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0001110")),
    "sc.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0001101")),
    "sc.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0001111")),
    "amoswap.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000100")),
    "amoswap.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000110")),
    "amoswap.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000101")),
    "amoswap.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000111")),
    "amoadd.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000000")),
    "amoadd.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000010")),
    "amoadd.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000001")),
    "amoadd.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0000011")),
    "amoxor.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0010000")),
    "amoxor.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0010010")),
    "amoxor.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0010001")),
    "amoxor.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0010011")),
    "amoand.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0110000")),
    "amoand.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0110010")),
    "amoand.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0110001")),
    "amoand.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0110011")),
    "amoor.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0100000")),
    "amoor.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0100010")),
    "amoor.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0100001")),
    "amoor.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "0100011")),
    "amomin.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1000000")),
    "amomin.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1000010")),
    "amomin.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1000001")),
    "amomin.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1000011")),
    "amomax.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1010000")),
    "amomax.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1010010")),
    "amomax.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1010001")),
    "amomax.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1010011")),
    "amominu.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1100000")),
    "amominu.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1100010")),
    "amominu.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1100001")),
    "amominu.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1100011")),
    "amomaxu.w": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1110000")),
    "amomaxu.w.aq": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1110010")),
    "amomaxu.w.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1110001")),
    "amomaxu.w.aq.rl": CommandHandler(parse_reg_reg_reg, ex_rtype, CommandData("0101111", "010", "1110011"))
}


if __name__ == "__main__":
	cmd_str = sys.argv[1].strip().lower()
	parts = cmd_str.split(" ")
	title = parts[0]
	tail = "".join(parts[1:])

	handler = handlers[title]
	handler.parse(tail)
	output = handler.execute()

	print(output)