import gym
import numpy as np
import os
from PIL import Image
from IPython import display

WIDTH  = 210
HEIGHT = 160
hist  = []

def generate_images():
	env = gym.make("KungFuMaster-v0")
	env.seed(0)
	obs   = 0
	count = 0
	done  = True
	for i in range(94):
		if done:
			env.reset()
		random_action = env.action_space.sample()
		new_obs, rew, done, info = env.step(random_action)
		if np.any(new_obs-obs):
			count += 1
			img = Image.fromarray(new_obs, 'RGB')
			print("i:%3d, count:%d"%(i,count))
			img.save('images_%05d.png'%(count))
		obs = new_obs
	env.close()

def process_images():
	files = os.listdir('.')
	files.sort()
	for file in files:
		if file.startswith('images_'):
				img = Image.open(file)
				process_image(img)

def get_background(count, new_obs, img):
	img.save('components_background.png')

def get_sprite(count, new_obs, img):
	mask = Image.fromarray(np.minimum(new_obs-hist[0],1)*255, 'RGB').convert('1')
	mask.save('components_mask%d.png'%(count))

	sprite = Image.new("RGBA", img.size)
	sprite.paste(img, mask)
	sprite.save('components_sprite%d.png'%(count))


def process_image(img):
	new_obs = np.array(img)
	count = len(hist)
	hist.append(new_obs)	
			
	if count == 0:
		get_background(count, new_obs, img)

	if count == 1:
		get_sprite(count, new_obs, img)

	if count == 2:
		get_sprite(count, new_obs, img)
					
def show_images():
	files = os.listdir(".")
	files.sort()
	for file in files:
	  if file.endswith(".png"):
	    with open(file,'rb') as f:
	      print(file)
	      display.display(display.Image(data=f.read()))

#sprite数据结构: 多个可能的造型，当前位置，当前造型，造型重叠判断
generate_images()
process_images()
show_images()
	


		

