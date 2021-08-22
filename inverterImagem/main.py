from PIL import Image, ImageOps
import numpy as np
from numpy import asarray

def main():
	image = Image.open('imagem4.jpg')
	image = ImageOps.grayscale(image)
	npImage = np.array(image)
	npImage = (255 - npImage)
	image2 = Image.fromarray(npImage)
	image2.show()
	image2.save('imagem4_.jpg')


if __name__ == "__main__":
    main()
