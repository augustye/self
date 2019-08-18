import gym
import numpy as np
import os
from IPython import display
from PIL import Image

#sprite数据结构: 多个可能的造型，当前位置，当前造型，造型重叠判断

#obs shape: (210, 160, 3) min: 0 max: 232
env = gym.make("KungFuMaster-v0")
env.seed(0)

obs   = 0
count = 0
done  = True
hist  = []
for i in range(94):
	if done:
		env.reset()
	random_action = env.action_space.sample()
	new_obs, rew, done, info = env.step(random_action)
	if np.any(new_obs-obs):
		count += 1
		img = Image.fromarray(new_obs, 'RGB')
		print("i:%3d, count:%d"%(i,count))
		
		if len(hist) == 0:
			img.save('components_background.png')

		if len(hist) == 1:
			mask = Image.fromarray(np.minimum(new_obs-hist[0],1)*255, 'RGB').convert('1')
			mask.save('components_mask.png')

			sprite = Image.new("RGBA", img.size)
			sprite.paste(img, mask)
			sprite.save('components_sprite.png')

		if len(hist) == 2:
			mask = Image.fromarray(np.minimum(new_obs-hist[0],1)*255, 'RGB').convert('1')
			mask.save('components_mask2.png')

			sprite = Image.new("RGBA", img.size)
			sprite.paste(img, mask)
			sprite.save('components_sprite2.png')


		hist.append(new_obs)
		img.save(f'images_{count}.png')
	obs = new_obs
	#env.render()
env.close()


files = os.listdir(".")
files.sort()
for file in files:
  if file.endswith(".png"):
    with open(file,'rb') as f:
      print(file)
      display.display(display.Image(data=f.read()))
