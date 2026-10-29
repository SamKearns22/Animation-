#!/usr/bin/env python3
"""Story post still for Halo No-No: Musk and Cortana in the car, Musk looking over at her, two cranberry texts.
    python3 source/halo_story.py OUT.png
Safe area x 60-900, y 310-1500 (guides/tiktok-design.md)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                      # noqa: E402
import halo_no_no as H                   # noqa: E402

HS, HC = H.HS, H.HC
TEXT_1 = ['WHEN YOUR ANNOYING', 'GF POINTS OUT']
TEXT_2 = ["THAT YOU DON'T", 'ACTUALLY MIND THE WEST', 'GETTING INVADED']


def still():
    B.SS = 1
    cam, t = B.Cam(1.1, 508, 1010), 26.0   # a little nearer than the film's wide, seats lower so text 1 clears Cortana
    img = B.canvas(HS.SPACE)
    HS.cabin_back(img, cam, t, None, False)
    HC.chief(img, cam, *HS.MUSK, dict(mouth='rest', look=-1.0, blink=False, turn=0.0, lean=0.0), t)
    HC.cortana(img, cam, HS.CORTANA_AT[0], H.cortana_y(t), H.C_SCALE,
               dict(pose='point', hip=-0.8, mouth='smile', look=1.0, blink=False, appear=1.0, flicker=0.0), t)
    HS.cabin_front(img, cam)
    B.title_lines(img, TEXT_1, cap=62, top=324)
    B.title_lines(img, TEXT_2, cap=50, top=1300)
    return img.convert('RGB')


if __name__ == '__main__':
    still().save(sys.argv[1])
    print('wrote', sys.argv[1])
