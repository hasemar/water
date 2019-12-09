from Water import Pipe
   
# assign the flow you want to analyze in gallons per minute
flow = 300       # gpm
L = 100          # ft

# create the 2 pipe segments in the pipe network
pipe_1 = Pipe(length=60, size=4, kind='STEEL', sch=40)
pipe_2 = Pipe(length=20, size=2, kind='STEEL', sch=40)

# add fittings to the pipe segments 
pipe_1.fitting(fitting_type='elbow_90', con_type='standard_threaded', qty=2)
pipe_1.fitting('tee_through', 'standard_threaded', qty=1)
pipe_1.fitting('tee_branch', 'standard_threaded', qty=1)
pipe_1.fitting('valve', 'gate', qty=1)

pipe_2.fitting('elbow_90', 'standard_threaded', qty=2)

# apply the get_losses function to compute major and minor losses 
losses = pipe_1.get_losses(flow) + pipe_2.get_losses(flow)

TDH = L + losses 

print('Size Pump for {} gpm at {:.0f} feet of Head'.format(flow, TDH))

