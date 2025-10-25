from PIL import Image, ImageDraw, ImageFont

def create_donut_image(size, slices, center_text):
    img = Image.new("RGBA", (size, size), (255,255,255,0))
    draw = ImageDraw.Draw(img)
    bbox = (4,4,size-4,size-4)
    start = -90
    for perc, color in slices:
        end = start + (perc/100)*360
        draw.pieslice(bbox, start, end, fill=color)
        start = end

    inner = size*0.58
    left = (size - inner)/2
    draw.ellipse((left, left, left + inner, left + inner), fill=(31, 41, 55, 255))
    fnt = ImageFont.load_default()
    try:
        fnt = ImageFont.truetype("arial.ttf", size//8)
    except:
        pass

    bbox = draw.textbbox((0, 0), center_text, font=fnt)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) // 2, (size - h) // 2), center_text, font=fnt, fill="white")

    return img