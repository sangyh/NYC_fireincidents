#A circular road has N positions labeled 0 through N−1 where adjacent positions are connected to each other and position N−1 is connected to 0. M cars start at position 0 through M−1 (inclusive). A car can make a valid move by moving forward one position (or goes from N-1 to 0) if the position it is moving into is empty. At each turn, only consider cars that have a valid move available and make one of the valid moves that you choose randomly with equal probability. After T rounds, we compute the average (A) and standard deviation (S) of the position of the cars.
import numpy as np 
import random
from matplotlib import pyplot as plt

def update_position(circle,pos,t,T,N):
	if t==T:
		return pos

	options=[]
	#access cars which are available to move
	if circle[0]==False and circle[N-1]==True:
			options.append(N-1)
	for i in range(1,N):
		if circle[i]==False and circle[i-1]==True:
			options.append(i-1) 

	if len(options)>0 :
		move=options[random.randint(0,len(options)-1)]
		#print(move)
		if move==N-1:
			new_pos=0
		else:
			new_pos=move+1

		circle[move]=False
		circle[new_pos]=True
		pos.append(new_pos)
	
	t+=1
	return(update_position(circle,pos,t,T,N))


def calc_stats(N,M,T,trials):
	position=[] #contains all chosen positions
	circle={} #contains status of availability of positions during simulation 
	options=[] #available options in each trial

	#true means occupied, false means empty
	for i in range(N):
		circle[i]=False #'free'

	for i in range(M):
		circle[i]=True #'occupied'
		position.append(i)
		
	A=[] #average of positions
	S=[] #standard deviation of positions
	
	for trial in range(trials):
		positions=update_position(circle,position,0,T,N)
		A.append(np.mean(positions))
		S.append(np.std(positions))

	return(A,S)

A,S=calc_stats(25,10,50,1000)

plt.plot(range(1000),A)
plt.show()

print(round(np.mean(A),10),round(np.std(A),10),round(np.mean(S),10),round(np.std(S),10))