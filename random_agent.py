import gym
import numpy as np
from PIL import Image,ImageChops

IMAGES = 100

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

if __name__ == '__main__':
  generate_images()