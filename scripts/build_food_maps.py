from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
import random

OUT = Path(__file__).resolve().parents[1] / "assets"
FONT = "C:/Windows/Fonts/msjh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def text(draw, xy, value, fill, size=36, anchor=None, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def icon_bowl(draw, cx, cy, scale=1, fill=(226, 87, 39)):
    w, h = int(86 * scale), int(48 * scale)
    draw.ellipse((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), fill=(255, 245, 221), outline=(17, 45, 61), width=max(2, int(3 * scale)))
    draw.pieslice((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2 + 36), 0, 180, fill=fill)
    for i in range(4):
        x = cx - w // 3 + i * w // 5
        draw.line((x, cy - h // 2 - 18 * scale, x + 18 * scale, cy - h // 2 + 10 * scale), fill=(17, 45, 61), width=max(2, int(3 * scale)))


def pin(draw, x, y, label, accent=(226, 87, 39)):
    draw.ellipse((x - 23, y - 23, x + 23, y + 23), fill=accent, outline="white", width=5)
    draw.polygon([(x, y + 28), (x - 13, y + 10), (x + 13, y + 10)], fill=accent)
    tw = min(42 + len(label) * 31, 360)
    rounded(draw, (x + 32, y - 34, x + tw, y + 35), 18, (255, 255, 255), (206, 216, 218), 2)
    text(draw, (x + 54, y - 13), label, (17, 45, 61), 28, bold=True)


def make_city(filename, city, subtitle, palette, water, pins, dishes, routes, landmark):
    random.seed(filename)
    width, height = 1600, 1000
    img = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(img)

    for _ in range(12):
        cx, cy = random.randint(-100, width + 100), random.randint(80, height - 80)
        radius = random.randint(130, 320)
        color = random.choice([palette["mint"], palette["cream"], palette["sky"]])
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)

    if water == "lake":
        draw.ellipse((180, 250, 760, 770), fill=palette["water"], outline=(125, 184, 189), width=7)
        draw.ellipse((330, 360, 610, 630), fill=(245, 251, 247), outline=(125, 184, 189), width=4)
        draw.arc((190, 260, 750, 760), 210, 330, fill=(255, 255, 255), width=8)
    elif water == "rivers":
        draw.line([(0, 540), (320, 490), (620, 540), (930, 480), (1600, 550)], fill=palette["water"], width=145)
        draw.line([(720, 0), (760, 230), (730, 520), (820, 1000)], fill=palette["water2"], width=110)
        for x in [470, 1050, 1260]:
            draw.arc((x - 150, 455, x + 150, 610), 200, 340, fill=(255, 255, 255), width=7)
    else:
        draw.line([(80, 710), (420, 620), (700, 670), (1040, 570), (1500, 640)], fill=palette["water"], width=88)
        draw.ellipse((230, 170, 510, 410), fill=palette["park"], outline=(132, 180, 145), width=4)
        draw.ellipse((970, 210, 1210, 420), fill=palette["park"], outline=(132, 180, 145), width=4)

    for route in routes:
        draw.line(route, fill=(255, 255, 255), width=20)
        draw.line(route, fill=(222, 188, 102), width=5)

    for i, x in enumerate(range(980, 1480, 70)):
        top = 210 + ((i * 53) % 150)
        draw.rounded_rectangle((x, top, x + 46, 570), radius=8, fill=(137, 166, 180), outline=(17, 45, 61), width=2)
        for yy in range(top + 25, 550, 45):
            draw.line((x + 9, yy, x + 36, yy), fill=(234, 242, 239), width=2)

    rounded(draw, (78, 66, 1522, 182), 36, (255, 255, 255), (206, 216, 218), 3)
    text(draw, (120, 87), city, (17, 45, 61), 54, bold=True)
    text(draw, (120, 148), subtitle, (226, 87, 39), 27, bold=True)
    text(draw, (1480, 119), "FOOD MAP", (22, 129, 134), 26, anchor="ra")

    for item in pins:
        pin(draw, *item)

    rounded(draw, (990, 655, 1505, 895), 28, (255, 250, 237), (206, 216, 218), 3)
    text(draw, (1025, 690), landmark[0], (17, 45, 61), 34, bold=True)
    text(draw, (1025, 742), landmark[1], (80, 96, 104), 24)

    if city.startswith("成都"):
        draw.ellipse((1360, 720, 1455, 815), fill="white", outline=(17, 45, 61), width=4)
        draw.ellipse((1346, 702, 1388, 742), fill=(17, 45, 61))
        draw.ellipse((1426, 702, 1468, 742), fill=(17, 45, 61))
        draw.ellipse((1388, 755, 1408, 775), fill=(17, 45, 61))
        draw.ellipse((1418, 755, 1438, 775), fill=(17, 45, 61))
    elif city.startswith("重慶"):
        draw.rectangle((1320, 730, 1455, 820), fill=(184, 91, 59), outline=(17, 45, 61), width=4)
        for yy in [755, 785]:
            draw.line((1320, yy, 1455, yy), fill=(255, 214, 132), width=3)
    else:
        draw.polygon([(1350, 800), (1420, 700), (1490, 800)], fill=(226, 87, 39), outline=(17, 45, 61))
        draw.rectangle((1368, 800, 1472, 840), fill=(246, 204, 115), outline=(17, 45, 61), width=3)

    rounded(draw, (78, 820, 945, 930), 28, (255, 255, 255), (206, 216, 218), 3)
    x = 110
    for dish in dishes:
        icon_bowl(draw, x + 32, 875, 0.58, random.choice([(203, 46, 34), (226, 87, 39), (244, 202, 117), (77, 142, 92)]))
        text(draw, (x + 75, 858), dish, (17, 45, 61), 24, bold=True)
        x += 205 if len(dish) < 5 else 235
        if x > 870:
            break

    text(draw, (95, 955), "親子規劃：晚餐回住宿圈，商場與景點同區解決，避開跨城找店與高溫排隊。", (80, 96, 104), 24)
    img.save(OUT / filename, quality=95)


common = {"bg": (235, 247, 243), "mint": (205, 235, 220), "cream": (255, 245, 221), "sky": (213, 238, 247), "water": (123, 197, 209), "water2": (104, 174, 190), "park": (181, 220, 174)}

make_city(
    "food-map-hangzhou.png",
    "杭州美食地圖",
    "湖濱銀泰、西湖湖濱、武林廣場：第一晚輕鬆吃喝散步",
    common,
    "lake",
    [(890, 270, "湖濱銀泰 in77", (226, 87, 39)), (670, 570, "西湖湖濱", (22, 129, 134)), (1030, 510, "武林廣場", (77, 142, 92))],
    ["東坡肉", "龍井蝦仁", "宋嫂魚羹", "片兒川", "蔥包檜", "定勝糕"],
    [[(760, 310), (930, 270), (1160, 350)], [(520, 650), (730, 575), (1030, 510)], [(920, 270), (1020, 420), (1110, 560)]],
    ("湖濱住宿最省力", "晚上用餐、散步、補給都在同一圈"),
)

make_city(
    "food-map-chengdu.png",
    "成都美食地圖",
    "春熙路、太古里、IFS、人民公園、寬窄巷子：火鍋川菜小吃集中",
    {"bg": (239, 247, 232), "mint": (212, 235, 213), "cream": (255, 243, 219), "sky": (219, 241, 247), "water": (128, 197, 209), "water2": (114, 184, 199), "park": (184, 220, 166)},
    "city",
    [(830, 270, "春熙路 / 太古里", (226, 87, 39)), (1040, 430, "IFS 熊貓地標", (17, 45, 61)), (530, 430, "人民公園茶館", (77, 142, 92)), (420, 630, "寬窄巷子", (137, 99, 61))],
    ["麻婆豆腐", "水煮牛肉", "回鍋肉", "火鍋", "龍抄手", "鐘水餃", "冰粉"],
    [[(420, 630), (530, 430), (830, 270), (1040, 430)], [(780, 710), (930, 520), (1040, 430)], [(300, 760), (420, 630), (830, 270)]],
    ("上午戶外、午後商場", "IFS / 太古里 / 萬象城做避暑備案"),
)

make_city(
    "food-map-chongqing.png",
    "重慶美食地圖",
    "解放碑、來福士、朝天門、洪崖洞、觀音橋：山城夜景與火鍋小麵",
    {"bg": (235, 241, 247), "mint": (214, 232, 219), "cream": (255, 240, 219), "sky": (209, 230, 244), "water": (81, 159, 184), "water2": (70, 140, 170), "park": (184, 215, 176)},
    "rivers",
    [(730, 390, "解放碑", (226, 87, 39)), (1010, 355, "來福士 / 朝天門", (22, 129, 134)), (1130, 600, "洪崖洞夜景", (205, 83, 49)), (500, 650, "觀音橋商圈", (77, 142, 92))],
    ["重慶小麵", "豌雜麵", "重慶火鍋", "毛肚", "鴨腸", "江湖魚", "冰粉"],
    [[(500, 650), (730, 390), (1010, 355)], [(730, 390), (950, 500), (1130, 600)], [(500, 650), (680, 730), (1130, 600)]],
    ("山城移動要省腿力", "住宿圈吃晚餐，洪崖洞以夜景小吃為主"),
)
