// Strictly Crabs Dancing: the ballroom's back of stage, built in 3D from Sam's four reference photos (21 Oct).
// Concentric arches of sunburst LED panels edged in lilac neon, the glitterball logo in the middle, the band's
// balcony with a curving staircase down each side, lit steps along the front, free-standing neon arcs at the
// sides, moving-head light beams from the rig and twinkling star lights. Everything is drawn here, no photos
// except the logo (cut from the finished title frame: tex/logo.png).
import * as THREE from 'three';

const TAU = Math.PI * 2;
const rnd = (() => { let s = 7; return () => ((s = (s * 16807) % 2147483647) / 2147483647); })();

function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

// LED wall: rays of coloured dashes radiating from the arch's centre, cut into panels, with a fine pixel grid
const PAL = ['#ff3fa8', '#ff7a2e', '#36dcff', '#a35cff', '#ff5ad0', '#ffd25a'];
const sunburst = canvasTex(1024, 1024, (g, w, h) => {
  g.fillStyle = '#16052a'; g.fillRect(0, 0, w, h);
  const cx = w / 2, cy = h / 2;
  for (let k = 0; k < 150; k++) {
    const a = k / 150 * TAU + rnd() * 0.01;
    g.strokeStyle = PAL[Math.floor(rnd() * PAL.length)];
    g.lineWidth = 2 + rnd() * 4;
    let r = 20 + rnd() * 60;
    while (r < 720) {
      const len = 30 + rnd() * 110;
      g.globalAlpha = 0.55 + rnd() * 0.45;
      g.beginPath(); g.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r);
      g.lineTo(cx + Math.cos(a) * (r + len), cy + Math.sin(a) * (r + len)); g.stroke();
      r += len + 10 + rnd() * 50;
    }
  }
  g.globalAlpha = 1;
  // panel seams: dark spokes every 7.5 degrees and dark rings
  g.strokeStyle = 'rgba(10,2,20,0.85)'; g.lineWidth = 3;
  for (let k = 0; k < 48; k++) {
    const a = k / 48 * TAU;
    g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.cos(a) * 800, cy + Math.sin(a) * 800); g.stroke();
  }
  // LED pixel grid
  g.fillStyle = 'rgba(8,0,16,0.35)';
  for (let x = 0; x < w; x += 6) g.fillRect(x, 0, 1, h);
  for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 1);
});

// lit step faces: a hot-pink strip with a brighter line along the top edge
const riserTex = canvasTex(256, 32, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h);
  gr.addColorStop(0, '#ffb3e6'); gr.addColorStop(0.18, '#ff3fb4'); gr.addColorStop(1, '#7a1070');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(40,0,40,0.5)';
  for (let x = 0; x < w; x += 16) g.fillRect(x, 0, 2, h);
});
riserTex.wrapS = THREE.RepeatWrapping;

// light beam: bright at the lamp, fading down its length and towards its edges
const beamTex = canvasTex(64, 256, (g, w, h) => {
  const img = g.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const v = y / (h - 1), u = Math.abs(x / (w - 1) - 0.5) * 2;      // v: 0 at the far end, 1 at the lamp
    const a = Math.pow(v, 1.6) * (1 - u * u) * 255;
    const i = (y * w + x) * 4; img.data[i] = img.data[i + 1] = img.data[i + 2] = 255; img.data[i + 3] = a;
  }
  g.putImageData(img, 0, 0);
}, false);

// star sparkle: glow plus a four-point cross
const starTex = canvasTex(64, 64, (g, w, h) => {
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.15, 'rgba(200,255,240,0.8)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.strokeStyle = 'rgba(230,255,250,0.9)'; g.lineWidth = 1.5;
  g.beginPath(); g.moveTo(32, 2); g.lineTo(32, 62); g.moveTo(2, 32); g.lineTo(62, 32); g.stroke();
});

const glow = (color) => new THREE.MeshBasicMaterial({ color, toneMapped: false, fog: false });
const NEON = 0xd7b4ff;

