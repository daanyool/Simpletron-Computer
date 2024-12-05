from os import system, sys, path

class Memory(object):
    def __init__(self, size: int):
        self.memory: list = []
        self.size = size
        self.count = 0
        for i in range(0, self.size):
            self.memory.append('0000')
        
    def getitem(self, address: int) -> str:
        return self.memory[address]
        
    def setitem(self, address: int, value: str) -> None:
        self.memory[address] = value
        
    def __str__(self) -> str:
        return str(self.memory)

def dump(mem: list) -> None:
    dcount: int = 1
    [print(f"{i:8}", end="") for i in range(0, 10)]
    print(f"\n00", end=" ")
    for i in range(0, len(mem)):
        if dcount % 10 == 0 and dcount < 100:
            print(f"+{mem[i]:7}")
            print(f"{(i + 1)}", end=" ")
        else:
            print(f"+{mem[i]:7}", end="")
        dcount += 1
    print()
    print('-' * 100)

def loader(filename: str, memory: Memory, symbol_table: dict) -> None:
    if path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                address = int(parts[0])
                command = parts[1]

                if command in Processor.opcode_map:
                    opcode = Processor.opcode_map[command]
                    if command in {"loadI", "addI", "subI", "divI", "modI", "mulI"}:
                        operand = int(parts[2])
                        instruction = f"{opcode:02d}{operand:02d}"
                    elif command == "halt":
                        instruction = f"{opcode:02d}00"
                    else:
                        operand_label = parts[2]
                        operand = symbol_table.get(operand_label)
                        if operand is None:
                            print(f"Error: Undefined label '{operand_label}'")
                            return
                        instruction = f"{opcode:02d}{operand:02d}"
                    
                    memory.setitem(address, instruction)
                else:
                    print(f"Unknown command in file: {command}")

class Processor:
    opcode_map = {
        "read": 10, "write": 11, "loadM": 20, "store": 21, "loadI": 22,
        "addM": 30, "subM": 31, "divM": 32, "modM": 33, "mulM": 34,
        "addI": 35, "subI": 36, "divI": 37, "modI": 38, "mulI": 39,
        "jmp": 40, "jn": 41, "jz": 42, "halt": 43
    }

    def __init__(self, memory: Memory, symbol_table: dict):
        self.accumulator = 0  
        self.program_counter = 0 
        self.instruction_register = None  
        self.memory = memory
        self.symbol_table = symbol_table
        self.halted = False    

    def fetch(self):
        instruction = self.memory.getitem(self.program_counter)
        self.program_counter += 1
        parts = instruction.split()

        if len(parts) == 1 and instruction[:4].isnumeric():
            # Direct numeric instruction
            self.instruction_register = instruction
        elif parts[0] in self.opcode_map:
            opcode = self.opcode_map[parts[0]]
            if parts[0] in {"loadI", "addI", "subI", "divI", "modI", "mulI"}:  # Immediate value instructions
                operand = int(parts[1])
                self.instruction_register = f"{opcode:02d}{operand:02d}"
            elif parts[0] in {"HALT"}:
                self.halted = True
            else:
                operand_label = parts[1]
                operand = self.symbol_table.get(operand_label, None)
                if operand is None:
                    print(f"Error: Undefined label '{operand_label}'")
                    self.halted = True
                    return
                self.instruction_register = f"{opcode:02d}{operand:02d}"
        else:
            print(f"Unknown instruction: {instruction}")
            self.halted = True            

    def decode(self):
        instruction = int(self.instruction_register)
        opcode = instruction // 100 
        operand = instruction % 100  
        return opcode, operand

    def execute(self, opcode, operand):
        if opcode == 10:  # READ: Load value from input into memory
            value = input(f"Enter a value to store in memory location {operand}: ")
            self.memory.setitem(operand, value.zfill(4))
        
        elif opcode == 11: # WRITE: Write a value from a specific location in memory to the screen
            value = int(self.memory.getitem(operand))
            print(f"value: {value}")
        
        elif opcode == 20:  # LOADM: Load value from memory into the accumulator
            self.accumulator = int(self.memory.getitem(operand))
        
        elif opcode == 21:  # STORE: Store value from the accumulator into memory
            self.memory.setitem(operand, str(self.accumulator).zfill(4))

        elif opcode == 22:  # LOADI: The 2 digit operand becomes the immediate value to be loaded in the accumulator.
            self.accumulator = operand
        
        elif opcode == 30:  # ADDM: Add value from memory to the accumulator
            self.accumulator += int(self.memory.getitem(operand))
        
        elif opcode == 31:  # SUBM: Subtract value from memory to the accumulator
            self.accumulator -= int(self.memory.getitem(operand))

        elif opcode == 32:  # DIVM: Divide the accumulator by the value from the memory
            self.accumulator /= int(self.memory.getitem(operand))

        elif opcode == 33:  # MODM: Perform modulo between the value in the memory and the accumulator
            self.accumulator %= int(self.memory.getitem(operand))

        elif opcode == 34:  # MULM: Multiply value from memory to the accumulator
            self.accumulator *= int(self.memory.getitem(operand))

        elif opcode == 35:  # ADDI: Add the immediate operand represented by the next 2 digits to the word in the accumulator 
            self.accumulator += operand

        elif opcode == 36:  # SUBI: Subtract the immediate operand represented by the next 2 digits to the word in the accumulator 
            self.accumulator -= operand
            
        elif opcode == 37:  # DIVI: Divide the immediate operand represented by the next 2 digits to the word in the accumulator 
            self.accumulator /= operand

        elif opcode == 38:  # MODI: Perform a modulo betweeen the immediate operand represented by the next 2 digits to the word in the accumulator 
            self.accumulator %= operand

        elif opcode == 39:  # MULI: Multiply the immediate operand represented by the next 2 digits to the word in the accumulator 
            self.accumulator *= operand
        
        elif opcode == 40:  # JMP: Set the program counter to operand
            self.program_counter = operand
        
        elif opcode == 41:  # JN: If accumulator is negative, set program counter to operand
            if self.accumulator < 0:
                self.program_counter = operand
        
        elif opcode == 42:  # JZ: If accumulator is zero, set program counter to operand
            if self.accumulator == 0:
                self.program_counter = operand
        
        elif opcode == 43:  # HALT: Stop the program
            self.halted = True
            print("Program halted.")
        else:
            print(f"Unknown opcode: {opcode}")
            self.halted = True

    def run(self):
        self.fetch()
        opcode, operand = self.decode()
        self.execute(opcode, operand) 
        print("\nREGISTERS")
        print(f"accumulator: {self.accumulator}")
        print(f"instructionRegister: {self.instruction_register}")
        print(f"programCounter: {self.program_counter}")
        print(f"operationCode: {opcode}")
        print(f"operand: {operand}\n")   

def main() -> None:
    symbol_table = {
        "n": 21,
        "initOne": 22,
        "deductedN": 23,
        "fact": 24,
        "display": 16,
        "x": 8,
        "0": 00
    }

    m = Memory(100)
    print("REGISTERS")
    print(f"accumulator: +0000")
    print(f"instructionRegister: 00")
    print(f"programCounter: +0000")
    print(f"operationCode: 00")
    print(f"operand: 00\n")
    print("MEMORY")
    dump(m.memory)

    filename: str = str(sys.argv[1])
    loader(filename, m, symbol_table)

    processor = Processor(m, symbol_table)
    while not processor.halted:
        processor.run()
        print("MEMORY")
        dump(m.memory)
        input("press any key to continue...")

if __name__ == "__main__":
    main()