import socket

# Create a stream based socket(i.e, a TCP socket)

# operating on IPv4 addressing scheme

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

 
# Bind and listen

serverSocket.bind(("192.168.43.208",9090));
# serverSocket.bind(("127.0.0.1",9090));

serverSocket.listen();
print("waiting.........")


# Accept connections

while(True):

    (clientConnected, clientAddress) = serverSocket.accept();

    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));


    dataFromClient = clientConnected.recv(1024);
    data = dataFromClient.decode();
    final = "How are you"
    # # Send some data back to the client
    #clientConnected.send(final.encode());
    data2 = data.strip()
    data2 = data.split("\n" and ",")
    print(data2);
   

    try:
        data2.remove('')
        data2.remove()
        data2.remove('\n')
    except:
        data2

    length_data = int(len(data2)/2);
    print(length_data)
    
    ap = []
    ssf = []
    for i in range(length_data):
        ap.append(data2[i])
        ssf.append(int(data2[i+length_data]))
    
    print("Data received by %s"%(clientAddress[0]))
    print(ap)
    print(ssf)
    
    

    #---------------------------------------------------------------------
    # server computation
    import subprocess
    import os
    import re
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pylab as plt
    from numpy import matrix, maximum

    r = matrix(ssf)
    print(r)
    count = len(ssf)

    association = []
    for j in range(count):
        if r[0,j] > 0:
            association.append((0,j))
    print('\nAssociation',association)

    # Goal is the final destination set for Q-learning
    goal = count+1
    MATRIX_SIZE = count+2

    # R is Reward matrix inintially set to -1
    R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
    R *= -1

    # pac is the list containing the number of packets encountered at each access point
    pac = []
    #-------------------------------------------------- Reading csv file for load information generated using Kali Linux
    train = pd.read_csv("myOutput-01.csv") 
    df = pd.DataFrame(train)
    for accesspoint in ap:
        packet = df.loc[df[' ESSID'] == accesspoint]
        packet = packet.head(1)
        load = packet[' # IV']
        strings = [str(integer) for integer in load.values.tolist()]
        a_string = "".join(strings)
        a_string = a_string + "0"
        an_integer = float(a_string)
        pac.append(an_integer)


    #------------------------------------------------- Normalization of data packets at each access point

    load = [] # it is the list containing normalised load
    print("Number of packets encountered ")
    print(pac)

    amin = min(pac)
    amax = 0
    for num in pac:
        if (amax is None or num > amax):
            amax = num
    # amax = max_value
    for i, val in enumerate(pac):
        try:
            pac[i] = (val-amin) / (amax-amin)
        except:
            pac[i]=0


    load = pac

    #------------------------------------------------ Assigning Rewards 
    for idx,point in enumerate(association):
        if pac[idx] > 0.75:
            packet = 0
        elif pac[idx] > 0.50:
            packet = 25
        elif pac[idx] > 0.25:
            packet = 50
        else:
            packet = 100 
        if r[point] >= 75:
            R[point[0],point[1]+1] = 100 + packet
        elif r[point] >= 50:
            R[point[0],point[1]+1] = 50 + packet
        elif r[point] < 50 :
            R[point[0],point[1]+1] = 0 + packet



    print('\nRewards\n')
    for i in range(1,count+2):
        R[i,count+1] = 150
    print(R)
    Q = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))

    # learning parameter
    gamma = 0.8

    initial_state = 1

    def available_actions(state):
        current_state_row = R[state,]
        av_act = np.where(current_state_row >= 0)[1]
        return av_act

    available_act = available_actions(initial_state) 
    def sample_next_action(available_actions_range):
        next_action = int(np.random.choice(available_act,1))
        return next_action

    action = sample_next_action(available_act)

    def update(current_state, action, gamma):
        
        max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
        
        if max_index.shape[0] > 1:
            max_index = int(np.random.choice(max_index, size = 1))
        else:
            max_index = int(max_index)
        max_value = Q[action, max_index]

        #   /----------------------------------------------------------Updation of Q-table
        
        Q[current_state, action] = R[current_state, action] + gamma * max_value


        if (np.max(Q) > 0):
            return(np.sum(Q/np.max(Q)*100))
        else:
            return (0)
        
    update(initial_state, action, gamma)

    # ----------------------------------------------------Training Stage
    scores = []
    for i in range(700):
        current_state = np.random.randint(0, int(Q.shape[0]))
        # print(current_state)
        available_act = available_actions(current_state)
        action = sample_next_action(available_act)
        score = update(current_state,action,gamma)
        scores.append(score)
        # print ('Score:', str(score))
        
    # --------------------------------------------Graph showing the scores for each iteration
    plt.figure(figsize=(8,6))
    plt.xlabel('Number of Epochs')
    plt.ylabel('score') 
    plt.plot(scores, label = 'score value')
    plt.legend(loc='best')
    plt.show()

    print("\nTrained Q matrix:\n")
    # print(Q)
    print(Q/np.max(Q)*100)
    print("\nload rewards\n")
    print(load)

    # Testing
    def walk(start,goal):
        current_state = start
        steps = [current_state]

        while current_state != goal:

            next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
            
            if next_step_index.shape[0] > 1:
                next_step_index = int(np.random.choice(next_step_index, size = 1))
            else:
                next_step_index = int(next_step_index)
            
            steps.append(next_step_index)
            current_state = next_step_index
                

        print("\nMost efficient Association:")
        
        steps 
        
        print ("src...dst", start, goal)

        if goal > start: 
            steps
            print(steps)
        else:
            steps.reverse()
            print(steps)
        return steps

    steps = walk(0,count+1)

    print(steps[1])

    index = steps[1]-1
    final= ap[index]
    final = final[1:]
    print("Connecting to Network")
    print(final)

    # # Send some data back to the client
    clientConnected.send(final.encode());
    clientConnected.close();
    print("\n\n==============================================================================================\n")