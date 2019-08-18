import os
import numpy as np
from PIL import Image

files = os.listdir("images")
files.sort()

hist  = []
for file in files:
	img = Image.open("images/"+file)
	new_obs = np.array(img)
	hist.append(new_obs)

	if len(hist) == 1:
		img.save('components/background.png')

	elif len(hist) == 2:
		mask = Image.fromarray(np.minimum(new_obs-hist[0],1)*255, 'RGB').convert('1')
		mask.save('components/mask.png')

		sprite = Image.new("RGBA", img.size)
		sprite.paste(img, mask)
		sprite.save('components/sprite.png')

	elif len(hist) == 3:
		mask = Image.fromarray(np.minimum(new_obs-hist[0],1)*255, 'RGB').convert('1')
		mask.save('components/mask2.png')

		sprite = Image.new("RGBA", img.size)
		sprite.paste(img, mask)
		sprite.save('components/sprite2.png')

	else:
		break

	