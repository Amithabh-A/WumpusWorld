"""
4 5     # number of rows and cols
A 4 0   # agent starting coordinates
W 1 0   # wumpus coordinates
G 1 1   # gold coordinates
P 0 3   # 1st pit coordinates
P 1 2   # 2nd pit coordinates
P 3 2   # 3rd pit coordinates
"""

class File_Parser:
    def __init__(self, world_file):
        self.row_col = []
        self.agent = []
        self.wumpus = []
        self.gold = []
        self.pits = [[]]
        self.agent_index = -1
        self.wumpus_index = -1
        self.gold_index = -1
        self.pits_index = []

        file = open(world_file, 'r')

        self.row_col = file.readline()
        self.row_col = self.row_col.rstrip('\r\n')
        self.row_col = self.row_col.split(" ")
        # print(self.row_col)

        self.agent = file.readline()
        self.agent = self.agent.rstrip('\r\n')
        self.agent = self.agent.split(" ")
        # print(self.agent)

        self.wumpus = file.readline()
        self.wumpus = self.wumpus.rstrip('\r\n')
        self.wumpus = self.wumpus.split(" ")
        # print(self.wumpus)

        self.gold = file.readline()
        self.gold = self.gold.rstrip('\r\n')
        self.gold = self.gold.split(" ")
        # print(self.gold)

        self.pits = []

        while True:
            pit = file.readline()
            if len(pit) == 0:
                break
            pit = pit.rstrip('\r\n')
            pit = pit.split(" ")

            self.pits.append(pit)
        
        self.converter()

    def converter(self):
        self.agent_index = int(self.row_col[0])*int(self.agent[1]) + int(self.agent[2])
        self.wumpus_index = int(self.row_col[0])*int(self.wumpus[1]) + int(self.wumpus[2])
        self.gold_index = int(self.row_col[0])*int(self.gold[1]) + int(self.gold[2])
        for i in range(len(self.pits)):
            index = int(self.row_col[0])*int(self.pits[i][1]) + int(self.pits[i][2])
            self.pits_index.append(index)

#file_parser = File_Parser("world.txt")
#print(file_parser.agent_index, file_parser.wumpus_index, file_parser.gold_index, file_parser.pits_index)