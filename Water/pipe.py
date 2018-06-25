'''
Pipe Class
   
'''
from __future__ import print_function

class Pipe:

    def __init__(self, kind, grade):
        self.kind = kind
        self.grade = grade
        self.length = 0

    def set_length(self, length):
        self.length = length

if __name__=="__main__":
    print('test script:')

    pipe_1 = Pipe('kind', 'grade')
    pipe_1.set_length(10)

    print(pipe_1.length) 

    '''
    Notes:  Make this class a super class for fittings to inherent pipe size and type
    This class will also be a subclass of losses class
    '''