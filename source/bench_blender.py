"""MAP  bench_blender: the same test-bench frame drawn by Blender (learn step L2, proposal solid-body-moves, chat 33):
flat toon fills (each house colour as an unlit flat colour) and Line Art outlines (Blender's outline maker: the
silhouettes, part borders and where things cross, worked out from the 3D scene), the house head as a picture laid at
the head's depth, house circle hands as balls. Reads the folder bench_draw.py `blender` wrote.

    blender -b --factory-startup -P source/bench_blender.py -- DIR OUT.png
"""
import json
import math
import os
import sys
import time

import bpy
from mathutils import Vector

d, out = sys.argv[sys.argv.index('--') + 1:][:2]
cfg = json.load(open(os.path.join(d, 'scene.json')))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
t0 = time.time()


def flat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = [(c / 255.0) ** 2.2 for c in rgb] + [1]
    o = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(em.outputs[0], o.inputs[0])
    return m


for f in ('jason', 'car', 'gun', 'hands'):
    bpy.ops.wm.obj_import(filepath=os.path.join(d, f + '.obj'), forward_axis='Y', up_axis='Z')
for ob in list(sc.objects):
    if ob.type == 'MESH':
        for slot in ob.material_slots:
            if slot.material:
                nm = slot.material.name.split('.')[0]
                slot.material = flat('house_' + nm, cfg['cols'].get(nm, (128, 128, 128)))
        ob.data.shade_flat()

# the camera: shot 4's locked camera (car frame -> Blender: x, z, y); focal 2000 px on a 1080 px wide frame
(px, py, pz), (ax, ay, az), focal = cfg['cam']
cam_d = bpy.data.cameras.new('cam')
cam_d.sensor_fit = 'HORIZONTAL'
cam_d.sensor_width = 36.0
cam_d.lens = focal / 1080.0 * 36.0
cam_d.clip_start = 0.12
cam = bpy.data.objects.new('cam', cam_d)
sc.collection.objects.link(cam)
cam.location = (px, pz, py)
look = Vector((ax, az, ay)) - cam.location
cam.rotation_euler = look.to_track_quat('-Z', 'Y').to_euler()
sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.film_transparent = True
sc.render.engine = 'BLENDER_EEVEE'
sc.view_settings.view_transform = 'Standard'
sc.eevee.taa_render_samples = 8

# the house head: a picture filling the frame, set at the head's depth so nearer things (the roof rail) hide it
dep = cfg['head_depth']
img = bpy.data.images.load(os.path.join(d, 'head.png'))
m = bpy.data.materials.new('head')
m.use_nodes = True
m.blend_method = 'BLEND'
nt = m.node_tree
nt.nodes.clear()
tx = nt.nodes.new('ShaderNodeTexImage')
tx.image = img
em = nt.nodes.new('ShaderNodeEmission')
tr = nt.nodes.new('ShaderNodeBsdfTransparent')
mx = nt.nodes.new('ShaderNodeMixShader')
o = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(tx.outputs['Color'], em.inputs['Color'])
nt.links.new(tx.outputs['Alpha'], mx.inputs[0])
nt.links.new(tr.outputs[0], mx.inputs[1])
nt.links.new(em.outputs[0], mx.inputs[2])
nt.links.new(mx.outputs[0], o.inputs[0])
w, h = 1080 / focal * dep, 1920 / focal * dep
bpy.ops.mesh.primitive_plane_add(size=1)
pl = bpy.context.object
pl.scale = (w, h, 1)
pl.rotation_euler = cam.rotation_euler
pl.location = cam.location + cam.matrix_world.to_quaternion() @ Vector((0, 0, -dep))
pl.data.materials.append(m)
pl.lineart.usage = 'EXCLUDE'

# Line Art: the outlines from the scene's 3D shapes, in house ink
bpy.ops.object.gpencil_add(type='LRT_SCENE')
gp = bpy.context.object
la = gp.grease_pencil_modifiers[0]
la.thickness = int(os.environ.get('LA_THICK', '4'))
la.use_contour = la.use_crease = la.use_material = la.use_intersection = True
la.use_edge_mark = False
la.crease_threshold = math.radians(float(os.environ.get("LA_CREASE", "115")))
la.chaining_image_threshold = 0.002
la.use_overlap_edge_type_support = True
gm = gp.data.materials[0] if gp.data.materials else None
if gm:
    gm.grease_pencil.color = [(c / 255.0) ** 2.2 for c in cfg['ink']] + [1]
bpy.context.view_layer.update()
sc.render.filepath = out
t1 = time.time()
bpy.ops.render.render(write_still=True)
print('BLENDER scene build s %.1f render s %.1f' % (t1 - t0, time.time() - t1))
