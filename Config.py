import numpy as np
class config1:
    Safe_points=list(np.zeros(16))
    stink_points=list(np.zeros(16))
    breeze_points=list(np.zeros(16))
    wumpus_pos=[5]
    pit_pos=[7,15]
    reward_pos=[2,4]
    def __init__(self):
        for i in self.wumpus_pos:
            if i+1<17 and (i)//4==(i-1)//4:
                self.stink_points[i]=1
            if i-1>0 and (i-2)//4==(i-1)//4:
                self.stink_points[i-2]=1
            if i+4<17:
                self.stink_points[i+3]=1
            if i-4>0:
                self.stink_points[i-5]=1
        for i in self.pit_pos:
            if i+1<17 and (i)//4==(i-1)//4:
                self.breeze_points[i]=1
            if i-1>0 and (i-2)//4==(i-1)//4:
                self.breeze_points[i-2]=1
            if i+4<17:
                self.breeze_points[i+3]=1
            if i-4>0:
                self.breeze_points[i-5]=1
        for i in range(len(self.Safe_points)):
            if (i+1 not in self.wumpus_pos) and (i+1 not in self.pit_pos):
                self.Safe_points[i]=1


    
