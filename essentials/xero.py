"""
$PYRUN_CODE X

$END_BLOCK X
"""
import subprocess
import sys,os
from pathlib import Path
from . import interaction

debug = True

VALID_TYPES = ['PyRunBlock','CmdBlock','SendMessageBlock']
class _BlockType:
    def __init__(self,type_:str):
        if type_ in VALID_TYPES:
            self.type=type_
        else:
            raise TypeError("Invalid BlockType.")
    def __repr__(self):
        return f"<B_TYPE {self.type}>"
PyRunBlock = _BlockType('PyRunBlock')
CmdBlock = _BlockType('CmdBlock')
SendMessageBlock = _BlockType('SendMessageBlock')

class Block:
    def __init__(self,block_name:str,block_type:_BlockType,context:str):
        self.block_name = block_name
        self.block_type = block_type
        self.context = context
        self.is_executed = False
    def __repr__(self):
        return f"<Block name=\"{self.block_name}\" type=\"{self.block_type}\">"
test_string = """
$SEND_MESSAGE PythonScript
Yes, I can write a Python script that prints the first 100 prime numbers.
Here's the code:
```
def is_prime(num):
    # Checks if a number is prime
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
```
Do you want me to run the code for you?
$END_BLOCK PythonScript
$PYRUN_CODE PrintPrimes
import interaction

def is_prime(num):
    # Checks if a number is prime
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
$END_BLOCK PrintPrimes
$SEND_MESSAGE Successful
I ran the python code and saved the results of prime numbers in a txt file in Documents folder.
I also opened the text file in notepad so you can see the results.
$END_BLOCK Successful
"""

def blockize(string:str):
    blockchain = BlockChain("BlockChain")
    In_Block = False
    block_name=None
    block_type=None
    block_context=None
    for line in string.splitlines():
        if line.startswith('$PYRUN_CODE'):
            block_name=line.split(' ')[1]
            block_type=PyRunBlock
            block_context=""
            In_Block = True
        elif line.startswith('$CMD_BLOCK'):
            block_name=line.split(' ')[1]
            block_type=CmdBlock
            block_context=""
            In_Block = True
        elif line.startswith('$SEND_MESSAGE'):
            block_name=line.split(' ')[1]
            block_type=SendMessageBlock
            block_context=""
            In_Block = True
        elif line.startswith('$END_BLOCK'):
            blockchain.add_block(Block(block_name,block_type,block_context))
            In_Block = False
            block_name=None
            block_type=None
            block_context=None
            continue
        else:
            if In_Block:
                block_context+=line+'\n'
    return blockchain

    
class BlockChain:
    def __init__(self,blockchain_name):
        self.blockchain_name = blockchain_name
        self.blockchain = []
    def add_block(self,block:Block):
        self.blockchain.append(block)
    def get_blockchain(self):
        return self.blockchain

class Compiler:
    def __init__(self,blockchain:BlockChain):
        self.blockchain = blockchain
        self.compiled_names = []
    def update_blockchain(self,new_blockchain:BlockChain):
        self.blockchain = new_blockchain
        return self
    def execute_python(self,context):
        if debug:
            print(context)
        sys.path.append(str(Path(__file__).parent.absolute()))
        code_object = compile(context,"<string>",'exec')
        exec(code_object)
        return True
    def execute_cmd(self,context):
        if debug:
            print(context)
        return subprocess.run(context,shell=True)
    def execute_block(self,block:Block):
        if block.is_executed or block.block_name in self.compiled_names:
            return True
        if block.block_type == PyRunBlock:
            self.execute_python(block.context)
        elif block.block_type == CmdBlock:
            self.execute_cmd(block.context)
        block.is_executed = True
        self.compiled_names.append(block.block_name)
        return True
    # def execute_blockchain(self,blockchain:BlockChain):
    #     ...
    def execute(self):
        for block in self.blockchain.get_blockchain():
            if block.block_type == SendMessageBlock:
                yield block.context
                continue
            self.execute_block(block)

class ReplaceRandom:
    def __init__(self,ls):
        self.max = len(ls)
        self.current = 0
        self.ls=ls
    def Next(self):
        if self.current == self.max:
            self.current = 0
        _ = self.ls[self.current]
        self.current+=1
        return _