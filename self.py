import gym
import numpy as np
import os
from PIL import Image

IMAGES = 4
WIDTH  = 210
HEIGHT = 160
hist  = []

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
			img.save('images_%05d.png'%(images))
			images += 1
		frames += 1
		obs = new_obs
	env.close()

def process_images():
	files = os.listdir('.')
	files.sort()
	for file in files:
		if file.startswith('images_'):
				img = Image.open(file)
				obs = np.array(img)
				index = len(hist)
				hist.append(obs)	
				process_image(index, img)

def save_background(index, img):
	img.save('components_background.png')

def save_sprite(index, img):
	diff = hist[index] - hist[0]
	diff = np.minimum(diff, 1)*255
	mask = Image.fromarray(diff, 'RGB')
	mask = mask.convert('1')
	mask.save('components_mask%d.png'%(index))

	sprite = Image.new("RGBA", img.size)
	sprite.paste(img, mask)
	sprite.save('components_sprite%d.png'%(index))

def process_image(index, img):
			
	if index == 0:
		save_background(index, img)

	if index == 1:
		save_sprite(index, img)

	if index == 2:
		save_sprite(index, img)
					
def show_images():
	from IPython import display as d
	files = os.listdir(".")
	files.sort()
	for file in files:
		if file.endswith(".png"):
			with open(file,'rb') as f:
				print(file)
				d.display(d.Image(data=f.read()))
				
if __name__ == '__main__':
	generate_images()
	process_images()
	show_images()
	
#sprite数据结构: 造型列表，x/y，遮挡标志，当前造型id
#sprite造型重叠判断

		

