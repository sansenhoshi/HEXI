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
classesList = {
    "Mackay": "麦凯",
    "Angel": "天使",
    "Falck": "法尔克",
    "Paik": "白智秀",
    "Sundance": "日舞",
    "Dozer": "推土机",
    "Rao": "拉奥",
    "Lis": "莉丝",
    "Irish": "爱尔兰佬",
    "Crawford": "克劳福德",
    "Boris": "鲍里斯",
    "Zain": "扎因",
    "Casper": "卡斯帕",
    "Blasco": "布拉斯科",
    "BF3 Recon": "BF3 侦察",
    "BF3 Support": "BF3 支援",
    "BF3 Assault": "BF3 突击",
    "BF3 Engineer": "BF3 工程",
    "BC2 Recon": "BC2 侦察",
    "BC2 Medic": "BC2 医疗",
    "BC2 Assault": "BC2 突击",
    "BC2 Engineer": "BC2 工程",
    "1942 Anti-tank": "1942 反坦克",
    "1942 Assault": "1942 突击",
    "1942 Medic": "1942 医疗",
    "1942 Engineer": "1942 工程",
    "1942 Scout": "1942 侦察",
}


async def builder(data, platform, property):
    # 1. 构建纯黑画板 1920*1080
    data_image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 1000))
    draw = ImageDraw.Draw(data_image)
    # 2. 载入字体
    ch_text_font4 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    ch_text_font3 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 48)
    en_text_font4 = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 32)
    ch_text_font_m = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 42)
    ch_text_font_5 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 24)
    ch_text_font_6 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 22)
    ch_text_font_title = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 80)
    ch_text_font_h2 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 60)
    en_text_font_small = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 20)
    # 测试背景
    bg_name = os.listdir(filepath + "/img/bg/common/")
    index = random.randint(0, len(bg_name) - 1)
    img = Image.open(filepath + f"/img/bg/common/{bg_name[index]}").convert('RGBA').resize((1920, 1080))
    # img_filter = img.filter(ImageFilter.GaussianBlur(radius=3))
    # 4.拼合板块+背景+logo
    data_image.paste(img, (0, 0))

    # 3. 获取各个类别的数据
    data_info = PlayerStats(data)
    weapon_list = data_info.weapons
    weapon_list = data_info.weapons
    vehicle_list = data_info.vehicles
    class_list = data_info.classes
    gadget_list = data_info.gadgets

    # 专家图片板块图层往前
    spc_name = data_info.bestClass
    best_class = Image.open(filepath + f"/img/specialist_img/{spc_name}.png").convert('RGBA')
    best_class = png_resize(best_class, new_width=1920, new_height=1080)
    data_image = image_paste(best_class, data_image, (395, 0))

    # 4. 绘制武器板块
    # 绘制武器版面外框
    # x1 ,y1 ,x2 y2
    # 文字框
    data_image = draw_rect(data_image, (25, 25, 550, 120), 1, fill=(0, 0, 0, 300))
    # 白横条
    data_image = draw_rect(data_image, (25, 125, 550, 145), 1, fill=(255, 255, 255, 300))
    # 外框
    data_image = draw_rect(data_image, (25, 150, 550, 1055), 1, fill=(50, 50, 50, 150))
    # 内框
    data_image = draw_rect(data_image, (28, 153, 547, 1052), 5, fill=(0, 0, 0, 150))

    weapon_text = "枪 械 数 据"
    text_width = draw.textlength(weapon_text, ch_text_font_title)
    print(text_width)
    pos = (((525 - text_width) / 2) + 25, 30)
    draw.text(pos, f'{weapon_text}', fill="white", font=ch_text_font_title)
    weapon_en_text = "W E A P O N S    R E C O R D S"
    text_width = draw.textlength(weapon_en_text, en_text_font_small)
    pos = (((525 - text_width) / 2) + 25, 124)
    draw.text(pos, f'{weapon_en_text}', fill="black", font=en_text_font_small)
    height = 170
    for i in range(0, 5):
        # 粘贴武器图片
        data_image = image_paste(get_top_object_img(weapon_list[i]).resize((160, 80)), data_image, (75, height + 5))
        # 绘制竖线
        draw.line([290, height - 5, 290, height + 130], fill="white", width=3, joint=None)
        # 获取文字的宽度
        weapon_name = weapon_list[i]["weaponName"]
        width = draw.textlength(weapon_name, en_text_font4)  # 获取长度

        # 绘制武器名称
        draw.text((200 - width, height + 90), f'{weapon_name}', fill="white", direction="rtl", font=en_text_font4)

        # 绘制武器数据
        draw.text((300, height), f'击杀数：{weapon_list[i]["kills"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 35), f'爆头率：{weapon_list[i]["headshots"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 70), f'命中率：{weapon_list[i]["accuracy"]}', fill="white", font=ch_text_font_5)
        draw.text((300, height + 105), f'KPM：{weapon_list[i]["killsPerMinute"]}', fill="white", font=ch_text_font_5)
        # 绘制时长边框
        data_image = draw_rect(data_image, (210, height + 90, 290, height + 130), 3, fill=(255, 255, 255, 1000))
        # 绘制时长
        play_time = f'{int(int(weapon_list[i]["timeEquipped"]) / 3600 + 0.55)}H'
        font_width = draw.textlength(play_time, en_text_font4)  # 获取长度
        draw.text((285 - font_width, height + 90), play_time,
                  fill="black",
                  font=en_text_font4)
        height += 180

    # 5.绘制载具板块
    # 文字框
    data_image = draw_rect(data_image, (575, 25, 1100, 120), 1, fill=(0, 0, 0, 300))
    # 白横条
    data_image = draw_rect(data_image, (575, 125, 1100, 145), 1, fill=(255, 255, 255, 300))
    # 外框
    data_image = draw_rect(data_image, (575, 150, 1100, 1055), 1, fill=(50, 50, 50, 150))
    # 内框
    data_image = draw_rect(data_image, (578, 153, 1097, 1052), 5, fill=(0, 0, 0, 150))

    vehicle_text = "载 具 数 据"
    text_width = draw.textlength(vehicle_text, ch_text_font_title)
    print(text_width)
    pos = (((525 - text_width) / 2) + 575, 30)
    draw.text(pos, f'{vehicle_text}', fill="white", font=ch_text_font_title)
    vehicle_en_text = "V E H I C L E S    R E C O R D S"
    text_width = draw.textlength(vehicle_en_text, en_text_font_small)
    pos = (((575 - text_width) / 2) + 575, 124)
    draw.text(pos, f'{vehicle_en_text}', fill="black", font=en_text_font_small)
    height = 170
    for i in range(0, 5):
        # 粘贴载具图片
        data_image = image_paste(get_top_object_img(vehicle_list[i]).resize((240, 60)), data_image, (600, height + 5))
        # 绘制竖线
        draw.line([835, height - 5, 835, height + 130], fill="white", width=3, joint=None)
        # 获取文字的宽度
        vehicle_name = vehicle_list[i]["vehicleName"]
        width = draw.textlength(vehicle_name, en_text_font4)  # 获取长度

        # 绘制载具名称
        draw.text((765 - width, height + 90), f'{vehicle_name}', fill="white", direction="rtl", font=en_text_font4)

        # 绘制载具数据
        draw.text((855, height), f'击杀人数：{vehicle_list[i]["kills"]}', fill="white", font=ch_text_font4)
        draw.text((855, height + 45), f'摧毁载具：{vehicle_list[i]["vehiclesDestroyedWith"]}', fill="white",
                  font=ch_text_font4)
        draw.text((908, height + 90), f'KPM：{vehicle_list[i]["killsPerMinute"]}', fill="white", font=ch_text_font4)
        # 绘制时长边框
        data_image = draw_rect(data_image, (775, height + 90, 900, height + 130), 3, fill=(255, 255, 255, 1000))
        data_image = draw_rect(data_image, (777, height + 92, 898, height + 128), 3, fill=(0, 0, 0, 1000))
        data_image = draw_rect(data_image, (779, height + 94, 896, height + 126), 3, fill=(255, 255, 255, 1000))
        # 绘制时长
        play_time = f'{int(int(vehicle_list[i]["timeIn"]) / 3600 + 0.55)}H'
        font_width = draw.textlength(play_time, en_text_font4)  # 获取长度
        draw.text((895 - font_width, height + 90), play_time,
                  fill="black",
                  font=en_text_font4)
        height += 180
    # 6.绘制个人信息
    ea_id = data_info.userName
    # 时长
    time_played = data_info.timePlayed
    if ',' in time_played:
        times = time_played.split(',')
        if "days" in times[0]:
            times_1 = int(times[0].replace("days", "").strip()) * 24
        else:
            times_1 = int(times[0].replace("day", "").strip()) * 24
        times_2 = times[1].split(':')
        time_part2 = int(times_2[0]) + Decimal(int(times_2[1]) / 60).quantize(Decimal("0.00"))
        time_played = str(times_1 + time_part2)
    else:
        time_part2 = Decimal(int(time_played.split(':')[1]) / 60).quantize(Decimal("0.00"))
        time_played = int(time_played.split(':')[0]) + time_part2
    # 场次
    matches = data_info.matchesPlayed
    # mvp
    mvp = data_info.mvp

    # 绘制 个人信息框
    data_image = draw_rect(data_image, (1120, 690, 1645, 830), 1, fill=(50, 50, 50, 150))
    data_image = draw_rect(data_image, (1123, 693, 1642, 827), 5, fill=(0, 0, 0, 150))
    user_text = f"EA ID:  {ea_id}"
    pos = (1135, 700)
    draw.text(pos, user_text, fill="white", font=en_text_font4)
    data_text1 = f"时长：{time_played}H"
    data_text2 = f"场次：{matches}"
    data_text3 = f"最佳：{mvp}"
    draw.text((1135, 775), data_text1, fill="white", font=ch_text_font_5)
    draw.text((1315, 775), data_text2, fill="white", font=ch_text_font_5)
    draw.text((1456, 775), data_text3, fill="white", font=ch_text_font_5)
    # 绘制专家信息
    # 边框
    data_image = draw_rect(data_image, (1120, 831, 1645, 1055), 1, fill=(50, 50, 50, 150))
    data_image = draw_rect(data_image, (1123, 834, 1642, 1052), 5, fill=(0, 0, 0, 150))
    # 文字部分
    best_text = "最 佳 专 家"
    best_text_width = draw.textlength(best_text, ch_text_font_h2)
    # 分割线
    draw.line([1455, 845, 1430, 1030], fill="white", width=3, joint=None)
    draw.text((1440 - best_text_width, 860), best_text, fill="white", font=ch_text_font_h2)
    best_class_data = sorted(data["classes"], key=lambda k: k['kills'], reverse=True)[0]
    best_class_name = classesList[spc_name]
    best_kill = best_class_data['kills']
    best_kd = best_class_data['killDeath']
    best_kpm = best_class_data['kpm']
    best_time = best_class_data['secondsPlayed']
    best_time = round(best_time / 3600, 2)
    text_width_class_name = draw.textlength(best_class_name, ch_text_font_m)
    draw.text((1415 - text_width_class_name, 963), best_class_name,
              fill="white",
              font=ch_text_font_m)

    special_icon = await get_special_icon(best_class_data)
    special_icon = png_resize(special_icon, new_width=75, new_height=75)
    print(text_width_class_name)
    # paste方法不能处理浮点数
    pos = (round(1390 - text_width_class_name - 60), 950)
    data_image = image_paste(special_icon, data_image, pos)
    # 击杀/kd/kpm/时长
    draw.text((1465, 860), f'K/D：{best_kd}', fill="white", font=ch_text_font_5)
    draw.text((1460, 900), f'KPM：{best_kpm}', fill="white", font=ch_text_font_5)
    draw.text((1455, 940), f'击杀：{best_kill}', fill="white", font=ch_text_font_5)
    draw.text((1450, 980), f'时长：{best_time}H', fill="white", font=ch_text_font_5)

    # 边框
    data_image = draw_rect(data_image, (1120, 25, 1645, 120), 1, fill=(0, 0, 0, 300))
    # 白横条
    data_image = draw_rect(data_image, (1120, 125, 1645, 145), 1, fill=(255, 255, 255, 300))

    # 分割线
    draw.line([1670, 150, 1670, 1055], fill="white", width=5, joint=None)
    # 7.生涯数据
    # part1
    kd = data_info.killDeath
    real_kd = data_info.infantryKillDeath
    kills = data_info.kills
    vehicle_kills = data_info.dividedKills['vehicle']
    death = data_info.deaths
    # part2
    kpm = data_info.killsPerMinute
    kill_human_per = float(data_info.humanPrecentage.strip('%')) / 100
    real_kpm = round(kill_human_per * kpm, 2)
    headshot = data_info.headshots
    acc = data_info.accuracy
    win = data_info.winPercent
    # part3
    AI_kills = data_info.dividedKills['ai']
    kills_per_match = data_info.killsPerMatch
    revives = data_info.revives
    spot = data_info.enemiesSpotted
    vehicles_destroyed = data_info.vehiclesDestroyed

    # 开始打印生涯数据
    # 绘制边框
    data_image = draw_rect(data_image, (1673, 150, 1895, 1055), 1, fill=(50, 50, 50, 150))
    data_image = draw_rect(data_image, (1676, 153, 1892, 1052), 5, fill=(0, 0, 0, 150))
    # part1
    draw.text((1680, 165), f'K/D：{kd}', fill="white", font=ch_text_font_6)
    draw.text((1680, 222), f'真实K/D：{real_kd}', fill="white", font=ch_text_font_6)
    draw.text((1680, 279), f'击杀总数：{kd}', fill="white", font=ch_text_font_6)
    draw.text((1680, 336), f'载具击杀：{kd}', fill="white", font=ch_text_font_6)
    draw.text((1680, 393), f'死亡次数：{kd}', fill="white", font=ch_text_font_6)
    # part1
    # 分割线
    data_image = await draw_point_line(data_image, (1685, 450), (1870, 450), line_spacing=5, line_length=30, line_width=2,
                                       line_color='white')

    draw.text((1680, 479), f'KPM：{kpm}', fill="white", font=ch_text_font_6)
    draw.text((1680, 536), f'真实KPM：{real_kpm}', fill="white", font=ch_text_font_6)
    draw.text((1680, 593), f'爆头率：{headshot}', fill="white", font=ch_text_font_6)
    draw.text((1680, 650), f'命中率：{acc}', fill="white", font=ch_text_font_6)
    draw.text((1680, 707), f'胜率：{win}', fill="white", font=ch_text_font_6)
    # part1
    # 分割线
    data_image = await draw_point_line(data_image, (1685, 764), (1870, 764), line_spacing=5, line_length=30,line_width=2,
                                       line_color='white')
    draw.text((1680, 793), f'AI击杀：{AI_kills}', fill="white", font=ch_text_font_6)
    draw.text((1680, 850), f'场均击杀：{kills_per_match}', fill="white", font=ch_text_font_6)
    draw.text((1680, 907), f'急救：{revives}', fill="white", font=ch_text_font_6)
    draw.text((1680, 964), f'标记：{spot}', fill="white", font=ch_text_font_6)
    draw.text((1680, 1021), f'摧毁载具：{vehicles_destroyed}', fill="white", font=ch_text_font_6)

    # 粘贴game logo
    logo = Image.open(filepath + "/img/bf2042_logo/bf2042logo.png").convert('RGBA')
    logo = png_resize(logo, new_width=120, new_height=120)
    data_image = image_paste(logo, data_image, (1775, 25))

    data_image.show()
    b_io = BytesIO()
    data_image.save(b_io, format="PNG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str
