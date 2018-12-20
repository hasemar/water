'''
straight length object for pipes
'''
from __future__ import print_function

class straight_pipe(Pipe):

    def __init__(self, size, kind='PVC', sch='C900 DR-18', length):
        super(straight_pipe, self).__init__(size, kind='PVC', sch='C900 DR-18')
        self.kind = kind
        self.sch = sch
        self.size = pipe_dims[sch][size]
        self.length = length
        self.c_factor = c_dict[kind]
        self.h_loss = None

    
    def head_loss(self, flow):
        '''
        uses Hazen-Williams equation to find major losses in pipe
        Enter flow in gpm, returns loss in ft of head
        '''
        num = 4.52 * flow**1.852 * self.length
        den = self.c_factor**1.852 * self.inner_diameter**4.8704
        self.h_loss = (num/den) * .43333333
        
        return self.h_loss
