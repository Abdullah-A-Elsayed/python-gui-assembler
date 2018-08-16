"""
"""
from tkinter import *
root = Tk()
root.title("G7 assembler")
#root.geometry("500x500")
root.resizable(width=False,height=False)
opcode =                    {
                                            'R-TYPE' : { #function this case
                                                    'add': 32,
                                                    'and': 36,
                                                    'or': 37,
                                                    'sub': 34,
                                                    'sll': 0,
                                                    'slt': 42,
                                                    'srl' : 2,
                                                    'jr': 8,
                                                    'nor' : 39
                                            },
                                            'I-TYPE': {
                                                    'addi': 8,
                                                    'andi': 12,
                                                    'ori': 13,
                                                    'slti': 10,
                                                  # 'subi': 7, ##??
                                                    'lw': 35,
                                                    'sw': 43,
                                                    'lui': 15,
                                                    'lb': 32,
                                                    'sb': 40,
                                                    'lh': 33,
                                                    'sh': 41,
                                                    'beq': 4,
                                                    'bne': 5
                                            },
                                            'J-TYPE': {
                                                    'j': 2,
                                                    'jal': 3
                                            }
                            }
REGISTERS = {
        '$zero': '0',
        '$at': '1',
        '$v0': '2',
        '$v1': '3',
        '$a0': '4',
        '$a1': '5',
        '$a2': '6',
        '$a3': '7',
        '$t0': '8',
        '$t1': '9',
        '$t2': '10',
        '$t3': '11',
        '$t4': '12',
        '$t5': '13',
        '$t6': '14',
        '$t7': '15',
        '$s0': '16',
        '$s1': '17',
        '$s2': '18',
        '$s3': '19',
        '$s4': '20',
        '$s5': '21',
        '$s6': '22',
        '$s7': '23',
        '$t8': '24',
        '$t9': '25',
        '$k0': '26',
        '$k1': '27',
        '$gp': '28',
        '$sp': '29',
        '$fp': '30',
        '$ra': '31'
        }
def read_Entry(event):
    lines = entry.get("1.0","end-1c")
    if(lines!=''):
        lines_list = lines.split('\n')
        mc_list = []
        for line in lines_list :
            if(line!=''):
                line = to_Machine(line)
                temp = line.split('0b')
                line = temp[1]
                mc_list.append(line)
        fob = open("machine.txt",'w')
        for mc in mc_list:
            fob.write(mc+'\n')
        fob.close
    
def to_Machine(ins) :
    ins = ins.replace(',','') #removing commas
    ins = ins.replace('(',' ') #removing bracket
    ins = ins.replace(')','') #removing bracket
    l = ins.split()
    machine = 0
    ## most cases size of l = 4
    if( l.__len__()==4):
        if(opcode['R-TYPE'].get(l[0]) or opcode['R-TYPE'].get(l[0])==0):
            #print("R type")
            ##fn
            machine = machine + opcode['R-TYPE'][l[0]] ##function in reality
            ##sh_amt
            if(l[0]=='sll' or l[0]=='srl'):
             machine = machine + (int(l[3]))* (2**6)
            else:
             pass
            ##rd
            machine = machine + (int(REGISTERS[l[1]]))* (2**11)
            ##rt
            if(l[0]=='sll' or l[0]=='srl'):
             machine = machine + (int(REGISTERS[l[2]]))* (2**16)
            else:
             machine = machine + (int(REGISTERS[l[3]]))* (2**16)
            ##rs
            if(l[0]=='sll' or l[0]=='srl'):
             pass
            else:
             machine = machine + (int(REGISTERS[l[2]]))* (2**21)
            return(bin(machine))
        if(opcode['I-TYPE'].get(l[0]) or opcode['I-TYPE'].get(l[0])==0):
            #print("I type")
            ##2 categs num is last or before last
            if(l[0]=='slti' or l[0]=='addi' or l[0]=='andi' or l[0]=='ori' or l[0]=='beq' or l[0]=='bne'):
             #const
             machine = machine + (int(l[3]))
             #rt
             machine = machine + (int(REGISTERS[l[1]]))* (2**16)
             #rs
             machine = machine + (int(REGISTERS[l[2]]))* (2**21)
             #op
             machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
             return(bin(machine))
            else:##second cat contains lw, sw,...
             #const
             machine = machine + (int(l[2]))
             #rt
             machine = machine + (int(REGISTERS[l[1]]))* (2**16)
             #rs
             machine = machine + (int(REGISTERS[l[3]]))* (2**21)
             #op
             machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
             return(bin(machine))
    elif(l.__len__() ==2):   ## special cases when size of l = 2 (j,jr,jal)
        if(l[0]=='jr'):
            ##funct
            machine = machine + opcode['R-TYPE'][l[0]]
            ##rs
            machine = machine + (int(REGISTERS[l[1]]))* (2**21)
        else: #j,jal
            #const
            machine = machine + (int(l[1]))
            #op_code
            machine = machine + (opcode['J-TYPE'][l[0]]) * (2**26)
        return(bin(machine))
    elif(l.__len__()==3):  ##lui
        #const
        machine = machine + (int(l[2]))
        #rt
        machine = machine + (int(REGISTERS[l[1]]))* (2**16)
        #op
        machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
        return(bin(machine))
    
                                      
    
Label(root,text = "add assembly instructions",padx=5,pady = 5).grid(row=1)
instruction = StringVar();
entry = Text(root,width=30,height=6)
entry.grid(row=2,column =0,columnspan = 3,sticky = E + W )
entry.config(undo=True)
scroll = Scrollbar(command=entry.yview)
entry['yscrollcommand'] = scroll.set
scroll.grid(row=2,column=3,sticky='nsew')
add = Button(root,text = "CONVERT!")
add.grid(row=3,columnspan=4,sticky= E + W)
add.bind("<Button-1>",read_Entry)
root.mainloop()
