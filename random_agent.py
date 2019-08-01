import gym
import numpy as np
from PIL import Image

#obs shape: (210, 160, 3) min: 0 max: 232
env = gym.make("KungFuMaster-v0")
env.seed(0)

obs   = 0
count = 0
done  = True
for i in range(100):
	if done:
		env.reset()
	random_action = env.action_space.sample()
	new_obs, rew, done, info = env.step(random_action)
	if np.any(new_obs - obs):
		count += 1
		img = Image.fromarray(new_obs, 'RGB')
		img.save(f'images/{count}.png')
	obs = new_obs
	env.render()
env.close()
