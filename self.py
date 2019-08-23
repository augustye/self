import numpy as np
import os
from PIL import Image,ImageChops
from IPython.display import display

WIDTH   = 160
HEIGHT  = 210
hist    = []
sprites = []
worlds  = []

class Pose:
  def __init__(self,im,masks=None):
    m = masks or [0,0,0,0]
    self.img           = im
    self.top_masked    = bool(m[0])
    self.right_masked  = bool(m[1])
    self.bottom_masked = bool(m[2])
    self.left_masked   = bool(m[3])

class Sprite:
  def __init__(self, poses=[]):
    self.poses = poses

def process_images():
  files = os.listdir('images')
  files.sort()
  for file in files:
    path  = 'images/' + file
    img   = Image.open(path)
    obs   = np.array(img)
    index = len(hist)
    hist.append(obs)  
    if index < 3:
      display(img)
      get_world(index, img)  

def get_world(index, img):
  
  if index > 0:
    diff = hist[index] - hist[0]
    d    = np.minimum(diff, 1)*255
    mask = Image.fromarray(d,'RGB')
    mask = mask.convert('1')
    size = img.size
    img2 = Image.new("RGBA",size)
    img2.paste(img, mask)
    img  = img2

  bbox = img.getbbox()
  im = img.crop(bbox)
  print('bbox:',bbox)
  
  x,y = bbox[:2]
  print('position',x,y)
  
  l = (bbox[0] == 0)
  t = (bbox[1] == 0)
  r = (bbox[2] == WIDTH)
  b = (bbox[3] == HEIGHT)
  masks = [t,r,b,l]
  pose  = Pose(im, masks)
    
  if index == 0:
    sid, pid = find_sprite(pose)
    item  = [sid,pid,x,y]
    world = [item]

  if index == 1:
    sid, pid = find_sprite(pose)
    item  = [sid,pid,x,y]
    world = [item]
    world = [worlds[0][0], item]

  if index == 2:
    sid, pid = find_sprite(pose)
    item  = [sid,pid,x,y]
    world = [item]
    world = [worlds[0][0], item]
  
  worlds.append(world)
  print('world:', world)

def find_sprite(pose):
  for s in sprites:
    sid = sprites.index(s)
    for p in s.poses:
      pid = s.poses.index(p)
      if pose.img == p.img:
        return sid,pid
  sprite = Sprite([pose])
  sprites.append(sprite)
  return len(sprites)-1, 0
 
def show_sprites():
  print('sprites:')
  for i in range(len(sprites)):
    sprite = sprites[i]
    imgs = []
    height = 0
    width  = 0
    for pose in sprite.poses:
      w,h = pose.img.size
      height = max(height, h)
      width += w+10
    size = (width,height)
    canvas = Image.new("RGBA",size)
    x = 0    
    for pose in sprite.poses:
      w,h = pose.img.size
      area = (x, 0, x+w, h)
      canvas.paste(pose.img, area)    
      x += w+10
    file = 'sprite_%03d.png'%(i)
    print('saved:', file)
    canvas.save(file)
    display(canvas)
                                        
if __name__ == '__main__':
  print('version 1')
  process_images()
  show_sprites()


 