from PIL import Image,ImageFilter

before = Image.open('c:/Users/mudda/OneDrive/Desktop/2.jpg')
after = before.filter(ImageFilter.FIND_EDGES)
after.save('img.jpg')

