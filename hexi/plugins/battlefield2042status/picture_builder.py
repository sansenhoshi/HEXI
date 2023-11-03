import base64
import os
import random
from decimal import Decimal
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .picture_tools import draw_rect, circle_corner, png_resize, \
    get_top_object_img, \
    image_paste, paste_ic_logo, get_avatar, get_special_icon, draw_point_line\

from .PlayDataClass import PlayerStats

filepath = os.path.dirname(__file__).replace("\\", "/")


async def builder(data, platform, property):
    # 1. 构建纯黑画板 1920*1080
    data_image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 1000))
    draw = ImageDraw.Draw(data_image)
    # 2. 载入字体
    ch_text_font4 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    en_text_font4 = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 32)
    ch_text_font_5 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 24)

    # 3. 获取各个类别的数据
    we = PlayerStats(data)
    weapon_list = we.weapons
    weapon_list = sorted(data[property], key=lambda k: k['kills'], reverse=True)
    vehicle_list = sorted(data[property], key=lambda k: k['kills'], reverse=True)
    class_list = sorted(data[property], key=lambda k: k['kills'], reverse=True)

    # 4. 绘制武器板块
    height = 170
    line_height = 515
    for i in range(0, 5):
        # 粘贴武器图片
        data_image = image_paste(get_top_object_img(weapon_list[i]).resize((160, 80)), data_image, (50, height + 5))
        # 绘制竖线
        draw.line([290, height - 5, 290, height+130], fill="white", width=3, joint=None)
        # 获取文字的宽度
        weapon_name = weapon_list[i]["weaponName"]
        width = draw.textlength(weapon_name, en_text_font4)  # 获取长度

        # 绘制武器名称
        draw.text((200-width, height+90), f'{weapon_name}', fill="white", direction="rtl", font=en_text_font4)

        # 绘制武器数据
        draw.text((300, height), f'击杀数：{weapon_list[i]["kills"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 35), f'爆头率：{weapon_list[i]["headshots"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 70), f'命中率：{weapon_list[i]["accuracy"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 105), f'KPM：{weapon_list[i]["killsPerMinute"]}', fill="white", font=ch_text_font_5)
        # 绘制时长边框
        data_image = draw_rect(data_image, (210, height+90, 290, height+130), 5, fill=(255, 255, 255, 1000))
        # 绘制时长
        play_time = f'{int(int(weapon_list[i]["timeEquipped"]) / 3600 + 0.55)}H'
        font_width = draw.textlength(play_time, en_text_font4)  # 获取长度
        draw.text((285-font_width, height+90), play_time,
                  fill="black",
                  font=en_text_font4)
        height += 180

    data_image.show()
    b_io = BytesIO()
    data_image.save(b_io, format="PNG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str
