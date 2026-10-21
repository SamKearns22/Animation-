// Strictly Crabs Dancing: two real-looking crabs dance a Latin routine on the Strictly floor.
// Runs in headless Chromium (render.mjs). Crab parts are "pillows" cut from Sam's photos (prep.py).
// Times are in dance seconds: 0 = 9.0 s into the music; beats every 60/136 s from 0.302 s.
import * as THREE from 'three';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const Q = new URLSearchParams(location.search);
const W = +(Q.get('w') || 1280), H = +(Q.get('h') || 720);
const BEAT = 60 / 136, B0 = 0.302;
const D2R = Math.PI / 180;
const V3 = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const UP = V3(0, 1, 0);

// ---------------------------------------------------------------- renderer, set, lights
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05020a);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.25;
scene.fog = new THREE.Fog(0x140a22, 9, 22);

const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 100);
const loader = new THREE.TextureLoader();
const tex = async (f) => { const t = await loader.loadAsync('tex/' + f); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };

// the ballroom, far behind and out of focus
const plateTex = await tex('plate.jpg');
const plate = new THREE.Mesh(new THREE.PlaneGeometry(40, 15), new THREE.MeshBasicMaterial({ map: plateTex, toneMapped: false, fog: false }));
plate.position.set(0, 6.0, -15);
scene.add(plate);

// polished dance floor: a mirror under a dark glossy film, plus a layer that only catches shadows
const mirror = new Reflector(new THREE.PlaneGeometry(50, 50), { textureWidth: W, textureHeight: H, color: 0x8a8a96 });
mirror.rotation.x = -Math.PI / 2; mirror.position.set(0, 0, -5);
scene.add(mirror);
const film = new THREE.Mesh(new THREE.PlaneGeometry(50, 50), new THREE.MeshStandardMaterial({ color: 0x1a0f24, roughness: 0.35, metalness: 0.0, transparent: true, opacity: 0.72 }));
film.rotation.x = -Math.PI / 2; film.position.set(0, 0.001, -5); film.receiveShadow = true;
scene.add(film);
const shadowCatch = new THREE.Mesh(new THREE.PlaneGeometry(50, 50), new THREE.ShadowMaterial({ opacity: 0.55 }));
shadowCatch.rotation.x = -Math.PI / 2; shadowCatch.position.set(0, 0.002, -5); shadowCatch.receiveShadow = true;
scene.add(shadowCatch);

scene.add(new THREE.HemisphereLight(0x9a7cff, 0x1a0a20, 0.55));
const key = new THREE.DirectionalLight(0xfff1dc, 2.6);
key.position.set(2.5, 8, 6); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6, near: 1, far: 25 });
key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02; key.shadow.radius = 4;
scene.add(key);
for (const [x, c] of [[-5, 0xff3fa8], [5, 0x5a6bff]]) {
  const p = new THREE.PointLight(c, 45, 0, 2); p.position.set(x, 3.2, -3); scene.add(p);
}
const front = new THREE.PointLight(0xfff2e6, 9, 0, 2); front.position.set(0, 2.5, 6); scene.add(front);

// ---------------------------------------------------------------- pillow parts
const PARTS = await (await fetch('tex/parts.json')).json();
async function heights(f) {
  const im = new Image(); im.src = 'tex/' + f; await im.decode();
  const c = document.createElement('canvas'); c.width = im.width; c.height = im.height;
  const g = c.getContext('2d'); g.drawImage(im, 0, 0);
  const d = g.getImageData(0, 0, im.width, im.height).data;
  return (u, v) => {
    const x = u * (im.width - 1), y = v * (im.height - 1);
    const x0 = Math.floor(x), y0 = Math.floor(y), x1 = Math.min(x0 + 1, im.width - 1), y1 = Math.min(y0 + 1, im.height - 1);
    const fx = x - x0, fy = y - y0, at = (i, j) => d[(j * im.width + i) * 4] / 255;
    return (at(x0, y0) * (1 - fx) + at(x1, y0) * fx) * (1 - fy) + (at(x0, y1) * (1 - fx) + at(x1, y1) * fx) * fy;
  };
}
// place(u, v, h, side) -> [x, y, z]; side +1 is the upper face, -1 the lower
function pillow(hf, nu, nv, place) {
  const pos = [], uv = [], idx = [];
  for (const side of [1, -1]) {
    const base = pos.length / 3;
    for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++) {
      const u = i / nu, v = j / nv;
      pos.push(...place(u, v, hf(u, v), side)); uv.push(u, 1 - v);
    }
    for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) {
      const a = base + j * (nu + 1) + i, b = a + 1, c = a + nu + 1, d = c + 1;
      if (side > 0) idx.push(a, c, b, b, c, d); else idx.push(a, b, c, b, d, c);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}
