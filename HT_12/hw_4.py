class CntInstance:
    cnt = 0

    def __init__(self):
        CntInstance.cnt +=1
    
    def check_cnt(self):
        print(CntInstance.cnt)


a = CntInstance()
b = CntInstance()
b.check_cnt() #2
c = CntInstance()
c.check_cnt() #3
c.check_cnt() #3
CntInstance().check_cnt() #4
