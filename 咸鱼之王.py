import pyautogui
import time
import os
from PIL import Image

# 屏幕分辨率 1920x1080
screen_width, screen_height = pyautogui.size()  # 获取屏幕分辨率
game_width = screen_width // 3  # 游戏占据屏幕的三分之一
game_x = screen_width - game_width  # 游戏窗口紧靠屏幕的右侧
game_y = 0  # 游戏窗口从屏幕顶部开始
game_height = screen_height  # 游戏高度占满屏幕的高度

# 图片路径"C:\\Users\\Dogfun\\Desktop\\png\\"
image_folder = "C:\\Users\\Dogfun\\Desktop\\png\\"  # 请替换为你存放截图的文件夹路径
image_names_1 = ["fight.png", "skip.png", "next.png"]  # 1关按钮顺序
image_names_2_9 = ["skip.png", "next.png"]  # 2-9关按钮顺序
image_names_10 = ["skip.png", "sure.png", "reward.png", "return.png", "nextpower.png", "goon.png"]  # 10关按钮顺序


def preprocess_image(image_path):
    """对图片进行灰度化预处理"""
    image = Image.open(image_path).convert('L')  # 转为灰度图
    preprocessed_image_path = image_path.replace(".png", "_grayscale.png")
    image.save(preprocessed_image_path)
    return preprocessed_image_path


def find_and_click(image_path, confidence=0.9):  # 提高 confidence 参数
    try:
        # 如果图像是灰度图，使用灰度图进行查找
        if image_path.endswith(".png"):
            image_path = preprocess_image(image_path)

        print(f"查找图片: {image_path}")
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence,
                                                  region=(game_x, game_y, game_width, game_height))
        if location:
            pyautogui.click(location)  # 点击找到的位置
            print(f"点击位置：{location}")
            return True
        else:
            print(f"未找到图片: {image_path}")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False


def play_level(level):
    """根据关卡选择点击的图片"""
    if level == 1:
        images_to_click = image_names_1
    elif 2 <= level <= 9:
        images_to_click = image_names_2_9
    elif level == 10:
        images_to_click = image_names_10
    else:
        return

    # 遍历每个按钮图片进行匹配和点击
    for image_name in images_to_click:
        image_path = os.path.join(image_folder, image_name)
        print(f"正在查找并点击图片：{image_path}")

        success = False
        for attempt in range(4):
            print(f"尝试 {attempt + 1} 次...")
            if find_and_click(image_path):
                success = True
                break
            time.sleep(1)  # 等待1秒钟后再次尝试

        if not success:
            print(f"未能点击图片：{image_path}，请检查图片是否准确或者提高图片的分辨率和对比度。")
        else:
            print(f"成功点击图片：{image_path}")

    time.sleep(1)  # 点击完后等待 1 秒


def main():
    level = 1  # 从 1 关开始
    while True:
        print(f"开始进行第 {level} 关...")
        play_level(level)
        level += 1  # 进行下一关
        if level > 10:  # 超过 10 关后重新从 1 关开始
            level = 1
        time.sleep(1)  # 等待 1 秒再进行下一关


if __name__ == "__main__":
    main()
