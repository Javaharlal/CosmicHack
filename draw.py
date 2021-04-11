import fill


def rect(ctx, x, y, w, h, color="#000", width=1):
    ctx.create_line(x,     y,     x + w, y,     fill=color, width=width)
    ctx.create_line(x + w, y,     x + w, y + h, fill=color, width=width)
    ctx.create_line(x + w, y + h, x,     y + h, fill=color, width=width)
    ctx.create_line(x,     y + h, x,     y,     fill=color, width=width)


def pixel(ctx, x, y, color="#000"):
    ctx.create_line((x, y) * 2, fill=color)


def button(ctx, button):
    if button["nowHover"]:
        fill.rect(ctx,
                  button['x'],
                  button['y'],
                  button["w"],
                  button["h"],
                  button["borderHoverColor"])
        fill.rect(ctx,
                  button['x'] + button["borderWidth"],
                  button['y'] + button["borderWidth"],
                  button['w'] - 2 * button["borderWidth"],
                  button['h'] - 2 * button["borderWidth"],
                  button["backgroundHoverColor"])
        fill.text(ctx, button['x'] + button['w'] / 2, button['y'] + button['h'] / 2, text=button["text"])
    else:
        fill.rect(ctx,
                  button['x'],
                  button['y'],
                  button["w"],
                  button["h"],
                  button["borderColor"])
        fill.rect(ctx,
                  button['x'] + button["borderWidth"],
                  button['y'] + button["borderWidth"],
                  button['w'] - 2 * button["borderWidth"],
                  button['h'] - 2 * button["borderWidth"],
                  button["backgroundColor"])
        fill.text(ctx, button['x'] + button['w'] / 2, button['y'] + button['h'] / 2, text=button["text"])

def cursor(ctx, cursor):
    if cursor.rect:
        fill.rect(ctx, cursor.x, cursor.y,
                  cursor.width, cursor.height, cursor.color)
    else:
        fill.circle(ctx, cursor.x, cursor.y, cursor.radius, cursor.color)