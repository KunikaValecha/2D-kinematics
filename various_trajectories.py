import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from bicycle import Bicycle
import argparse

parser = argparse.ArgumentParser(description='2D trajectories of two wheeled vehicle')
parser.add_argument('--trajectory',      type=str, default='square')
args = parser.parse_args()

sample_time = 0.01
time_end = 60
model = Bicycle()
model.reset()


t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)


# maintain velocity at 4 m/s
v_data = np.zeros_like(t_data)
v_data[:] = 4 

w_data = np.zeros_like(t_data)

# ==================================
#  Square Path: set w at corners only
# ==================================
if (args.trajectory == 'square'):
	w_data[670:670+100] = 0.753
	w_data[670+100:670+100*2] = -0.753
	w_data[2210:2210+100] = 0.753
	w_data[2210+100:2210+100*2] = -0.753
	w_data[3670:3670+100] = 0.753
	w_data[3670+100:3670+100*2] = -0.753
	w_data[5220:5220+100] = 0.753
	w_data[5220+100:5220+100*2] = -0.753

# ==================================
#  Spiral Path: high positive w, then small negative w
# ==================================
elif(args.trajectory == 'spiral'):
	w_data[:] = -1/100
	w_data[0:100] = 1

# ==================================
#  Wave Path: square wave w input
# ==================================
elif(args.trajectory=='squarewave'):
	w_data[:] = 0
	w_data[0:100] = 1
	w_data[100:300] = -1
	w_data[300:500] = 1
	w_data[500:5700] = np.tile(w_data[100:500], 13)
	w_data[5700:] = -1

# ==================================
#  Triangular Path: equilateral triangle w input
# ==================================

elif(args.trajectory == 'equilateral'):

	w_data[1000:1000+100]=0.98
	w_data[1000+100:1000+100*2]=-0.98
	w_data[3000:3000+100]=0.98
	w_data[3000+100:3000+100*2]=-0.98
	w_data[5000:5000+100]=0.98
	w_data[5000+100:5000+100*2]=-0.98

for i in range(t_data.shape[0]):
    x_data[i] = model.xc
    y_data[i] = model.yc
    model.step(v_data[i], w_data[i])

# ==================================
#  Circular Path: circular w input
# ==================================

if(args.trajectory == 'circle'):
	sample_time = 0.01
	time_end = 20
	model.reset()
	

	t_data = np.arange(0,time_end,sample_time)
	x_data = np.zeros_like(t_data)
	y_data = np.zeros_like(t_data)
	
	for i in range(t_data.shape[0]):
	    x_data[i] = model.xc
	    y_data[i] = model.yc
	    
	    if model.delta < np.arctan(2/10):
	        model.step(np.pi, model.w_max)
	    else:
	        model.step(np.pi, 0)
	        
	    

# ==================================
#  Eight Path: eights w input
# ==================================



if(args.trajectory == 'eight'):
	time_end = 30
	t_data = np.arange(0,time_end,sample_time)
	x_data = np.zeros_like(t_data)
	y_data = np.zeros_like(t_data)
	w_data = np.zeros_like(t_data)

	v_data = np.zeros_like(t_data)
	v_data[:] = (16 * np.pi)/15
	
	model.xc = 0
	model.yc = 0
	for i in range(t_data.shape[0]):
	    x_data[i] = model.xc
	    y_data[i] = model.yc
	    
	    if i < 352 or i > 1800:
	        if model.delta < np.arctan(2/8):
	            model.step(v_data[i], model.w_max)
	            w_data[i] = model.w_max
	        else:
	            model.step(v_data[i], 0)
	            w_data[i] = 0
	    else:
	        if model.delta > -np.arctan(2/8):
	            model.step(v_data[i],-model.w_max)
	            w_data[i] = -model.w_max
	        else:
	            model.step(v_data[i],0)
	            w_data[i] = 0

# ==================================
#  Step through bicycle model
# ==================================
# for i in range(t_data.shape[0]):
#     x_data[i] = model.xc
#     y_data[i] = model.yc
#     model.step(v_data[i], w_data[i])

    
plt.axis('equal')
plt.plot(x_data, y_data,label='Desired Trajectory')
plt.savefig("trajectories" + "/" + args.trajectory + ".png")
plt.legend()
plt.show()
