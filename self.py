import gym
import numpy as np
import os
from PIL import Image,ImageChops
from IPython.display import display

IMAGES = 100
WIDTH  = 160
HEIGHT = 210

hist    = []
sprites = []

class Pose:
	def __init__(self, img, masks=[0,0,0,0]):
		self.img = img
		self.top_masked    = bool(masks[0])
		self.right_masked  = bool(masks[1])
		self.bottom_masked = bool(masks[2])
		self.left_masked   = bool(masks[3])

class Sprite:
	def __init__(self, poses=[]):
		self.poses = poses

def generate_images():
	env = gym.make("KungFuMaster-v0")
	env.seed(0)
	obs,done = 0,True
	frames,images = 0,0
	while images < IMAGES:
		if done:
			env.reset()
		random_action = env.action_space.sample()
		new_obs,_,done,_= env.step(random_action)
		if np.any(new_obs-obs):
			f,i = frames,images
			print("frame %05d, image %05d"%(f,i))
			img = Image.fromarray(new_obs, 'RGB')
			img.save('images/%05d.png'%(images))
			images += 1
		frames += 1
		obs = new_obs
	env.close()

def process_images():
	files = os.listdir('images')
	files.sort()
	for file in files:
		img = Image.open('images/'+file)
		obs = np.array(img)
		index = len(hist)
		hist.append(obs)	
		if index < 3:
			display(img)
			get_sprite(index, img)	

def get_sprite(index, img):
	
	if index > 0:
		diff = hist[index] - hist[0]
		diff = np.minimum(diff, 1)*255
		mask = Image.fromarray(diff, 'RGB')
		mask = mask.convert('1')
		img2 = Image.new("RGBA", img.size)
		img2.paste(img, mask)
		img  = img2
		
	bbox = img.getbbox()
	im = img.crop(bbox)
	print('bbox:',bbox)
	
	position = bbox[:2]
	print('position',position)
	
	l_masked = (bbox[0] == 0)
	t_masked = (bbox[1] == 0)
	r_masked = (bbox[2] == WIDTH)
	b_maksed = (bbox[3] == HEIGHT)
	masks  = [t_masked,r_masked,b_maksed,l_masked]
	pose   = Pose(im, masks)
	
	if index < 2:
		sprite = Sprite([pose])
		sprites.append(sprite)
	else:
		sprites[-1].poses.append(pose)

def show_sprites():
	print('sprites:')
	for i in range(1,len(sprites)):
		sprite = sprites[i]
		imgs = []
		height = 0
		width  = 0
		for pose in sprite.poses:
			w,h = pose.img.size
			height = max(height, h)
			width += w+10
		canvas = Image.new("RGBA", (width,height))
		x = 0		
		for pose in sprite.poses:
			w,h = pose.img.size
			canvas.paste(pose.img, (x,0,x+w,h))		
			x += w+10
		display(canvas)
																				
if __name__ == '__main__':
	print('version 12')
	#generate_images()
	process_images()
	show_sprites()

#生成world：(sprite id，pose id，position)列表
#为pose寻找已有的sprite id和pose id 


