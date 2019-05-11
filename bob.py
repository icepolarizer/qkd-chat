#other useful packages
import math
import matplotlib.pyplot as plt
import numpy as np

# Import Qiskit
from qiskit import Aer, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

import pickle



# Make random strings of length string_length

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
    with open('bob.laser', 'rb') as file:
        Alice_rotate = pickle.load(file)
        Bob_rotate = pickle.load(file)
        nlist = pickle.load(file)
        qcircuit_list = pickle.load(file)

    print(nlist)


    #start up your quantum program
    backend = Aer.get_backend('qasm_simulator')
    shots = 1
    circuits = ['send_over']
    Bob_result = ''

    for ind,l in enumerate(nlist):
        #define temp variables used in breaking up quantum program if message length > 10
        if l < 10:
            Br_temp = Bob_rotate[10*ind:10*ind+l]
        else:
            Br_temp = Bob_rotate[l*ind:l*(ind+1)]

        #start up the rest of your quantum circuit information
        q = qcircuit_list[ind][0]
        c = qcircuit_list[ind][1]
        send_over = qcircuit_list[ind][2]

        #prepare qubits based on key; add Hadamard gates based on Alice's and Bob's
        #rotation strings

        #Look at Bob's rotation string
        for k,n in zip(Br_temp,range(0, l)):
            k = int(k)
            if k > 0:
                send_over.h(q[n])
            send_over.measure(q[n],c[n])

        #execute quantum circuit
        result_so = execute([send_over], backend, shots=shots).result()
        counts_so = result_so.get_counts(send_over)
        result_key_so = list(result_so.get_counts(send_over).keys())
        Bob_result += result_key_so[0][::-1]

    print("Bob's results:          ", Bob_result)






    Bkey = makeKey(Bob_rotate,Alice_rotate,Bob_result)

    print("Bob's key:  ",Bkey)

    return Bkey