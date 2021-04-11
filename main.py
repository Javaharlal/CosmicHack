from gui import *
from google_trans_new import google_translator as Translator
import requests, fill, draw, tkinter as tk, sqlite3 as sql


def check():
    main.after(30, check)
    if not (380 <= cursor.x and 30 <= cursor.y <= 120):
        canvas.delete("all")
        draw.cursor(canvas, cursor)
        for i in range(len(scene.buttons)):
            draw.button(canvas, scene.buttons[i])
        for i in range(4):
            fill.text(canvas, 5,   35 + 25 * i, names[i], anchor="w")
            fill.text(canvas, 105, 35 + 25 * i, heights[i], anchor="w")
            fill.text(canvas, 205, 35 + 25 * i, diameters[i], anchor="w")
            fill.text(canvas, 300, 35 + 25 * i, masses[i], anchor="w")
            entry = tk.Entry(width=15)
            entry.place(x=395, y=30 + 25 * i)
            entry.insert(0, fuels[i])
            entry1 = tk.Entry(width=15)
            entry1.place(x=495, y=30 + 25 * i)
            entry1.insert(0, descriptions[i])
            entry2 = tk.Entry(width=22)
            entry2.place(x=595, y=30 + 25 * i)
            entry2.insert(0, links[i])


def createScene():
    translator = Translator()
    response = requests.get("https://api.spacexdata.com/v4/rockets").json()
    with sql.connect("spacex.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS spacex ("Название" TEXT,
                                                          "Высота, м" FLOAT,
                                                          "Диаметр, м" FLOAT,
                                                          "Масса, кг" INTEGER,
                                                          "Топливо" TEXT,
                                                          "Описание" TEXT,
                                                          "Сраница на Википедии" TEXT)""")
        if not [*cur.execute("SELECT * FROM spacex")]:
            print("Создание базы данных")
            for i in range(len(response)):
                rockets.append({"Название": response[i]["name"],
                                "Высота, м": response[i]["height"]["meters"],
                                "Диаметр, м": response[i]["diameter"]["meters"],
                                "Масса, кг": response[i]["mass"]["kg"],
                                "Топливо": translator.translate(response[i]["engines"]["propellant_1"] + ", " +
                                                                response[i]["engines"]["propellant_2"],
                                                                lang_src='en',
                                                                lang_tgt='ru'),
                                "Описание": translator.translate(response[i]["description"],
                                                                 lang_src='en',
                                                                 lang_tgt='ru'),
                                "Сраница на Википедии": response[i]["wikipedia"].replace("en", "ru")})
            for rocket in rockets:
                cur.execute(f"""
                    INSERT INTO spacex VALUES("{rocket["Название"]}",
                                               {rocket["Высота, м"]},
                                               {rocket["Диаметр, м"]},
                                               {rocket["Масса, кг"]},
                                              "{rocket["Топливо"]}",
                                              "{rocket["Описание"]}",
                                              "{rocket["Сраница на Википедии"]}")""")
        cur.execute(f"SELECT * FROM spacex ORDER BY {sorting} DESC")
    scene.addButton(2,   2, 100, 20, text="Название")
    scene.addButton(100, 2, 100, 20, text="Высота, м")
    scene.addButton(198, 2, 100, 20, text="Диаметр, м")
    scene.addButton(296, 2, 100, 20, text="Масса, кг")
    scene.addButton(394, 2, 100, 20, text="Топливо")
    scene.addButton(492, 2, 100, 20, text="Описание")
    scene.addButton(590, 2, 150, 20, text="Сраница на Википедии")

    # with sql.connect("spacex.db") as con:
    #     cur = con.cursor()
    #     for i in range(4):
    #         fill.text(canvas, 5, 35 + 20 * i, text=names[i], anchor="w")
    #         fill.text(canvas, 105, 35 + 20 * i, text=heights[i], anchor="w")
    #         fill.text(canvas, 205, 35 + 20 * i, text=diameters[i], anchor="w")
    #         fill.text(canvas, 300, 35 + 20 * i, text=masses[i], anchor="w")
    #         fill.text(canvas, 400, 35 + 20 * i, text=fuels[i], anchor="w")
    #         # fill.text(canvas, 500, 35 + 20 * i, text=descriptions[i], anchor="w")
    #         # fill.text(canvas, 600, 35 + 20 * i, text=links[i], anchor="w")



def catchClick(event):
    cursor.click = True
    cursor.clickX, cursor.clickY = event.x, event.y


def opt():
    global activeButton
    activeButton = -1
    main.after(1, opt)
    for i in range(len(scene.buttons)):
        if scene.buttons[i]['x'] <= main.winfo_pointerx() - main.winfo_x() - 30 <= scene.buttons[i]['x'] + \
                scene.buttons[i]['w'] and scene.buttons[i]['y'] <= main.winfo_pointery() - \
                main.winfo_y() - 30 <= scene.buttons[i]['y'] + scene.buttons[i]['h'] + 5:
            scene.buttons[i]["nowHover"] = True
            activeButton = i
            if cursor.click:
                cursor.click = False
                sorting = scene.buttons[activeButton]["text"]
                createScene()
                with sql.connect("spacex.db") as con:
                    cur = con.cursor()
                    names = [str(*i) for i in cur.execute(f"SELECT \"Название\" FROM spacex ORDER BY {sorting} DESC")]
                    heights = [str(*i) for i in cur.execute(f"SELECT \"Высота, м\" FROM spacex ORDER BY {sorting} DESC")]
                    diameters = [str(*i) for i in cur.execute(f"SELECT \"Диаметр, м\" FROM spacex ORDER BY {sorting} DESC")]
                    masses = [str(*i) for i in cur.execute(f"SELECT \"Масса, кг\" FROM spacex ORDER BY {sorting} DESC")]
                    fuels = [str(*i) for i in cur.execute(f"SELECT \"Топливо\" FROM spacex ORDER BY {sorting} DESC")]
                    descriptions = [str(*i) for i in cur.execute(f"SELECT \"Описание\" FROM spacex ORDER BY {sorting} DESC")]
                    links = [str(*i) for i in cur.execute(f"SELECT \"Страница на Википедии\" FROM spacex ORDER BY {sorting} DESC")]
        else:
            scene.buttons[i]["nowHover"] = False
    if cursor.click:
        cursor.click = False

    if activeButton >= 0:
        cursor.rect = True
        if cursor.width < scene.buttons[activeButton]['w']:
            cursor.width += 2
        if cursor.height < scene.buttons[activeButton]['h'] + 2:
            cursor.height += 1
        if cursor.width > scene.buttons[activeButton]['w']:
            cursor.width -= 1
        if cursor.height > scene.buttons[activeButton]['h'] + 2:
            cursor.height -= 1
        if cursor.x < scene.buttons[activeButton]['x']:
            cursor.x += 1
        if cursor.x > scene.buttons[activeButton]['x']:
            cursor.x -= 1
        if cursor.y < scene.buttons[activeButton]['y']:
            cursor.y += 1
        if cursor.y > scene.buttons[activeButton]['y']:
            cursor.y -= 0.5
    else:
        cursor.x, cursor.y, cursor.lastX, cursor.lastY = main.winfo_pointerx() - main.winfo_x() - 30, \
                                                         main.winfo_pointery() - main.winfo_y() - 30, \
                                                         cursor.x, cursor.y
        cursor.rect = False
        cursor.width = cursor.radius * 2
        cursor.height = cursor.radius * 2

sorting = "Название"
activeButton = -1
rockets = []
cursor = Cursor(3)
main = tk.Tk()
main.config(cursor="none")
canvas = tk.Canvas(main, bg='white', height=600, width=738)
canvas.pack()
scene = Scene()
cursor = Cursor(3)
createScene()
with sql.connect("spacex.db") as con:
    cur = con.cursor()
    names = [str(*i) for i in cur.execute("SELECT \"Название\" FROM spacex")]
    heights = [str(*i) for i in cur.execute("SELECT \"Высота, м\" FROM spacex")]
    diameters = [str(*i) for i in cur.execute("SELECT \"Диаметр, м\" FROM spacex")]
    masses = [str(*i) for i in cur.execute("SELECT \"Масса, кг\" FROM spacex")]
    fuels = [str(*i) for i in cur.execute("SELECT \"Топливо\" FROM spacex")]
    descriptions = [str(*i) for i in cur.execute("SELECT \"Описание\" FROM spacex")]
    links = [str(*i) for i in cur.execute("SELECT \"Страница на Википедии\" FROM spacex")]
main.bind("<Button-1>", catchClick)
main.after(1000, check)
main.after(1000, opt)
main.mainloop()
