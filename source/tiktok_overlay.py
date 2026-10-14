#!/usr/bin/env python3
"""tiktok_overlay: put the REAL TikTok app screen over a finished video, to see what the app covers.

Measured from a screenshot of the For You feed on Sam's iPhone (1170 x 2532 pixels): the status bar, the top tabs and
search, the right-hand column (avatar and follow, like, comments, save, share, sound), the username and description at
the bottom left, the progress line and the black menu bar. The video fills the screen above the menu bar, so a 9:16
video is trimmed a little at both sides, exactly as the app does.

  python3 source/tiktok_overlay.py check SCREENSHOT.png OUT.jpg     the layer drawn over the screenshot (alignment)
  python3 source/tiktok_overlay.py video IN.mp4 OUT.mp4             the video inside the phone, the app on top
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PH = 1170, 2532                         # the phone screen in pixels
K = PW / 924                                # the measurements below are in points of a 924-wide screen
NAV = 1805                                  # the top of the black menu bar (points)
BOLD = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')
MED = os.path.join(HERE, 'fonts', 'TikTokSans-Medium.woff')
WHITE = (255, 255, 255, 255)


def f(path, size):
    return ImageFont.truetype(path, int(size * K))


def P(*v):
    return [x * K for x in v]


def ui_layer():
    """The app's own screen, transparent where the video shows through."""
    lay = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # the black menu bar and its five buttons
    d.rectangle(P(0, NAV, 924, 2000), fill=(0, 0, 0, 255))
    for x, label in ((92, 'Home'), (277, 'Shop'), (646, 'Inbox'), (831, 'Profile')):
        d.text((x * K, 1895 * K), label, font=f(BOLD, 24), fill=WHITE, anchor='mm')
        d.rounded_rectangle(P(x - 22, 1825, x + 22, 1868), 8 * K, outline=WHITE, width=int(4 * K))
    d.rounded_rectangle(P(410, 1828, 514, 1893), 18 * K, fill=(255, 255, 255, 255))
    d.text((462 * K, 1860 * K), '+', font=f(BOLD, 56), fill=(0, 0, 0, 255), anchor='mm')
    # the progress line
    d.line(P(28, 1797, 896, 1797), fill=(255, 255, 255, 90), width=int(3 * K))
    d.line(P(28, 1797, 100, 1797), fill=(255, 255, 255, 230), width=int(3 * K))
    # everything white sits on a soft shadow, as in the app
    w = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    g = ImageDraw.Draw(w)
    g.text((68 * K, 58 * K), '23:24', font=f(BOLD, 36), fill=WHITE, anchor='lm')               # status bar
    for i, h in enumerate((10, 16, 22, 28)):
        g.rectangle(P(716 + i * 10, 74 - h, 722 + i * 10, 74), fill=WHITE if i < 2 else (255, 255, 255, 120))
    g.pieslice(P(770, 38, 810, 78), 225, 315, fill=WHITE)
    g.rounded_rectangle(P(822, 46, 872, 74), 7 * K, fill=(250, 230, 70, 255))
    g.text((847 * K, 60 * K), '66', font=f(BOLD, 22), fill=(0, 0, 0, 255), anchor='mm')
    g.rounded_rectangle(P(40, 138, 94, 186), 8 * K, outline=WHITE, width=int(4 * K))           # LIVE
    g.text((67 * K, 168 * K), 'LIVE', font=f(BOLD, 18), fill=WHITE, anchor='mm')
    for x, tab, a in ((120, 't Sussex', 140), (300, 'Following', 220), (500, 'Friends', 220), (660, 'For You', 255)):
        g.text((x * K, 163 * K), tab, font=f(BOLD, 34), fill=(255, 255, 255, a), anchor='lm')
    g.rectangle(P(702, 205, 757, 210), fill=WHITE)
    g.ellipse(P(836, 140, 874, 178), outline=WHITE, width=int(5 * K))                           # search
    g.line(P(868, 172, 884, 188), fill=WHITE, width=int(5 * K))
    # the right-hand column
    g.ellipse(P(812, 730, 892, 810), outline=(255, 255, 255, 200), width=int(5 * K))           # the round button
    g.ellipse(P(800, 858, 904, 962), fill=(200, 170, 150, 255), outline=WHITE, width=int(4 * K))   # avatar
    g.ellipse(P(828, 941, 876, 989), fill=(234, 38, 72, 255))
    g.text((852 * K, 965 * K), '+', font=f(BOLD, 40), fill=WHITE, anchor='mm')
    heart = [(852, 1110), (818, 1078), (814, 1060), (822, 1048), (836, 1046), (852, 1060), (868, 1046), (882, 1048),
             (890, 1060), (886, 1078)]
    g.polygon([(x * K, y * K) for x, y in heart], fill=WHITE)
    g.ellipse(P(819, 1206, 885, 1262), fill=WHITE)
    g.polygon(P(836, 1255, 830, 1272, 850, 1258), fill=WHITE)
    g.polygon(P(828, 1364, 876, 1364, 876, 1420, 852, 1402, 828, 1420), fill=WHITE)            # save
    g.polygon(P(820, 1560, 850, 1530, 850, 1518, 884, 1550, 850, 1582, 850, 1566), fill=WHITE)  # share
    for y, n in ((1138, '401K'), (1294, '6,169'), (1450, '34.4K'), (1606, '97.5K')):
        g.text((852 * K, y * K), n, font=f(BOLD, 28), fill=WHITE, anchor='mm')
    g.ellipse(P(805, 1675, 899, 1769), fill=WHITE)                                               # sound off
    # the username and the description, bottom left
    g.text((30 * K, 1650 * K), 'I am happy tour', font=f(BOLD, 38), fill=WHITE, anchor='lm')
    g.text((30 * K, 1718 * K), 'Did I ever complain? #bornalone', font=f(MED, 35.5), fill=WHITE, anchor='lm')
    g.text((30 * K, 1758 * K), '#absurdhumor #deadpan ... more', font=f(MED, 35.5), fill=WHITE, anchor='lm')
    sh = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    sh.putalpha(w.getchannel('A').point(lambda v: v * 0.45).filter(ImageFilter.GaussianBlur(4)))
    lay.alpha_composite(sh)
    lay.alpha_composite(w)
    return lay


