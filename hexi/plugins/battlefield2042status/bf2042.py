import base64
import os
import random
from decimal import Decimal
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from .data_tools import hacker_check, get_bf_ban_check
from .picture_tools import draw_rect, circle_corner, png_resize, \
    get_top_object_img, \
    image_paste, paste_ic_logo, get_avatar, get_special_icon, draw_point_line

classesList = {
    "Mackay": "   麦凯",
    "Angel": "   天使",
    "Falck": "  法尔克",
    "Paik": "  白智秀",
    "Sundance": "   日舞",
    "Dozer": "  推土机",
    "Rao": "   拉奥",
    "Lis": "   莉丝",
    "Irish": "爱尔兰佬",
    "Crawford": "克劳福德",
    "Boris": "  鲍里斯",
    "Zain": "   扎因",
    "Casper": "  卡斯帕",
    "Blasco": "布拉斯科",
}
classes_type_list = {
    "Assault": "突击兵",
    "Support": "支援兵",
    "Recon": "侦察兵",
    "Engineer": "工程兵"
}

ban_reason = {
    0: "未处理",
    1: "石锤",
    2: "待自证",
    3: "MOSS自证",
    4: "无效举报",
    5: "讨论中",
    6: "需要更多管理投票",
    7: "未知原因封禁",
    8: "刷枪"
}

filepath = os.path.dirname(__file__).replace("\\", "/")
bf_ban_url = "https://api.gametools.network/bfban/checkban"


