def rect(ctx, x, y, w, h, color="#000"):
    ctx.create_rectangle(x, y, x + w, y + h, fill=color, width=0, tag="rect")


def circle(ctx, x, y, radius, color="#000"):
    ctx.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, width=0, tag="rect")


def text(ctx, x=0, y=0, text="text", size=10, color="#000", anchor="c"):
    ctx.create_text(x, y, text=text, font=('Consolas', size), fill=color, anchor=anchor)