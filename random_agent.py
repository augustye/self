import gym
import numpy as np
from PIL import Image

#obs shape: (210, 160, 3) min: 0 max: 232
env = gym.make("KungFuMaster-v0")
env.seed(0)

obs   = 0
count = 0
done  = True
imgs  = []
for i in range(93):
	if done:
		env.reset()
	random_action = env.action_space.sample()
	new_obs, rew, done, info = env.step(random_action)
	diff = new_obs-obs
	if np.any(diff):
		count += 1
		img = Image.fromarray(new_obs, 'RGB')
		print("i:%3d, count:%d"%(i,count))
		if len(imgs) == 0:
			img.save('components/background.png')
		else:
			mask = Image.fromarray(np.minimum(diff,1)*255, 'RGB').convert('1')
			mask.save('components/mask.png')

			sprite = Image.new("RGBA", img.size)
			sprite.paste(img, mask)
			sprite.save('components/sprite.png')

		imgs.append(img)
		img.save(f'images/{count}.png')
	obs = new_obs
	env.render()
env.close()