async def bf_2042_gen_pic(data, platform):
    # 1.创建黑色板块 1920*1080
    new_img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 1000))
    # 2.获取头像图片 150*150
    platform_id = 1
    nucleus_id = data['userId']
    persona_id = data['id']
    # 调用接口获取正确的头像
    avatar = await get_avatar(platform_id, persona_id, nucleus_id)
    avatar = png_resize(avatar, new_width=145, new_height=145)
    avatar = circle_corner(avatar, 10)
    # 3.获取背景 并 模糊
    # 判断是否为support
    bg_name = os.listdir(filepath + "/img/bg/common/")
    index = random.randint(0, len(bg_name) - 1)
    img = Image.open(filepath + f"/img/bg/common/{bg_name[index]}").convert('RGBA').resize((1920, 1080))
    # img_filter = img.filter(ImageFilter.GaussianBlur(radius=3))
    # 4.拼合板块+背景+logo
    new_img.paste(img, (0, 0))
    logo = Image.open(filepath + "/img/bf2042_logo/bf2042logo.png").convert('RGBA')
    logo = png_resize(logo, new_width=145, new_height=145)
    logo = circle_corner(logo, 10)
    new_img = image_paste(logo, new_img, (1750, 30))
    # 5.绘制头像框 (x1,y1,x2,y2)
    # x2 = x1+width+img_width+width
    # y2 = y1+width+img_height+width
    draw = ImageDraw.Draw(new_img)
    new_img = draw_rect(new_img, (25, 25, 768, 180), 10, fill=(0, 0, 0, 150))
    # 6添加头像
    new_img = image_paste(avatar, new_img, (30, 30))
    # 7.添加用户信息文字

    # # 等级计算
    # xp = data["XP"][0]["total"]
    # unit = 93944
    # level = int((xp \\ unit) + 0.55)
    # color = 'white'
    # if int((xp \\ 93944) + 0.55) > 0:
    #     level = ('S' + str(level - 99))
    #     color = '#FF3333'

    # 载入字体
    en_text_font = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 36)
    ch_text_font = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 36)
    # 获取用化名
    player_name = data["userName"]
    plat = Image.open(filepath + "/img/platform/origin.png").convert("RGBA").resize((40, 40))
    if platform == "pc":
        plat = Image.open(filepath + "/img/platform/origin.png").convert("RGBA").resize((40, 40))
    elif platform == "psn":
        plat = Image.open(filepath + "/img/platform/playstation.png").convert("RGBA").resize((40, 40))
    elif platform == "xbl":
        plat = Image.open(filepath + "/img/platform/xbox.png").convert("RGBA").resize((40, 40))
    draw.text((208, 33), '玩家：', fill='white', font=ch_text_font)
    draw.text((308, 30), f'{player_name}', fill='white', font=en_text_font)
    # 游玩平台
    new_img = image_paste(plat, new_img, (208, 120))
    draw.text((260, 120), '游玩时长：', fill='white', font=ch_text_font)
    time_played = data["timePlayed"]
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
    draw.text((430, 118), f'{time_played} H', fill='white', font=en_text_font)
    # 8.绘制最佳专家外框
    # 获取兵种图标
    best_class = sorted(data["classes"], key=lambda k: k['kills'], reverse=True)[0]
    # 专家名称
    best_specialist = best_class["characterName"]
    # 专家击杀数
    best_specialist_kills = best_class["kills"]
    # 专家kpm
    best_specialist_kpm = best_class["kpm"]
    # 专家kd
    best_specialist_kill_death = best_class["killDeath"]
    # 游玩时长
    seconds = best_class["secondsPlayed"]
    best_specialist_played = round(seconds / 3600, 2)
    # 专家图标
    class_icon = await get_special_icon(best_class)
    # 图像缩放
    class_icon = class_icon.resize((90, 90))
    # 绘制最佳专家
    ch_text_font_bc = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 38)
    ch_text_font_s = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 30)
    new_img = draw_rect(new_img, (768 + 25, 25, 1318, 180), 10, fill=(0, 0, 0, 150))
    draw.text((815, 55), '最 佳', fill='lightgreen', font=ch_text_font_bc)
    draw.text((815, 105), '专 家', fill='lightgreen', font=ch_text_font_bc)
    new_img = image_paste(class_icon, new_img, (930, 35))
    spec_name = classesList[best_specialist]
    draw.text((918, 130), f'{spec_name}', fill='skyblue', font=ch_text_font_s)
    draw.text((1050, 40), f'KD：{best_specialist_kill_death}', fill='white', font=ch_text_font_s)
    draw.text((1050, 70), f'KPM：{best_specialist_kpm}', fill='white', font=ch_text_font_s)
    draw.text((1050, 103), f'击杀数：{best_specialist_kills}', fill='white', font=ch_text_font_s)
    draw.text((1050, 138), f'时长：{best_specialist_played}', fill='white', font=ch_text_font_s)

    # 9.MVP/最佳小队
    # 绘制最佳小队/MVP
    new_img = draw_rect(new_img, (1318 + 25, 25, 1920 - 195, 180), 10, fill=(0, 0, 0, 150))
    # 游玩场数
    matches = data["matchesPlayed"]
    # mvp
    mvp = "MVP：" + str(data["mvp"])
    # 最佳小队
    best_squad = "最佳小队：" + str(data["bestSquad"])
    best_show = random.choice((mvp, best_squad))
    ch_text_font2 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 36)
    draw.text((1368, 50), f'游玩场数: {matches}', fill='white', font=ch_text_font2)
    draw.text((1368, 111), f'{best_show}', fill='white', font=ch_text_font2)
    # 10.绘制生涯框
    new_img = draw_rect(new_img, (25, 205, 1920 - 25, 455), 10, fill=(0, 0, 0, 150))
    ch_text_font3 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    en_text_font3 = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 36)
    # 分割的击杀数据
    divided_kills = data["dividedKills"]
    # 处理击杀玩家的百分比
    kill_human_per = data["humanPrecentage"]
    kill_human_per = float(kill_human_per.strip('%')) / 100
    # kd
    kd = data["killDeath"]
    # 四舍五入计算真实KD
    real_kd = round(kill_human_per * kd, 2)
    # 击杀数
    kills = data["kills"]
    # kpm
    kpm = data["killsPerMinute"]
    # 真实kpm
    real_kpm = round(kill_human_per * kpm, 2)
    # 步战kd
    infantryKillDeath = data["infantryKillDeath"]
    # 场均击杀
    k_per_match = data["killsPerMatch"]
    # 爆头率
    hs = data["headshots"]
    # 命中率
    acc = data["accuracy"]
    # 胜场
    win = data["winPercent"]
    # 人类百分比
    human_per = data["humanPrecentage"]
    # AI击杀数量
    AI_kill = divided_kills["ai"]
    # 阵亡
    deaths = data["deaths"]
    # 急救
    revives = data["revives"]
    # 标记敌人数
    eme = data["enemiesSpotted"]
    # 摧毁载具数量
    vehiclesDestroyed = data["vehiclesDestroyed"]
    # 载具击杀数
    vehicle_kill = divided_kills["vehicle"]
    # 数据1
    draw.text((150, 220), f'K/D： {kd}', fill='white', font=ch_text_font3)
    draw.text((150, 265), f'步战 K/D： {infantryKillDeath}', fill='white', font=ch_text_font3)
    draw.text((150, 310), f'击杀： {kills}', fill='white', font=ch_text_font3)
    draw.text((150, 355), f'载具击杀： {vehicle_kill}', fill='white', font=ch_text_font3)
    draw.text((150, 400), f'死亡数： {deaths}', fill='white', font=ch_text_font3)

    # 数据2
    draw.text((550, 220), f'KPM： {kpm}', fill='white', font=ch_text_font3)
    draw.text((550, 265), f'真实KPM： {real_kpm}', fill='white', font=ch_text_font3)
    draw.text((550, 310), f'爆头率： {hs}', fill='white', font=ch_text_font3)
    draw.text((550, 355), f'命中率： {acc}', fill='white', font=ch_text_font3)
    draw.text((550, 400), f'胜率： {win}', fill='white', font=ch_text_font3)

    # 数据3
    draw.text((950, 220), f'AI击杀： {AI_kill}', fill='white', font=ch_text_font3)
    draw.text((950, 265), f'场均击杀： {k_per_match}', fill='white', font=ch_text_font3)
    draw.text((950, 310), f'急救数： {revives}', fill='white', font=ch_text_font3)
    draw.text((950, 355), f'标记敌人数： {eme}', fill='white', font=ch_text_font3)
    draw.text((950, 400), f'摧毁载具数： {vehiclesDestroyed}', fill='white', font=ch_text_font3)

    # 数据4 BF TRACKER个人主页
    # en_text_font_ext = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 24)
    # qr_img = qr_code_gen(player_name, platform)
    # qr_img = qr_img.resize((145, 145))
    # draw.text((1300, 228), "BATTLEFIELD\n    TRACKER", fill="lightgreen", font=en_text_font_ext)
    # new_img.paste(qr_img, (1300, 290))

    weapon_list = sorted(data["weapons"], key=lambda k: k['kills'], reverse=True)

    # 数据5 简易检测器
    hacker_check_res = hacker_check(weapon_list)
    final = "未知"
    color = "white"
    check_res = False

    if 3 in hacker_check_res:
        final = "鉴定为红橙黄绿蓝紫\n没有青吗？"
        color = "#FF9999"
        check_res = True
    elif 2 in hacker_check_res:
        final = "挂？\n样本太少了"
        color = "yellow"
        check_res = True
    elif 1 in hacker_check_res:
        final = "数据不对？\n样本太少了"
        color = "yellow"
        check_res = True
    elif 0 in hacker_check_res:
        final = "可疑？\n建议详查"
        color = "yellow"
        check_res = True
    if not check_res:
        # kpm大于1 总kd大于2 真实kd大于1.5
        if kpm > 1.00 and kd > 2 and real_kd > 1.5:
            final = "Pro哥\n你带我走吧T_T"
            color = "gold"
        else:
            final = "薯薯\n别拷打我了哥>_<"
            color = "skyblue"

    ch_text_font_ext = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    ch_text_font_ext2 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 28)
    draw.text((1300, 220), f'机器棱鉴定结果（仅供参考）：', fill="white", font=ch_text_font_ext)
    draw.text((1300, 240), f'\n{final}', fill=f"{color}", font=ch_text_font_ext2)

    # 添加BF ban 检测结果
    bf_ban_res = await get_bf_ban_check(data["userName"], data["userId"], data["id"])
    draw.text((1300, 360), f'联BAN查询：', fill="white", font=ch_text_font_ext)
    draw.text((1300, 380), f'\n{bf_ban_res}', fill="yellow", font=ch_text_font_ext2)

    # 11.绘制第三部分 TOP4武器/载具 947.5-12.5
    new_img = draw_rect(new_img, (25, 480, 1920 - 25, 1080 - 25), 10, fill=(0, 0, 0, 150))
    ch_text_font4 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    en_text_font4 = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 32)
    # 武器部分
    top_weapon_list = sorted(data["weapons"], key=lambda k: k['kills'], reverse=True)
    height = 500
    line_height = 845
    for i in range(0, 5):
        # 1
        # 修饰线条
        if i < 3:
            draw.line([45, height + 5, 45, height + 85], fill="#CCFF00", width=5, joint=None)
        else:
            draw.line([45, line_height, 45, line_height+80], fill="#66CCFF", width=5, joint=None)
            line_height += 110
        new_img = image_paste(get_top_object_img(top_weapon_list[i]).resize((160, 80)), new_img, (50, height + 5))
        draw.text((230, height), f'{top_weapon_list[i]["weaponName"]}', fill="white", font=en_text_font4)
        draw.text((230, height + 45), f'击杀：{top_weapon_list[i]["kills"]}', fill="white", font=ch_text_font4)

        draw.text((450, height), f'爆头率：{top_weapon_list[i]["headshots"]}', fill="white", font=ch_text_font4)
        draw.text((450, height + 45), f'命中率：{top_weapon_list[i]["accuracy"]}', fill="white", font=ch_text_font4)

        draw.text((730, height), f'KPM：{top_weapon_list[i]["killsPerMinute"]}', fill="white", font=ch_text_font4)
        draw.text((730, height + 45), f'时长：{int(int(top_weapon_list[i]["timeEquipped"]) / 3600 + 0.55)} H',
                  fill="white",
                  font=ch_text_font4)
        height += 110

    # 分割线
    draw.line([950, 505, 950, 1030], fill="white", width=5, joint=None)

    # 载具部分
    top_vehicles_list = sorted(data["vehicles"], key=lambda k: k['kills'], reverse=True)
    height = 500
    line_height = 845
    for n in range(0, 5):
        # 修饰线条
        if n < 3:
            draw.line([975, height + 5, 975, height + 85], fill="#CCFF00", width=5, joint=None)
        else:
            draw.line([975, line_height, 975, line_height + 80], fill="#66CCFF", width=5, joint=None)
            line_height += 110
        new_img = image_paste(get_top_object_img(top_vehicles_list[n]).resize((320, 80)), new_img, (980, height + 5))
        draw.text((1325, height), f'{top_vehicles_list[n]["vehicleName"]}', fill="white", font=en_text_font4)
        draw.text((1325, height+45), f'击杀：{top_vehicles_list[n]["kills"]}', fill="white", font=ch_text_font4)
        draw.text((1630, height), f'KPM：{top_vehicles_list[n]["killsPerMinute"]}', fill="white", font=ch_text_font4)
        draw.text((1630, height+45), f'摧毁数：{top_vehicles_list[n]["vehiclesDestroyedWith"]}', fill="white", font=ch_text_font4)
        height += 110

    # 添加开发团队logo
    new_img = paste_ic_logo(new_img)
    # 图片处理完成 发送
    # sv.logger.info(f"玩家：{player_name}->图片处理完成")
    # 显示图片
    # new_img.show()
    b_io = BytesIO()
    new_img.save(b_io, format="PNG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str


async def bf2042_weapon(data, platform):
    # 1.创建黑色板块 1920*1080
    new_img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 1000))
    # 2.获取头像图片 150*150
    platform_id = 1
    nucleus_id = data['userId']
    persona_id = data['id']
    # 调用接口获取正确的头像
    avatar = await get_avatar(platform_id, persona_id, nucleus_id)
    avatar = png_resize(avatar, new_width=145, new_height=145)
    avatar = circle_corner(avatar, 10)
    # 3.获取背景 并 模糊
    # 判断是否为support
    bg_name = os.listdir(filepath + "/img/bg/common/")
    index = random.randint(0, len(bg_name) - 1)
    img = Image.open(filepath + f"/img/bg/common/{bg_name[index]}").convert('RGBA').resize((1920, 1080))
    # img_filter = img.filter(ImageFilter.GaussianBlur(radius=3))
    # 4.拼合板块+背景+logo
    new_img.paste(img, (0, 0))
    logo = Image.open(filepath + "/img/bf2042_logo/bf2042logo.png").convert('RGBA')
    logo = png_resize(logo, new_width=145, new_height=145)
    logo = circle_corner(logo, 10)
    new_img = image_paste(logo, new_img, (1750, 30))
    # 5.绘制头像框 (x1,y1,x2,y2)
    # x2 = x1+width+img_width+width
    # y2 = y1+width+img_height+width
    draw = ImageDraw.Draw(new_img)
    new_img = draw_rect(new_img, (25, 25, 768, 180), 10, fill=(0, 0, 0, 150))
    # 6添加头像
    new_img = image_paste(avatar, new_img, (30, 30))
    # 7.添加用户信息文字

    # # 等级计算
    # xp = data["XP"][0]["total"]
    # unit = 93944
    # level = int((xp \\ unit) + 0.55)
    # color = 'white'
    # if int((xp \\ 93944) + 0.55) > 0:
    #     level = ('S' + str(level - 99))
    #     color = '#FF3333'

    # 载入字体
    en_text_font = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 36)
    ch_text_font = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 36)
    # 获取用化名
    player_name = data["userName"]
    plat = Image.open(filepath + "/img/platform/origin.png").convert("RGBA").resize((40, 40))
    if platform == "pc":
        plat = Image.open(filepath + "/img/platform/origin.png").convert("RGBA").resize((40, 40))
    elif platform == "psn":
        plat = Image.open(filepath + "/img/platform/playstation.png").convert("RGBA").resize((40, 40))
    elif platform == "xbl":
        plat = Image.open(filepath + "/img/platform/xbox.png").convert("RGBA").resize((40, 40))
    draw.text((208, 33), '玩家：', fill='white', font=ch_text_font)
    draw.text((308, 30), f'{player_name}', fill='white', font=en_text_font)
    # 游玩平台
    # draw.rectangle([208, 120, 248, 160], fill="black")
    # r, g, b, alpha = plat.split()
    # new_img.paste(plat, (208, 120), mask=alpha)
    new_img = image_paste(plat, new_img, (208, 120))
    draw.text((260, 120), '游玩时长：', fill='white', font=ch_text_font)
    time_played = data["timePlayed"]
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
    draw.text((430, 118), f'{time_played} H', fill='white', font=en_text_font)
    # 8.绘制最佳专家外框
    # 获取兵种图标
    best_class = sorted(data["classes"], key=lambda k: k['kills'], reverse=True)[0]
    # 专家名称
    best_specialist = best_class["characterName"]
    # 专家击杀数
    best_specialist_kills = best_class["kills"]
    # 专家kpm
    best_specialist_kpm = best_class["kpm"]
    # 专家kd
    best_specialist_kill_death = best_class["killDeath"]
    # 游玩时长
    seconds = best_class["secondsPlayed"]
    best_specialist_played = round(seconds / 3600, 2)
    # 专家图标
    class_icon = await get_special_icon(best_class)
    # 图像缩放
    class_icon = class_icon.resize((90, 90))
    # class_icon = png_resize(class_icon, new_width=90, new_height=90)
    # (300, 360)
    # 绘制最佳专家
    ch_text_font_bc = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 38)
    ch_text_font_s = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 30)
    new_img = draw_rect(new_img, (768 + 25, 25, 1318, 180), 10, fill=(0, 0, 0, 150))
    draw.text((815, 55), '最 佳', fill='lightgreen', font=ch_text_font_bc)
    draw.text((815, 105), '专 家', fill='lightgreen', font=ch_text_font_bc)
    new_img = image_paste(class_icon, new_img, (930, 35))
    spec_name = classesList[best_specialist]
    draw.text((918, 130), f'{spec_name}', fill='skyblue', font=ch_text_font_s)
    draw.text((1050, 40), f'KD：{best_specialist_kill_death}', fill='white', font=ch_text_font_s)
    draw.text((1050, 70), f'KPM：{best_specialist_kpm}', fill='white', font=ch_text_font_s)
    draw.text((1050, 100), f'击杀数：{best_specialist_kills}', fill='white', font=ch_text_font_s)
    draw.text((1050, 130), f'时长：{best_specialist_played}', fill='white', font=ch_text_font_s)

    # 9.MVP/最佳小队
    # 绘制最佳小队/MVP
    new_img = draw_rect(new_img, (1318 + 25, 25, 1920 - 195, 180), 10, fill=(0, 0, 0, 150))
    # 游玩场数
    matches = data["matchesPlayed"]
    # mvp
    mvp = "MVP：" + str(data["mvp"])
    # 最佳小队
    best_squad = "最佳小队：" + str(data["bestSquad"])
    best_show = random.choice((mvp, best_squad))
    ch_text_font2 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 36)
    draw.text((1368, 50), f'游玩场数: {matches}', fill='white', font=ch_text_font2)
    draw.text((1368, 111), f'{best_show}', fill='white', font=ch_text_font2)

    # 10.绘制武器框
    new_img = draw_rect(new_img, (25, 205, 1920 - 25, 1080 - 25), 10, fill=(0, 0, 0, 150))

    # 武器击杀数排序
    top_weapon_list = sorted(data["weapons"], key=lambda k: k['kills'], reverse=True)

    # 载入字体
    ch_text_font4 = ImageFont.truetype(filepath + '/font/NotoSansSCMedium-4.ttf', 32)
    en_text_font4 = ImageFont.truetype(filepath + '/font/BF_Modernista-Bold.ttf', 32)

    # 遍历 左
    height = 220
    index = 0
    for i in range(0, 8):
        new_img = image_paste(get_top_object_img(top_weapon_list[i]).resize((160, 80)), new_img, (50, height + 5))
        draw.text((230, height), f'{top_weapon_list[i]["weaponName"]}', fill="white", font=en_text_font4)
        draw.text((230, height + 45), f'击杀：{top_weapon_list[i]["kills"]}', fill="white", font=ch_text_font4)

        draw.text((450, height), f'爆头率：{top_weapon_list[i]["headshots"]}', fill="white", font=ch_text_font4)
        draw.text((450, height + 45), f'命中率：{top_weapon_list[i]["accuracy"]}', fill="white", font=ch_text_font4)

        draw.text((730, height), f'KPM：{top_weapon_list[0]["killsPerMinute"]}', fill="white", font=ch_text_font4)
        draw.text((730, height + 45), f'时长：{int(int(top_weapon_list[0]["timeEquipped"]) / 3600 + 0.55)} H',
                  fill="white",
                  font=ch_text_font4)
        if i != 7:
            new_img = await draw_point_line(new_img, start_point=(50, height + 90), end_point=(1820, height + 90),
                                            line_color='green')
        height += 105
        index = i

    # 分割线
    draw.line([950, 225, 950, 1030], fill="white", width=5, joint=None)
    # 遍历 右
    height = 220
    for i in range(index, index + 8):
        new_img = image_paste(get_top_object_img(top_weapon_list[i]).resize((160, 80)), new_img, (975, height + 5))
        draw.text((1160, height), f'{top_weapon_list[i]["weaponName"]}', fill="white", font=en_text_font4)
        draw.text((1160, height + 45), f'击杀：{top_weapon_list[i]["kills"]}', fill="white", font=ch_text_font4)

        draw.text((1380, height), f'爆头率：{top_weapon_list[i]["headshots"]}', fill="white", font=ch_text_font4)
        draw.text((1380, height + 45), f'命中率：{top_weapon_list[i]["accuracy"]}', fill="white", font=ch_text_font4)

        draw.text((1660, height), f'KPM：{top_weapon_list[0]["killsPerMinute"]}', fill="white", font=ch_text_font4)
        draw.text((1660, height + 45), f'时长：{int(int(top_weapon_list[0]["timeEquipped"]) / 3600 + 0.55)} H',
                  fill="white",
                  font=ch_text_font4)
        height += 105
    # 添加开发团队logo
    new_img = paste_ic_logo(new_img)
    b_io = BytesIO()
    new_img.save(b_io, format="PNG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str
