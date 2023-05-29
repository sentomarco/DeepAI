import imageio as iio
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from skimage.transform import resize



#path is a string, return the image as a pixel array 1 if the pixel is white | 0 if the pixel is colored 
def convert(in_dim, out_dim, path):

	# load an example image
	try:
		img = iio.imread(path)	
	except:
		print(sys.stderr, "\n\nError opening " + path +"\n\n")
		f_error=True
		
	#A matrix, normally read row per row, each element of the row is a 3 byte array RGB 0-255 [R G B], a 3 byte array for each pixel
	#so a 16x16 image has 16 array of 3 byte each row 
	
	if ( len(img)!=in_dim or len(img[0])!=in_dim ): 
		print(sys.stderr, "Error: image dimension incorrect.")
		f_error=True

	arr_input=np.zeros((in_dim,in_dim,1))
	index=0
	x,y = 0,0
	
	#print(img.shape)
	for row in img: 
		#print(row)
		x=0
		for pixel in row:
		
			BW_conversion=int(pixel[0])+int(pixel[1])+int(pixel[2])
			
			if( BW_conversion<0 or BW_conversion>255*3 ):
				print(sys.stderr, "Error: image format incorrect. Only 1 byte RGB pixel are valid.")
				f_error=True
			else:
				if (BW_conversion<100): arr_input[y][x][0]=1 #1 nero, no colore
				else: arr_input[y][x][0]=0		     #0 bianco, tutti colori
				
				index+=1
			x+=1
		y+=1
			

	# Scale the array to 180x180x1
	new_shape = (out_dim, out_dim, 1)
	scaled_arr = resize(arr_input, new_shape, anti_aliasing=True)
	
	#plt.imshow(scaled_arr[:,:,0])
	#plt.show()
	
	return scaled_arr



FIRST_P=True
fig, ax, r1 =0,0,0

def update_plot(image, pos, direction, dim, goal_pos ):
	
	global FIRST_P, fig, ax, r1
	
	if not FIRST_P: 
		#fig.clear() # cancella il grafico precedente
		r1.remove()
	else: 
		FIRST_P=False
		fig, ax = plt.subplots()
			
	image[goal_pos[0],goal_pos[1]]=0.5
	ax.imshow(image)
		
	r1 = patches.Rectangle((0,0), dim, dim, color="red", alpha=0.50)

	x=pos[0]
	y=pos[1]
	
	
	ax.add_patch(r1)



	t1 = Affine2D().rotate_deg_around(dim/2,dim/2,direction) + Affine2D().translate(x-dim/2, y-dim/2) + ax.transData
	r1.set_transform(t1)
	
	
	plt.grid(True)
	plt.show(block=False)
	plt.pause(0.001)
	


if __name__ == '__main__' :
	DIM=30
	OUT=180
	img=convert(DIM, OUT, "./env/room1.png")
	update_plot(img, (25,20), 30, 5)
	update_plot(img, (30,20), 60, 5)
	update_plot(img, (95,95), 60, 5)
	#plt.imshow(img)
	#plt.show()






