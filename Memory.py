'''
	Simpletron memory
'''
from os import system,sys,path

class Memory(object):
    def __init__(self,size:int):
        self.memory:list = []
        self.size = size
        self.count = 0
        for i in range(0,self.size):
            self.memory.append('0000')
        
    def getitem(self,address:int)->str:
        return self.memory[address]
        
    def setitem(self,address:int,value:str)->None:
        self.memory[address] = value
        
    def __str__(self)->str:
        return str(self.memory)
    

def dump(mem:list)->None:
    
    dcount:int = 1
    [print(f"{i:8}",end="") for i in range(0,10)]
    print(f"\n00",end=" ")
    for i in range(0,len(mem)):
        if dcount % 10 == 0 and dcount<100:
            print(f"+{mem[i]:7}")
            print(f"{(i+1)}",end=" ")
        else:
            print(f"+{mem[i]:7}",end="")
        dcount+=1
    print()
    print('-'*100)
    
def loader(filename:str)->None:
    program:list = []
    if path.exists(filename):
        file = open(filename)
        program = file.readlines()
        file.close()
    return program

class Processor:
    def __init__(self, memory: Memory):
        self.accumulator = 0  
        self.program_counter = 0 
        self.instruction_register = None  
        self.memory = memory
        self.halted = False

    def fetch(self):
        self.instruction_register = self.memory.getitem(self.program_counter)
        self.program_counter += 1

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
        """Run the processor to execute instructions in memory."""
        self.fetch()
        opcode, operand = self.decode()
        self.execute(opcode, operand) 
        print()
        print("REGISTERS")
        print(f"accumulator: {self.accumulator}")
        print(f"instructionRegister: {self.instruction_register}")
        print(f"programCounter: {self.program_counter}")
        print(f"operationCode: {opcode}")
        print(f"operand: {operand}\n")   

def main()->None:
    m = Memory(100)
    print("REGISTERS")
    print(f"accumulator: +0000")
    print(f"instructionRegister: 00")
    print(f"programCounter: +0000")
    print(f"operationCode: 00")
    print(f"operand: 00\n")
    print("MEMORY")
    dump(m.memory)

    # system('cls')
    filename:str = str(sys.argv[1])
    # print(filename)
    program:list = loader(filename)
            
    for item in program:
        instruction:list = item.strip().split("\t")
        #print(instruction)
        address = instruction[0]
        command = instruction[1]
        m.setitem(int(address),command)

    processor = Processor(m)
    while not processor.halted:
        processor.run()
        print("MEMORY")
        dump(m.memory)

if __name__=="__main__":
    main()