const shellMat = (map, rough) => new THREE.MeshPhysicalMaterial({ map, alphaTest: 0.5, side: THREE.DoubleSide, roughness: rough + 0.1, clearcoat: 0.3, clearcoatRoughness: 0.35 });

// a limb segment: x runs 0..1 along the bone (scaled to length each frame), y is thickness, z is width
async function segment(name, width) {
  const p = PARTS[name], hf = await heights(p.hmap);
  const g = pillow(hf, 40, 10, (u, v, h, s) => [u, s * h * (s > 0 ? p.htop : p.hbot) * width, (v - 0.5) * width]);
  return { g, m: shellMat(await tex(p.tex), 0.5), width };
}
async function clawPart(name) {
  const p = PARTS[name], hf = await heights(p.hmap), [L, Wd] = p.size;
  const g = pillow(hf, 80, 36, (u, v, h, s) => [u, s * h * (s > 0 ? p.htop : p.hbot), (v - 0.5) * Wd]);
  return { g, m: shellMat(await tex(p.tex), 0.4), width: Wd, length: L };
}
async function shellPart(name) {
  const p = PARTS[name], hf = await heights(p.hmap), [Wd, L] = p.size;
  const g = pillow(hf, 96, 72, (u, v, h, s) => [(u - 0.5) * Wd, s * h * (s > 0 ? p.htop : p.hbot), (v - 0.5) * L]);
  return { g, m: shellMat(await tex(p.tex), 0.42) };
}
function noiseTex(rgb, spread) {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d'), im = g.createImageData(128, 128);
  for (let i = 0; i < 128 * 128; i++) {
    const n = (Math.random() - 0.5) * spread;
    for (let k = 0; k < 3; k++) im.data[i * 4 + k] = Math.max(0, Math.min(255, rgb[k] + n));
    im.data[i * 4 + 3] = 255;
  }
  g.putImageData(im, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ---------------------------------------------------------------- the crab
const LEG = { rx: [0.36, 0.40, 0.40, 0.36], rz: [0.12, 0.02, -0.09, -0.2], ang: [44, 14, -17, -48], rad: [1.0, 0.98, 0.95, 0.85],
  L1: 0.42, L2: 0.44, carpusFrac: 0.36, dactyl: [0.08, 0.20] };
const ARM = { root: [0.26, 0.04, 0.36], merus: 0.34, carpus: 0.18 };
const DEF = { x: 0, z: 0, y: 0.36, yaw: 0, pitch: 0, roll: 0, spreadL: 1, spreadR: 1, raiseF: 0, air: 0, carry: 0, flat: 0,
  bounce: 0, shimmy: 0, pulse: 0, Lout: 30, Lraise: 32, Lelbow: 35, Lwrist: 0, Rout: 30, Rraise: 32, Relbow: 35, Rwrist: 0 };

class Crab {
  constructor(name, keys) { this.name = name; this.keys = keys; this.meshes = []; }
  async build(sp) {
    const add = (part, castShadow = true) => {
      const m = new THREE.Mesh(part.g, part.m); m.matrixAutoUpdate = false; m.castShadow = castShadow; scene.add(m); this.meshes.push(m); return m;
    };
    this.shell = add(await shellPart('shell_' + sp));
    const under = { g: new THREE.SphereGeometry(1, 40, 20), m: new THREE.MeshPhysicalMaterial({ map: noiseTex(sp === 'shore' ? [140, 92, 50] : [58, 60, 70], 30), roughness: 0.5, clearcoat: 0.3 }) };
    this.under = add(under);
    const seg = {};
    for (const [n, w] of [['merus', 0.2], ['carpus', 0.16], ['propodus', 0.15], ['dactyl', 0.11], ['paddle', 0.26], ['armmerus', 0.2], ['armcarpus', 0.21]])
      seg[n] = await segment(`${n}_${sp}`, w);
    const claw = await clawPart('claw_' + sp);
    this.legs = [];
    for (const s of [1, -1]) for (let i = 0; i < 4; i++) {
      const last = sp === 'velvet' && i === 3 ? seg.paddle : seg.dactyl;   // velvet crabs swim with paddle feet
      this.legs.push({ s, i, foot: null, step: null, parts: [seg.merus, seg.carpus, seg.propodus, last].map(p => ({ p, m: add(p) })) });
    }
    this.arms = [1, -1].map(s => ({ s, parts: [seg.armmerus, seg.armcarpus, claw].map(p => ({ p, m: add(p) })) }));
    this.clawLen = claw.length; this.clawW = claw.width;
  }
  // choreography: each channel eases between the beats where it is keyed
  channels(t) {
    const b = (t - B0) / BEAT, out = { ...DEF };
    for (const ch in DEF) {
      const ks = this.keys.filter(k => ch in k[1]);
      if (!ks.length) continue;
      if (b <= ks[0][0]) { out[ch] = ks[0][1][ch]; continue; }
      if (b >= ks[ks.length - 1][0]) { out[ch] = ks[ks.length - 1][1][ch]; continue; }
      for (let k = 0; k < ks.length - 1; k++) if (b < ks[k + 1][0]) {
        const f = (b - ks[k][0]) / (ks[k + 1][0] - ks[k][0]), e = f * f * (3 - 2 * f);
        out[ch] = ks[k][1][ch] + (ks[k + 1][1][ch] - ks[k][1][ch]) * e; break;
      }
    }
    // rhythm on top: dip on every beat, hips sway over two beats, claws pulse in turn
    const ph = b;
    out.y -= out.bounce * (0.5 + 0.5 * Math.cos(2 * Math.PI * ph));
    out.yaw += out.shimmy * Math.sin(Math.PI * ph);
    out.roll += out.shimmy * 0.6 * Math.sin(Math.PI * ph + 0.6);
    out.Lraise += out.pulse * Math.sin(Math.PI * ph);
    out.Rraise -= out.pulse * Math.sin(Math.PI * ph);
    return out;
  }
  bodyMatrix(c) {
    const m = new THREE.Matrix4().makeTranslation(c.x, c.y, c.z);
    m.multiply(new THREE.Matrix4().makeRotationY(c.yaw * D2R));
    m.multiply(new THREE.Matrix4().makeRotationX(-c.pitch * D2R));
    m.multiply(new THREE.Matrix4().makeRotationZ(c.roll * D2R));
    return m;
  }
  armChain(c, Mb, s) {
    const S = s > 0 ? 'R' : 'L', dirL = (yaw, pitch) => V3(Math.sin(yaw * D2R) * Math.cos(pitch * D2R), Math.sin(pitch * D2R), Math.cos(yaw * D2R) * Math.cos(pitch * D2R));
    const out = c[S + 'out'], raise = c[S + 'raise'], elbow = c[S + 'elbow'], wrist = c[S + 'wrist'];
    const rot = new THREE.Matrix3().setFromMatrix4(Mb);
    const root = V3(s * ARM.root[0], ARM.root[1], ARM.root[2]).applyMatrix4(Mb);
    const d1 = dirL(s * out, raise).applyMatrix3(rot).normalize();
    const e = root.clone().addScaledVector(d1, ARM.merus);
    const d2 = dirL(s * (out - elbow), raise * 0.85).applyMatrix3(rot).normalize();
    const w = e.clone().addScaledVector(d2, ARM.carpus);
    let d3 = dirL(s * (out - elbow - wrist), raise * 0.6).applyMatrix3(rot).normalize();
    if (c.flat > 0) {   // claws held level, like a tray
      const lvl = V3(d3.x, 0, d3.z).normalize();
      d3 = d3.multiplyScalar(1 - c.flat).addScaledVector(lvl, c.flat).normalize();
    }
    const tip = w.clone().addScaledVector(d3, this.clawLen);
    return { root, e, w, tip, d3 };
  }
}

// ---------------------------------------------------------------- choreography (beats; 0 = first beat after the title)
// V = velvet crab (her, screen left), S = shore crab (him, screen right). Both face the camera (+z).
const open = (k, o = 68, r = 50) => ({ [k + 'out']: o, [k + 'raise']: r, [k + 'elbow']: 10, [k + 'wrist']: -10 });
const high = (k, o = 22, r = 78) => ({ [k + 'out']: o, [k + 'raise']: r, [k + 'elbow']: 12, [k + 'wrist']: 0 });
const rest = (k) => ({ [k + 'out']: 30, [k + 'raise']: 32, [k + 'elbow']: 35, [k + 'wrist']: 0 });
const tray = (k, r) => ({ [k + 'out']: 8, [k + 'raise']: r, [k + 'elbow']: 8, [k + 'wrist']: 0 });
const wide = (k) => ({ [k + 'out']: 75, [k + 'raise']: 45, [k + 'elbow']: 5, [k + 'wrist']: 0 });
const both = (f, ...a) => ({ ...f('L', ...a), ...f('R', ...a) });

const KV = [
  [-1, { x: -1.9, z: 0, yaw: 0, y: 0.36, bounce: 0, shimmy: 0, pulse: 0, ...both(rest) }],
  // A: bounce and shimmy, claws sweep open and close
  [0, { bounce: 0.035, shimmy: 7, ...both(rest) }], [2, both(open)], [4, { ...both(rest), pulse: 0 }], [6, { ...both(open), pulse: 12 }],
  // B: scuttle out and back, then hip rolls with a claw waving high
  [8, { x: -1.9, ...both(rest), pulse: 0 }], [10, { x: -2.4 }], [12, { x: -1.9, roll: 0, shimmy: 7, ...rest('L'), ...rest('R') }],
  [12.5, { shimmy: 0 }], [13, { roll: 10, ...high('R') }], [14, { roll: -10, ...open('L') }], [15, { roll: 10 }], [16, { roll: 0, y: 0.36, pitch: 0, spreadL: 1 }],
  // C: the lunge (low, wide on her left), one claw flung high
  [17.5, { y: 0.27, spreadL: 1.15, roll: -10, pitch: 8, ...high('R', 30, 70), ...open('L', 66, 22), bounce: 0.035 }],
  [18, { bounce: 0.015 }], [22, { y: 0.27, spreadL: 1.15, roll: -10, pitch: 8, bounce: 0.015 }],
  [24, { y: 0.36, spreadL: 1, roll: 0, pitch: 0, ...both(rest), yaw: 0, bounce: 0.03, shimmy: 0 }],
  // D: spin, then come forward and across in front of him
  [28, { yaw: -360, x: -1.9, z: 0 }], [30, { x: -1.6, z: 1.5 }], [32, { x: 0, z: 1.5, yaw: -360 }],
  // E: step back to him, hop up onto his claws, ride the spin, come down
  [33, { z: 0.98, y: 0.36, air: 0, bounce: 0.0, carry: 0, ...both(rest) }],
  [33.6, { y: 0.92, air: 1 }], [33.75, { carry: 0 }], [34.25, { carry: 1, yaw: -360 }],
  [45.5, { carry: 1, y: 0.76, air: 1, yaw: 0, x: 0, z: 0.9 }], [45.75, { carry: 0 }], [46.3, { y: 0.76, z: 1.8 }], [46.9, { y: 0.36, air: 0, x: 0, z: 1.8 }],
  // F: back to her mark, then rear up, claws high: the final pose
  [47.5, { x: 0, z: 1.8 }], [49, { x: -1.35, z: 0.8, yaw: 0, pitch: 0, raiseF: 0, y: 0.36, ...both(rest), bounce: 0.03 }],
  [50.5, { pitch: 34, y: 0.56, raiseF: 1, ...both(high), bounce: 0.02, pulse: 10 }],
  [53.5, { pitch: 34, y: 0.56, ...both(high), pulse: 10 }], [54.5, { ...both(open, 60, 60), pulse: 0, bounce: 0 }],
];
const KS = [
  [-1, { x: 1.9, z: 0, yaw: 0, y: 0.36, bounce: 0, shimmy: 0, pulse: 0, ...both(rest) }],
  [0, { bounce: 0.035, shimmy: -7, ...both(rest) }], [2, both(open)], [4, { ...both(rest), pulse: 0 }], [6, { ...both(open), pulse: -12 }],
  [8, { x: 1.9, ...both(rest), pulse: 0 }], [10, { x: 2.4 }], [12, { x: 1.9, shimmy: -7, ...both(rest) }],
  [12.5, { shimmy: 0 }], [13, { ...both(high), pulse: 18, bounce: 0.03 }], [16, { ...both(high), pulse: 0 }],
  // C: he widens and opens up behind her lunge
  [17.5, { spreadL: 1.15, spreadR: 1.15, pitch: 12, ...both(open), bounce: 0.03 }], [22, { spreadL: 1.15, spreadR: 1.15, pitch: 12, ...both(open) }],
  [24, { spreadL: 1, spreadR: 1, pitch: 0, ...both(rest), yaw: 0 }],
  // D: spin, then back off to centre stage
  [28, { yaw: 360, x: 1.9, z: 0, ...both(rest) }], [29, both(high)], [30, { x: 0.9, z: -0.4 }], [32, { x: 0, z: -0.4, yaw: 360, ...both(high) }],
  // E: claws out of her way, swing in under her as she hops, lift, spin, lower, swing out
  [32.6, both(wide)], [33.4, both(wide)], [33.85, { ...both(tray, 20), flat: 1 }],
  [34.25, { ...both(tray, 20) }], [36, { ...both(tray, 55), yaw: 360 }], [44, { yaw: 720, ...both(tray, 55) }],
  [45.5, { ...both(tray, 2), flat: 1 }], [46.4, { ...both(tray, 2), flat: 1 }], [47, { ...both(rest), flat: 0 }], [47.6, both(high)],
  // F: move to his mark and rear up beside her
  [48.3, { x: 0, z: -0.4 }], [49.6, { x: 1.35, z: 0.2, ...both(rest), pitch: 0, y: 0.36, raiseF: 0, bounce: 0.03 }],
  [50.5, { pitch: 34, y: 0.56, raiseF: 1, ...both(high), bounce: 0.02, pulse: -10 }],
  [53.5, { pitch: 34, y: 0.56, ...both(high), pulse: -10 }], [54.5, { ...both(open, 60, 60), pulse: 0, bounce: 0 }],
];

const V = new Crab('her', KV), S = new Crab('him', KS);
await V.build('velvet'); await S.build('shore');

// ---------------------------------------------------------------- posing: body, legs (stepping + IK), claws
function legPose(cr, c, Mb, leg, dt, t) {
  const { s, i } = leg, spread = s > 0 ? c.spreadR : c.spreadL;
  const bodyUp = V3(0, 1, 0).applyMatrix3(new THREE.Matrix3().setFromMatrix4(Mb)).normalize();
  const root = V3(s * LEG.rx[i], -0.03, LEG.rz[i]).applyMatrix4(Mb);
  const a = LEG.ang[i] * D2R, r = LEG.rad[i] * spread;
  const local = V3(s * r * Math.cos(a), 0, r * Math.sin(a)).applyAxisAngle(UP, c.yaw * D2R);
  const desired = V3(c.x + local.x, 0, c.z + local.z);
  // stepping on the floor
  if (!leg.foot || c.air > 0.5) { leg.foot = desired.clone(); leg.step = null; }
  if (leg.step) {
    const f = Math.min(1, (t - leg.step.t0) / leg.step.dur), e = f * f * (3 - 2 * f);
    leg.foot = leg.step.from.clone().lerp(leg.step.to, e); leg.foot.y = 0.09 * Math.sin(Math.PI * f);
    if (f >= 1) { leg.foot.y = 0; leg.step = null; }
  } else if (leg.foot.distanceTo(desired) > 0.1) {
    const busy = cr.legs.filter(l => l.step && ((l.s === s && Math.abs(l.i - i) === 1) || (l.s !== s && l.i === i))).length;
    const n = cr.legs.filter(l => l.step).length;
    const far = V3(leg.foot.x - root.x, 0, leg.foot.z - root.z).length() > 0.66 || leg.foot.distanceTo(desired) > 0.3;
    if ((!busy && n < 5) || far) {
      const lead = desired.clone().sub(leg.foot); if (lead.length() > 0.3) lead.setLength(0.3);
      leg.step = { from: leg.foot.clone(), to: desired.clone().addScaledVector(lead, 0.15), t0: t, dur: 0.1 };
    }
  }
  let foot = leg.foot.clone();
  // front legs lifted (rearing up) and legs spread in the air (being lifted) are held in the body's frame
  const raiseW = i < 2 ? c.raiseF : 0;
  if (raiseW > 0) foot.lerp(V3(s * 0.88, 0.22, 0.18 - 0.25 * i).applyMatrix4(Mb), raiseW);
  if (c.air > 0) foot.lerp(V3(s * r * 1.1 * Math.cos(a), -0.02, r * 1.1 * Math.sin(a)).applyMatrix4(Mb), c.air);
  // ankle above and inside the foot; the dactyl is the last segment
  const U = UP.clone().lerp(bodyUp, Math.max(c.air, raiseW)).normalize();
  const o = foot.clone().sub(root); o.addScaledVector(U, -o.dot(U)); o.normalize();
  const ankle = foot.clone().addScaledVector(o, -LEG.dactyl[0]).addScaledVector(U, LEG.dactyl[1]);
  // two-bone IK, knee up
  const L1 = LEG.L1, L2 = LEG.L2, ra = ankle.clone().sub(root);
  let d = ra.length(); const reach = d <= L1 + L2 - 0.002;
  d = Math.min(Math.max(d, 0.15), L1 + L2 - 0.002);
  const e1 = ra.normalize(), e2 = U.clone().addScaledVector(e1, -U.dot(e1)).normalize();
  const ax = (L1 * L1 - L2 * L2 + d * d) / (2 * d), hy = Math.sqrt(Math.max(0, L1 * L1 - ax * ax));
  const knee = root.clone().addScaledVector(e1, ax).addScaledVector(e2, hy);
  const ank = root.clone().addScaledVector(e1, d);
  if (!reach) foot = ank.clone().addScaledVector(o, LEG.dactyl[0]).addScaledVector(U, -LEG.dactyl[1]);
  const mid = knee.clone().lerp(ank, LEG.carpusFrac);
  const n = e1.clone().cross(U).normalize();
  leg.pts = [root, knee, mid, ank, foot]; leg.n = n; leg.reach = reach;
}

function place(mesh, p0, p1, zHint, extra = 0.015) {
  const X = p1.clone().sub(p0); const len = X.length() + extra; X.normalize();
  const Z = zHint.clone().addScaledVector(X, -zHint.dot(X)).normalize();
  const Y = Z.clone().cross(X);
  mesh.matrix.makeBasis(X.multiplyScalar(len), Y, Z).setPosition(p0.clone().addScaledVector(X.clone().normalize(), -extra / 2));
  mesh.matrixWorldNeedsUpdate = true;
}

const SIM = { t: -1e9, dt: 1 / 120 };
function poseCrabs(t, dt) {
  const cs = S.channels(t); const MbS = S.bodyMatrix(cs);
  const armsS = S.arms.map(a => S.armChain(cs, MbS, a.s));
  const cv = V.channels(t);
  if (cv.carry > 0) {   // she sits on his level claws, facing the way he faces
    const g = armsS.map(a => a.w.clone().addScaledVector(a.d3, S.clawLen * 0.55));
    const seat = g[0].clone().add(g[1]).multiplyScalar(0.5); seat.y += 0.34;
    cv.x += (seat.x - cv.x) * cv.carry; cv.y += (seat.y - cv.y) * cv.carry; cv.z += (seat.z - cv.z) * cv.carry;
    cv.yaw += ((cs.yaw - 720) - cv.yaw) * cv.carry;
  }
  for (const [cr, c, Mb, arms] of [[S, cs, MbS, armsS], [V, cv, V.bodyMatrix(cv), null]]) {
    cr.c = c; cr.Mb = Mb;
    cr.shell.matrix.copy(Mb); cr.shell.matrixWorldNeedsUpdate = true;
    cr.under.matrix.copy(Mb).multiply(new THREE.Matrix4().makeTranslation(0, -0.07, 0).scale(V3(0.44, 0.13, 0.34))); cr.under.matrixWorldNeedsUpdate = true;
    for (const leg of cr.legs) {
      legPose(cr, c, Mb, leg, dt, t);
      const [r, k, m, a, f] = leg.pts;
      place(leg.parts[0].m, r, k, leg.n); place(leg.parts[1].m, k, m, leg.n); place(leg.parts[2].m, m, a, leg.n); place(leg.parts[3].m, a, f, leg.n, 0.0);
    }
    cr.armPts = (arms || cr.arms.map(a => cr.armChain(c, Mb, a.s)));
    cr.arms.forEach((arm, j) => {
      const p = cr.armPts[j], bodyUp = V3(0, 1, 0).applyMatrix3(new THREE.Matrix3().setFromMatrix4(Mb));
      const zh = (d) => { const z = d.clone().cross(bodyUp); if (z.length() < 1e-3) z.set(1, 0, 0); return z.normalize().multiplyScalar(arm.s); };
      place(arm.parts[0].m, p.root, p.e, zh(p.e.clone().sub(p.root)));
      place(arm.parts[1].m, p.e, p.w, zh(p.w.clone().sub(p.e)));
      place(arm.parts[2].m, p.w, p.tip, zh(p.d3), 0.0);
    });
  }
}
function simulate(t) {
  if (t < SIM.t) { SIM.t = -1e9; for (const cr of [V, S]) for (const l of cr.legs) { l.foot = null; l.step = null; } }
  if (SIM.t < -1e8) SIM.t = Math.min(t, -0.5);
  while (SIM.t + SIM.dt < t) { SIM.t += SIM.dt; poseCrabs(SIM.t, SIM.dt); }
  SIM.t = t; poseCrabs(t, SIM.dt);
}

// ---------------------------------------------------------------- clipping checks (capsules)
function segDist(p1, q1, p2, q2) {
  const d1 = q1.clone().sub(p1), d2 = q2.clone().sub(p2), r = p1.clone().sub(p2);
  const a = d1.dot(d1), e = d2.dot(d2), f = d2.dot(r);
  let s, tt;
  if (a < 1e-9 && e < 1e-9) return r.length();
  if (a < 1e-9) { s = 0; tt = Math.min(Math.max(f / e, 0), 1); }
  else {
    const c = d1.dot(r);
    if (e < 1e-9) { tt = 0; s = Math.min(Math.max(-c / a, 0), 1); }
    else {
      const b = d1.dot(d2), den = a * e - b * b;
      s = den !== 0 ? Math.min(Math.max((b * f - c * e) / den, 0), 1) : 0;
      tt = (b * s + f) / e;
      if (tt < 0) { tt = 0; s = Math.min(Math.max(-c / a, 0), 1); } else if (tt > 1) { tt = 1; s = Math.min(Math.max((b - c) / a, 0), 1); }
    }
  }
  return p1.clone().addScaledVector(d1, s).distanceTo(p2.clone().addScaledVector(d2, tt));
}
function capsules(cr) {
  const out = [], Mb = cr.Mb, P = (x, y, z) => V3(x, y, z).applyMatrix4(Mb);
  out.push({ n: 'shell', a: P(-0.3, 0.0, 0), b: P(0.3, 0.0, 0), r: 0.2, body: 1 });
  out.push({ n: 'shell', a: P(-0.22, 0.0, 0.17), b: P(0.22, 0.0, 0.17), r: 0.17, body: 1 });
  out.push({ n: 'shell', a: P(-0.22, 0.0, -0.17), b: P(0.22, 0.0, -0.17), r: 0.17, body: 1 });
  for (const l of cr.legs) {
    const [r0, k, m, a, f] = l.pts, nm = `leg${l.s > 0 ? 'R' : 'L'}${l.i}`;
    out.push({ n: nm + '.merus', a: r0.clone().lerp(k, 0.25), b: k, r: 0.05, limb: nm });
    out.push({ n: nm + '.carpus', a: k, b: m, r: 0.045, limb: nm, distal: 1 });
    out.push({ n: nm + '.propodus', a: m, b: a, r: 0.042, limb: nm, distal: 1 });
    out.push({ n: nm + '.dactyl', a: a, b: f.clone().lerp(a, 0.12), r: 0.03, limb: nm, distal: 1, tip: 1 });
  }
  cr.armPts.forEach((p, j) => {
    const nm = 'claw' + (j === 0 ? 'R' : 'L');
    out.push({ n: nm + '.merus', a: p.root.clone().lerp(p.e, 0.3), b: p.e, r: 0.065, limb: nm });
    out.push({ n: nm + '.carpus', a: p.e, b: p.w, r: 0.065, limb: nm, distal: 1 });
    const side = p.d3.clone().cross(UP); if (side.length() < 1e-3) side.set(1, 0, 0); side.normalize();
    for (const o of [-0.08, 0.08]) out.push({ n: nm + '.claw', a: p.w.clone().addScaledVector(side, o), b: p.tip.clone().addScaledVector(p.d3, -0.1).addScaledVector(side, o * 0.5), r: 0.1, limb: nm, distal: 1, claw: 1 });
  });
  return out;
}
function check() {
  const cv = capsules(V), cs = capsules(S), res = { inter: 9, interPair: '', floor: 9, floorPart: '', self: 9, selfPair: '', reach: 0, seat: null };
  const carry = V.c.carry;
  for (const a of cv) for (const b of cs) {
    const g = segDist(a.a, a.b, b.a, b.b) - a.r - b.r;
    if (carry > 0.5 && b.claw && a.body) { res.seat = Math.min(res.seat ?? 9, g); continue; }   // her shell resting on his claws
    if (g < res.inter) { res.inter = g; res.interPair = `${a.n}~${b.n}`; }
  }
  for (const [cr, cc] of [[V, cv], [S, cs]]) {
    for (const p of cc) {
      if (p.tip) continue;
      const lo = Math.min(p.a.y, p.b.y) - p.r;
      if (lo < res.floor) { res.floor = lo; res.floorPart = cr.name + ':' + p.n; }
    }
    for (let i = 0; i < cc.length; i++) for (let j = i + 1; j < cc.length; j++) {
      const a = cc[i], b = cc[j];
      if (!a.limb || !b.limb || a.limb === b.limb || !(a.distal && b.distal)) continue;
      const g = segDist(a.a, a.b, b.a, b.b) - (a.r + b.r) * 0.8;
      if (g < res.self) { res.self = g; res.selfPair = `${cr.name}:${a.n}~${b.n}`; }
    }
    const rf = cr.legs.filter(l => !l.reach && cr.c.air < 0.5 && !(l.i < 2 && cr.c.raiseF > 0.5));
    res.reach += rf.length; if (rf.length) res.reachLegs = (res.reachLegs || '') + rf.map(l => cr.name + (l.s > 0 ? 'R' : 'L') + l.i + (l.step ? '*' : '')).join(' ') + ' ';
  }
  return res;
}

// ---------------------------------------------------------------- cameras (cut on the bar lines)
const tb = b => B0 + b * BEAT;
const SHOTS = [
  { to: tb(16), a: [[0, 3.1, 6.2], [0, 0.3, 0]], b: [[0, 2.8, 5.5], [0, 0.3, 0]] },
  { to: tb(24), a: [[-1.4, 2.6, 4.9], [-1.0, 0.35, 0]], b: [[-1.1, 2.4, 4.4], [-0.9, 0.35, 0]] },
  { to: tb(32.5), a: [[0, 5.2, 9.2], [0, 0.3, 0.4]], b: [[0.8, 4.8, 8.6], [0, 0.3, 0.4]] },
  { to: tb(48), a: [[1.4, 2.4, 5.8], [0, 0.8, 0.3]], b: [[-0.6, 2.5, 5.6], [0, 0.8, 0.3]] },
  { to: 1e9, a: [[0, 3.0, 6.8], [0, 0.55, 0.5]], b: [[0, 2.7, 5.9], [0, 0.6, 0.5]] },
];
function cameraAt(t) {
  let t0 = -0.5;
  for (const s of SHOTS) {
    if (t < s.to) {
      const f = Math.min(1, Math.max(0, (t - t0) / (Math.min(s.to, 25) - t0)));
      const p = V3(...s.a[0]).lerp(V3(...s.b[0]), f), l = V3(...s.a[1]).lerp(V3(...s.b[1]), f);
      camera.position.copy(p); camera.lookAt(l); return;
    }
    t0 = s.to;
  }
}

window.renderAt = (t, cam, draw = true) => {
  simulate(t);
  if (!draw) return check();
  if (cam) { camera.position.set(...cam[0]); camera.lookAt(V3(...cam[1])); } else cameraAt(t);
  renderer.render(scene, camera);
  return check();
};
window.frame = (q = 0.92) => renderer.domElement.toDataURL('image/jpeg', q);
window.DBG = () => ({ V: [V.c.x, V.c.y, V.c.z, V.c.carry].map(x => +x.toFixed(3)), S: S.armPts.map(p => [p.root, p.e, p.w, p.tip].map(v => v.toArray().map(x => +x.toFixed(2)))), legs: S.legs.map(l => [l.reach, l.i, l.s]).concat(S.legs.slice(0, 1).map(l => l.pts.map(v => v.toArray().map(x => +x.toFixed(2))))) });
window.READY = true;
