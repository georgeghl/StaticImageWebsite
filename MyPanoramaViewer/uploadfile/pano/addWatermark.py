import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import logging
import threading

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

fileFolder = ""
positionFlag = 0
text = ""
alphavalue = 0.01
threadCnt = 1

def textMark(img):
    # try:
        im = Image.open(img).convert('RGBA')
        newImg = Image.new('RGBA', im.size, (255, 255, 255, 0))
        imagedraw = ImageDraw.Draw(newImg)
        imgwidth, imgheight = im.size
        font = ImageFont.truetype(r'JosefinSlab-Bold.ttf', int(imgwidth / 10))
        txtwidth = font.getsize(text)[0]
        txtheight = font.getsize(text)[1]

        if positionFlag == 0:
            position = (0, 0)
        elif positionFlag == 1:
            position = (0, imgheight - txtheight)
        elif positionFlag == 2:
            position = (imgwidth - txtwidth, 0)
        elif positionFlag == 3:
            position = (imgwidth - txtwidth, imgheight - txtheight)
        elif positionFlag == 4:
            position = (imgwidth / 2, imgheight / 2)

        imagedraw.text(position, text, font=font, fill="black")
        alpha = newImg.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(alphavalue)
        newImg.putalpha(alpha)
        # Composite images and convert to RGB mode before saving as JPEG
        result_img = Image.alpha_composite(im, newImg).convert("RGB")
        result_img.save(img, 'JPEG')
    # except Exception as e:
        # logging.error(e)

def processImg(ip: str):
    logging.info("Process Image: " + ip)
    if ip.endswith("jpg"):
        logging.debug("This is a jpg file.")
        logging.debug("Adding at: " + str(positionFlag) + " with text: " + text)
        textMark(ip)

def processPath(pth):
    logging.debug("Process path: " + pth)
    files = os.listdir(path=pth)
    for i in files:
        tmp = pth + "/" + i
        logging.debug("Current file pointer: " + tmp)
        if not os.path.isdir(tmp):
            processImg(tmp)
        else:
            processPath(tmp)

def processFolder(files):
    for file in files:
        fullPath = os.path.join(fileFolder, file)  # 获取完整路径
        if os.path.isdir(fullPath):
            processPath(fullPath)
        else:
            processImg(fullPath)


def main():
    global fileFolder, positionFlag, text, alphavalue, threadCnt
    while True:
        fileFolder = input("Input folder: ")
        if os.path.exists(fileFolder):
            break
        else:
            print("Folder does not exist. Please enter a valid folder path.")

    positionFlag = int(input("Input position (0: top left, 1: bottom left, 2: top right, 3: bottom right, 4: center): "))
    text = input("Input text: ")
    alphavalue = float(input('Input watermark transparency (between 0 and 1): '))
    threadCnt = int(input("Input thread count: "))  # Input the number of threads
    logging.debug("fileFolder: " + fileFolder + ", position" + str(positionFlag) + ", text:" + text)

    # 获取文件列表
    files = os.listdir(fileFolder)

    # 分割文件列表以便并行处理
    file_chunks = [files[i:i + threadCnt] for i in range(0, len(files), threadCnt)]

    # 创建并启动线程
    threads = []
    for chunk in file_chunks:
        thread = threading.Thread(target=processFolder, args=(chunk,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()