export async function buildStage(scene, loader) {
  const G = new THREE.Group();
  const anim = [];
  const add = (m, x = 0, y = 0, z = 0) => { m.position.set(x, y, z); G.add(m); return m; };
  const BASE = 0.54;        // top of the front steps: the stage the arches stand on
  const AZ = -5;            // the arches' centre line (local z)
  const metal = new THREE.MeshStandardMaterial({ color: 0xc8c8d8, metalness: 0.9, roughness: 0.25 });
  const dark = new THREE.MeshBasicMaterial({ color: 0x0a0412, fog: false });

  // front steps: three lit risers across the width, dark treads
  for (let k = 0; k < 3; k++) {
    const y0 = k * 0.18, z0 = -k * 0.45;
    const tread = add(new THREE.Mesh(new THREE.BoxGeometry(60, 0.18, 9), dark), 0, y0 + 0.09, z0 - 4.5);
    tread.receiveShadow = true;
    const t = riserTex.clone(); t.needsUpdate = true; t.repeat.set(30, 1);
    add(new THREE.Mesh(new THREE.PlaneGeometry(40 - k * 0.6, 0.16), new THREE.MeshBasicMaterial({ map: t, toneMapped: false, fog: false })), 0, y0 + 0.09, z0 + 0.002);
  }

  // a dark back wall closing off the set, dotted with faint house lights
  const wallTex = canvasTex(1024, 256, (g, w, h) => {
    g.fillStyle = '#0a0412'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(${150 + rnd() * 100},${120 + rnd() * 80},255,${0.15 + rnd() * 0.35})`; g.fillRect(rnd() * w, rnd() * h, 2, 2); }
  });
  add(new THREE.Mesh(new THREE.PlaneGeometry(70, 18), new THREE.MeshBasicMaterial({ map: wallTex, toneMapped: false, fog: false })), 0, 9, AZ - 3.5);

  // the arches: four LED bands, each a little further forward, edged with neon tubes
  const bands = [[2.8, 3.6], [3.85, 4.65], [4.9, 5.7], [5.95, 6.75]];
  const core = new THREE.Mesh(new THREE.CircleGeometry(bands[0][0], 96, 0, Math.PI),
    new THREE.MeshBasicMaterial({ map: sunburst, toneMapped: false, fog: false, color: 0xd8c8ff }));
  add(core, 0, BASE, AZ - 0.35);
  bands.forEach(([r0, r1], k) => {
    const z = AZ + k * 0.3;
    add(new THREE.Mesh(new THREE.RingGeometry(r0, r1, 128, 1, 0, Math.PI),
      new THREE.MeshBasicMaterial({ map: sunburst, toneMapped: false, fog: false })), 0, BASE, z);
    for (const r of [r0, r1]) add(new THREE.Mesh(new THREE.TorusGeometry(r, 0.055, 8, 160, Math.PI), glow(NEON)), 0, BASE, z + 0.03);
    // dark gap behind, so the bands read as separate arches
    add(new THREE.Mesh(new THREE.RingGeometry(r1, r1 + 0.25, 96, 1, 0, Math.PI), glow(0x070210)), 0, BASE, z - 0.05);
  });

  // free-standing neon arcs either side, broken at the top like the real set
  for (const [k, r] of [7.3, 7.85, 8.4].entries()) {
    for (const side of [-1, 1]) {
      const arc = new THREE.Mesh(new THREE.TorusGeometry(r, 0.06, 8, 64, 0.95), glow(NEON));
      arc.rotation.z = side > 0 ? 0.2 : Math.PI - 0.2 - 0.95;
      add(arc, 0, BASE, AZ + 1.4 + k * 0.25);
    }
  }

  // the logo, high in the middle of the arches
  const logoTex = await loader.loadAsync('tex/logo.png'); logoTex.colorSpace = THREE.SRGBColorSpace;
  add(new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.06), new THREE.MeshBasicMaterial({ map: logoTex, transparent: true, toneMapped: false, fog: false })),
    0, BASE + 1.95, AZ - 0.2);

  // band balcony across the bottom of the logo: deck, glowing fascia, rails, a row of lamps
  const BY = BASE + 1.0, BZ = AZ + 0.55, BW = 2.5;
  add(new THREE.Mesh(new THREE.BoxGeometry(BW * 2, 0.1, 0.8), metal), 0, BY, BZ);
  add(new THREE.Mesh(new THREE.BoxGeometry(BW * 2, 0.07, 0.02), glow(0xf0d8ff)), 0, BY - 0.02, BZ + 0.41);
  add(new THREE.Mesh(new THREE.BoxGeometry(BW * 2, 0.025, 0.025), metal), 0, BY + 0.42, BZ + 0.38);
  for (let k = 0; k <= 12; k++) add(new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.42, 0.02), metal), -BW + k * BW / 6, BY + 0.21, BZ + 0.38);
  for (let k = 0; k < 7; k++) add(new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), glow(0xffffff)), -2.1 + k * 0.7, BY + 0.12, BZ + 0.3);
  // the band underneath: music stands with little lit tops
  for (let k = 0; k < 8; k++) {
    const x = -2.1 + k * 0.6;
    add(new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.3, 0.04), metal), x, BASE + 0.45, BZ - 0.1);
    add(new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.03, 0.05), glow(0xffe8c0)), x, BASE + 0.61, BZ - 0.1);
    add(new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.3), metal), x, BASE + 0.15, BZ - 0.1);
  }

  // curving staircases from each end of the balcony down to the stage, lit pink risers, silver rails
  for (const side of [-1, 1]) {
    const N = 9, rail = [[], []];
    for (let k = 0; k <= N; k++) {
      const f = k / N, a = f * 1.25;                        // sweep outwards and forwards
      const cx = side * (BW + 0.2 + Math.sin(a) * 1.5), cz = BZ - 0.1 + (1 - Math.cos(a)) * 1.6 + f * 0.4;
      const y = BY - f * (BY - BASE);
      const yaw = -side * a;
      const step = new THREE.Group(); step.position.set(cx, y - 0.05, cz); step.rotation.y = yaw; G.add(step);
      const tr = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.06, 0.32), metal); step.add(tr);
      const t = riserTex.clone(); t.needsUpdate = true; t.repeat.set(2, 1);
      const rs = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.1), new THREE.MeshBasicMaterial({ map: t, toneMapped: false, fog: false }));
      rs.position.set(0, -0.07, 0.165); step.add(rs);
      for (const [i, o] of [[0, -0.45], [1, 0.45]].map(([i, o]) => [i, o])) {
        const v = new THREE.Vector3(o, 0.45, 0).applyEuler(new THREE.Euler(0, yaw, 0)).add(step.position);
        rail[i].push(v);
      }
    }
    for (const pts of rail) add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, 0.025, 6), metal));
  }

  // moving-head beams from the lighting rig, swaying slowly
  const beamMat = new THREE.MeshBasicMaterial({ map: beamTex, color: 0xe8eaff, transparent: true, opacity: 0.32, blending: THREE.AdditiveBlending,
    depthWrite: false, side: THREE.DoubleSide, toneMapped: false, fog: false });
  for (let k = 0; k < 10; k++) {
    const x = -9 + k * 2, len = 11;
    const pivot = new THREE.Group(); pivot.position.set(x, BASE + 9.5, AZ + 2 + (k % 2) * 1.5); G.add(pivot);
    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.75, len, 24, 1, true), beamMat);
    cone.position.y = -len / 2; pivot.add(cone);                    // tip at the lamp, opening downwards
    add(new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 8), glow(0xffffff)), x, BASE + 9.5, pivot.position.z);
    const ph = k * 1.7, lean = -x * 0.045;
    anim.push(t => { pivot.rotation.z = lean + 0.22 * Math.sin(t * 0.55 + ph); pivot.rotation.x = 0.35 + 0.12 * Math.sin(t * 0.41 + ph * 1.3); });
  }

  // star lights: along the dark gaps between the arches and scattered through the rig above
  const pos = [];
  bands.forEach(([, r1], k) => { for (let i = 0; i < 9 + k * 2; i++) { const a = (i + 0.5) / (9 + k * 2) * Math.PI; pos.push(Math.cos(a) * (r1 + 0.13), BASE + Math.sin(a) * (r1 + 0.13), AZ + k * 0.3); } });
  for (let i = 0; i < 70; i++) pos.push((rnd() - 0.5) * 22, BASE + 7 + rnd() * 4, AZ - 1 + rnd() * 3);
  const sets = [0, 1].map(j => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos.filter((_, i) => Math.floor(i / 3) % 2 === j), 3));
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({ map: starTex, color: 0xbfffee, size: 0.42, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending, toneMapped: false, fog: false }));
    G.add(pts); return pts;
  });
  anim.push(t => sets.forEach((p, j) => { p.material.opacity = 0.65 + 0.35 * Math.sin(t * 3.1 + j * Math.PI); }));

  scene.add(G);
  return { group: G, update: t => anim.forEach(f => f(t)) };
}
