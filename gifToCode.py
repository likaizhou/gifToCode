# 将gif动图转为无背景的gif字符动图
# 参考网上部分开源代码

from PIL import Image, ImageSequence, ImageDraw
import os

# 待读取的动图
img = Image.open('C:/项目/暑期实习/代码/4.gif')
# 调整大小
img.resize((150, 150))
# 宽高
w, h = img.size
# 读取动图各个帧
iter = ImageSequence.Iterator(img)
# 拷贝，并转成RGB图
imgs = [frame.copy().convert('RGB') for frame in iter]
# 设定字符
s = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 将像素映射为字符
def pixel_to_char(p, alpha=256):
    r = p[0]
    g = p[1]
    b = p[2]
    if alpha == 0:
        return ""
    length = len(s)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256. + 1) / length
    return s[int(gray / unit)]

# 将图像改为透明背景（png）
def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = img.getpixel((0,0))
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,color_1)
    return img

# 将图片转为字符图
def changeImg(img, index):
    # 图像像素数组
    # data=np.array(img)
    # 开始创建字符图了
    new_img = Image.new('1', (2 * w, 2 * h), color=255)  # 生成白色背景图片
    draw = ImageDraw.Draw(new_img)
    # 高为行，宽为列，每隔5个取一次像素
    for i in range(0, h, 5):
        for j in range(0, w, 5):
            ch = pixel_to_char(img.getpixel((j, i)))
            # 松散一些较好看
            draw.text((2 * j, 2 * i), ch)
    new_img = transparent_back(new_img) # 转为透明背景的png格式
    # 保存字符图
    new_img.save('C:/项目/暑期实习/代码/gif-temp/%d.png' % index) # 存储到临时文件夹

# 字符图存储
idx = 0
for frame in imgs:
    changeImg(frame, idx)
    idx += 1

# 创建gif
img_list = []
#获取保存的PNG图像
pic_list = os.listdir("C:/项目/暑期实习/代码/gif-temp")
for k in pic_list:
    pic_p = Image.open("C:/项目/暑期实习/代码/gif-temp/{}".format(k))
    img_list.append(pic_p)
#保存图像
img_list[0].save("C:/项目/暑期实习/代码/2-1.gif", save_all=True, append_images=img_list[1:],duration=80,transparency=0,loop=0,disposal=3) # 通过duration控制gif频率
