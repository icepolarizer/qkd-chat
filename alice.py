#other useful packages
import math
import matplotlib.pyplot as plt
import numpy as np

# Import Qiskit
from qiskit import Aer, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

import pickle


def randomStringGen(string_length):
    #output variables used to access quantum computer results at the end of the function
    output_list = []
    output = ''
    
    #start up your quantum circuit information
    backend = Aer.get_backend('qasm_simulator')  
    circuits = ['rs']
    
    #run circuit in batches of 10 qubits for fastest results. The results
    #from each run will be appended and then clipped down to the right n size.
    n = string_length
    temp_n = 10
    temp_output = ''
    for i in range(math.ceil(n/temp_n)):
        #initialize quantum registers for circuit
        q = QuantumRegister(temp_n, name='q')
        c = ClassicalRegister(temp_n, name='c')
        rs = QuantumCircuit(q, c, name='rs')
            
        #create temp_n number of qubits all in superpositions
        for i in range(temp_n):
            rs.h(q[i]) #the .h gate is the Hadamard gate that makes superpositions
            rs.measure(q[i],c[i])

        #execute circuit and extract 0s and 1s from key
        result = execute(rs, backend, shots=1).result()
        counts = result.get_counts(rs)
        result_key = list(result.get_counts(rs).keys())
        temp_output = result_key[0]
        output += temp_output
        
    #return output clipped to size of desired string length
    return output[:n]


def makeKey(rotation1,rotation2,results):
    key = ''
    count = 0
    for i,j in zip(rotation1,rotation2):
        if i == j:
            key += results[count]
        count += 1
    return key


def key(): # Main function
    # Super secret message
    # print('Your super secret message: ',msg)

    # initial size of key
    # n = len(msg)*3
    n = 10

    # break up message into smaller parts if length > 10
    nlist = []
    for i in range(int(n/10)):
        nlist.append(10)
    if n%10 != 0:
        nlist.append(n%10)

    print(nlist)

    # print('Initial key length: ',n)



    key = randomStringGen(n)
    # print('Initial key: ',key)


    #generate random rotation strings for Alice and Bob
    Alice_rotate = randomStringGen(n)
    Bob_rotate = randomStringGen(n)
    print("Alice's rotation string:",Alice_rotate)
    # print("Bob's rotation string:  ",Bob_rotate)

    #start up your quantum program
    backend = Aer.get_backend('qasm_simulator')  
    shots = 1
    circuits = ['send_over']
    Bob_result = ''


    qcircuit_list = []

    for ind,l in enumerate(nlist):
        #define temp variables used in breaking up quantum program if message length > 10
        if l < 10:
            key_temp = key[10*ind:10*ind+l]
            Ar_temp = Alice_rotate[10*ind:10*ind+l]
            Br_temp = Bob_rotate[10*ind:10*ind+l]
        else:
            key_temp = key[l*ind:l*(ind+1)]
            Ar_temp = Alice_rotate[l*ind:l*(ind+1)]
            Br_temp = Bob_rotate[l*ind:l*(ind+1)]
        
        #start up the rest of your quantum circuit information
        q = QuantumRegister(l, name='q')
        c = ClassicalRegister(l, name='c')
        send_over = QuantumCircuit(q, c, name='send_over')
        
        #prepare qubits based on key; add Hadamard gates based on Alice's and Bob's
        #rotation strings
        for i,j,n in zip(key_temp,Ar_temp, range(0,len(key_temp))):
            i = int(i)
            j = int(j)
            if i > 0:
                send_over.x(q[n])
            #Look at Alice's rotation string
            if j > 0:
                send_over.h(q[n])

        qcircuit_list.append((q, c, send_over))


        #execute quantum circuit
        result_so = execute([send_over], backend, shots=shots).result()
        counts_so = result_so.get_counts(send_over)
        result_key_so = list(result_so.get_counts(send_over).keys())
        Bob_result += result_key_so[0][::-1]


    with open('laser.alice', 'wb') as file:
        pickle.dump(Alice_rotate, file)
        pickle.dump(Bob_rotate, file)
        pickle.dump(nlist, file)
        pickle.dump(qcircuit_list, file)



    
    Akey = makeKey(Bob_rotate,Alice_rotate,key)

    print("Alice's key:",Akey)

    return Akey