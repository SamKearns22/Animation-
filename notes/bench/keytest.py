import sys,time;import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'source'))
import bench_move as M, numpy as np
print('seat y',round(M.fit_seat(),3),'knee r',round(M.fit_knee(),3),'ankle y',round(M.fit_ankles(),3))
for k in ['K1','K2','K3','K4','K5']:
    g=M.key(k); o=M.solve(g); c=M.check_frame(o,g)
    print(k, {n:v for n,v in c.items() if v}, 'aim',round(M.aim_err(o),2), 'pel',o['pel'].round(2),'shR',o['J']['shR'].round(2),'head',o['J']['head'].round(2))
