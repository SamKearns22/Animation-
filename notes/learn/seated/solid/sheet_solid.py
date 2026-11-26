"""R7 chat 6 (proposal seated-legs-3d, Learn 2): sheet v4's twelve tiles with the solid legs (solid_seat), same
camera, poses and crop as sheet_r7.py. python3 notes/learn/seated/solid/sheet_solid.py OUT [legs|whole]"""
import os, sys, time
sys.path.insert(0, 'source')
from PIL import Image, ImageDraw, ImageFont
import castsheet as CS
import sitting as S
import solid_seat as SO
cast, PP = CS._setup('brexit-is-done', None)
B, V = PP.B, PP.V
MODE = sys.argv[2] if len(sys.argv) > 2 else 'legs'
VIEWS = ((0, 'upright', 'front'), (45, 'upright', 'three-quarter'), (90, 'upright', 'side'),
         (-45, 'cross, knee over knee', 'legs crossed'))


def tile(who, yaw, pose, full=False):
    sp = dict(cast[who]); sp['seat_r7'] = True; sp['seat_solid'] = MODE
    if MODE == 'body' and 'turned_curves' not in sp:
        sp['turned_curves'] = 0.0   # R7 chat 10: Sam's "way too curvaceous": both three-quarters hang straight like
        sp['turned_bust'] = 0.6     # her boxy jacket (his Y, 26 Nov), with "a very small amount of bust bump ... The
        #                             side view is a good representation" (Sam, 26 Nov)
    img = Image.new('RGBA', (1080, 1920), (232, 232, 226, 255))
    s = 0.5 * sp['height'] / 1.75
    V.person(img, B.Cam(2.0, 540, 470), 540, 840 - 928 * s, s, sp, 0.0, yaw, S.pose(sp, pose))
    chk = SO.checks()
    return (img.convert('RGB') if full else img.convert('RGB').crop((240, 1180, 840, 1740))), chk


if __name__ == '__main__':
    t0 = time.time()
    f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
    tw, th = 600, 560
    page = Image.new('RGB', (160 + 4 * (tw + 20), 110 + 3 * (th + 20)), 'white'); d = ImageDraw.Draw(page)
    for c, (_, _, n) in enumerate(VIEWS):
        d.text((160 + c * (tw + 20) + tw // 2 - 90, 60), n, fill='black', font=f2)
    for r, who in enumerate(('May', 'Kemi', 'Blair')):
        y = 110 + r * (th + 20)
        d.text((20, y + th // 2 - 15), who, fill='black', font=f2)
        for c, (yaw, pose, n) in enumerate(VIEWS):
            t, chk = tile(who.lower(), yaw, pose)
            page.paste(t, (160 + c * (tw + 20), y))
            print(who, n, chk)
    page = page.resize((page.width * 2 // 3, page.height * 2 // 3), Image.LANCZOS)
    page.save(sys.argv[1], quality=85)
    print(sys.argv[1], os.path.getsize(sys.argv[1]) // 1024, 'KB', round(time.time() - t0), 's')