def place(frame):
    """A 9:16 video frame as the app shows it: filling the screen above the menu bar, trimmed at the sides."""
    h = int(NAV * K)
    w = int(round(frame.width * h / frame.height))
    big = frame.convert('RGB').resize((w, h), Image.LANCZOS)
    x0 = (w - PW) // 2
    screen = Image.new('RGB', (PW, PH), (0, 0, 0))
    screen.paste(big.crop((x0, 0, x0 + PW, h)), (0, 0))
    return screen


def video(src, out):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    ui = ui_layer()
    rd = imageio_ffmpeg.read_frames(src)
    meta = next(rd)
    sw, sh_ = meta['size']
    fps = meta['fps']
    p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '586x1268',
                          '-r', str(fps), '-i', '-', '-i', src, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '24',
                          '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out],
                         stdin=subprocess.PIPE)
    for raw in rd:
        fr = Image.frombuffer('RGB', (sw, sh_), raw)
        sc = place(fr).convert('RGBA')
        sc.alpha_composite(ui)
        p.stdin.write(np.asarray(sc.convert('RGB').resize((586, 1268), Image.LANCZOS)).tobytes())
    p.stdin.close()
    p.wait()
    print(out, f'{os.path.getsize(out) / 1e6:.1f} MB')


def main():
    a = sys.argv[1:]
    if a[0] == 'check':
        shot = Image.open(a[1]).convert('RGBA').resize((PW, PH))
        shot.alpha_composite(Image.new('RGBA', (PW, PH), (0, 0, 0, 110)))
        shot.alpha_composite(ui_layer())
        shot.convert('RGB').resize((PW // 2, PH // 2)).save(a[2], quality=88)
    elif a[0] == 'video':
        video(a[1], a[2])


if __name__ == '__main__':
    main()
