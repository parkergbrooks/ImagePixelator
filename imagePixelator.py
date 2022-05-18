import numpy as np
import sys
import os
from PIL import Image


def main(imgName):
    #np.set_printoptions(threshold=sys.maxsize) #DEBUG PRINT LINE SETTING

    cwd = os.path.dirname(os.path.realpath(__file__))
    imgDir = cwd+'\\'+imgName
    img = np.array(Image.open(imgDir))

    pic = img
    orig_width = pic.shape[0]
    orig_height = pic.shape[1]


    target_height, target_width,scale_height,scale_width = getHeightWidthAndScales(orig_height,orig_width)


    target_image = Image.new('RGB',(target_width,target_height),"white")
    
    for x in range(target_width):
        for y in range(target_height):
            rgb = getPixelForChunk(x,y,scale_height,scale_width,orig_width,orig_height,img)
            target_image.putpixel((x,y),(rgb[0],rgb[1],rgb[2]))
            
    target = target_image.save("target.png")
    
    pixel_match_answer = input("Should you like to color match this image? (y/n) ")
    
    if pixel_match_answer == 'y':
        knn_pixel_match(target_image)
    

def knn_pixel_match(image):
    simple_rainbow = [(255, 0 , 0),(255, 127, 0),(255, 255, 0),(0, 255, 0),(0, 0, 255),(75, 0, 130),(148, 0, 211),(255,255,255),(0,0,0)]
    gray_monochrome = [(103, 104, 103),(119, 120, 119),(144, 144, 144),(170, 170, 170),(188, 188, 188),(212, 212, 212)]
    large_color_set = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(192,192,192),(240,128,128),(0,0,128),(128,0,128),(124,252,0),(0,100,0),(0,191,255),(0,0,128),(255,0,255),(139,69,19),(255,255,255),(0,0,0)]
    colors = print_list_palette()
    palette = simple_rainbow
    if colors == 1:
        #print(simple_rainbow)
        palette = simple_rainbow
    if colors == 2:
        #print(gray_monochrome)
        palette = gray_monochrome
    if colors == 3:
        #print(large_color_set)
        palette = large_color_set
    
    img_array = np.asarray(image)
    width = img_array.shape[0]
    height = img_array.shape[1]
    
    for x in range(width):
        for y in range(height):
            pixel = calculate_knn_pixel(x,y,palette,image)
            image.putpixel((x,y),(pixel))
            
    target = image.save("targetCorrected.png")
    
def calculate_knn_pixel(x,y,palette,image):
    
    img_pixel = image.getpixel((x,y))
    #print("calculate KNN Pix")
    best_val = 10000
    val_index = -1
    count = 0
    
    for item in palette:
        knn_sum = abs(np.sum(np.subtract(item , img_pixel)))
        #print(knn_sum)
        if knn_sum < best_val:
            val_index = count
            best_val = knn_sum
        count = count + 1     
    
    #print(val_index)
    return palette[val_index]


def print_list_palette():
    print("""\nWhich color palette should be used on image\n
             1. Simple Rainbow\n
             2. Gray Monochromatic\n
             3. Large Color Set\n
          """)
    selection = input()
    return int(selection)
    
def getPixelForChunk(start_x, start_y, scale_height, scale_width,orig_width,orig_height,img):
    
    x = (start_x * scale_width) + start_x
    y = (start_y * scale_height) + start_y
    finish_x = x + scale_width
    finish_y = y + scale_height
    
    if finish_x > orig_width:
        finish_x = orig_width
    if finish_y > orig_height:
        finish_y = orig_height
        
    x_count = finish_x-x
    y_count = finish_y-y
    if x_count == 0:
        x_count = 1
    if y_count == 0:
        y_count = 1
        
    imgArray = np.asarray(img)
    #average once to get average of all pixels in the col of pixels
    #average again to get the total average of pixels
    pixel = np.average(np.average(imgArray[y:finish_y,x:finish_x],axis=0),axis=0)
    
    #Cast to int to get rid of float decimals for to get rough RGB value
    pix = pixel.astype(int)
    
    
    #-----Debug To Check Pixel Value-----#
    #print(pix)
    
    
    return pix

    
def getHeightWidthAndScales(orig_height,orig_width):
    
    target_height = int(input("Enter Target Height: "))
    target_width = int(input("Enter Target Width: "))
    h_w_check = 0
    while h_w_check == 0:
        if target_height > orig_height:
         target_height = int(input("Target Height greater than original image. Enter Smaller Target Height: "))
        if target_width > orig_width:
         target_width = int(input("Target Width greater than original image. Enter Smaller Target Width: "))
        if target_height < orig_height and target_width < orig_width:
          h_w_check = 1
          
    scale_height = (orig_height)//(target_height)
    scale_width = (orig_width)//(target_width)


    max_new_width = orig_width // (scale_width + 1)
    max_new_height = orig_height // (scale_height+1)

    if target_height > max_new_height:
        target_height = max_new_height
        print("Target height would lead to blackspace in image.\nCropping to new height:",target_height)
    if target_width > max_new_width:
        target_width = max_new_width
        print("Target width would lead to blackspace in image.\nCropping to new width:",target_width)   
          
    return target_height, target_width, scale_height, scale_width




if __name__ == "__main__":
    
    if(len(sys.argv) > 1):
      imgName = str(sys.argv[1])
      main(imgName)
    else:
        print("filename expected in command line\nTry running: (imagePixelator.py) imageFileName")
      
    
    
