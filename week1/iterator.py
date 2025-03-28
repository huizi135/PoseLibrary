class CountDown:
    def __init__(self, maxNumber):
        self.current = MaxNumber
        #self.current = maxNumber if maxNumber % 2 ==1 else maxNumber =1 #ensure start from an odd number
        self.stop = 0
        
    def __iter__(self):
        return  self
    
    def __next__(self):
        if self.current < self.stop:
            raise StopIteration
    #get next odd value
    x = self.current
    self.current = 1
    return x
    
    def isDone(self):
        return self.current < self.stop
    
A = CountDown(10)
while not A.isDone():
    print(next(A))