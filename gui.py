class Scene:
    def __init__(self):
        self.buttons = []
        self.texts = []

    def addButton(self, x, y, w, h,
                        onClick=lambda: print("click!"),
                        border=2, borderColor="#aaa",
                        borderHover="#ccc",
                        bgColor="#fff",
                        bgHover="#fff",
                        text="text",
                        textSize=10):
        self.buttons.append({'x': x,
                           'y': y,
                           'w': w,
                           'h': h,
                           "text": text,
                           "clicked": False,
                           "nowHover": False,
                           "onClick": onClick,
                           "textSize": textSize,
                           "borderWidth": border,
                           "borderColor": borderColor,
                           "backgroundColor": bgColor,
                           "borderHoverColor": borderHover,
                           "backgroundHoverColor": bgHover})


class Cursor:
    def __init__(self, radius=5, color="#bbb"):
        self.x = 0
        self.y = 0
        self.lastX = 0
        self.lastY = 0
        self.clickX = 0
        self.clickY = 0
        self.normalRadius = radius
        self.radius = radius
        self.color = color
        self.click = False
        self.rect = False
        self.width = radius * 2
        self.height = radius * 2
