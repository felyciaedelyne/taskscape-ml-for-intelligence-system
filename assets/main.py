<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chase Maze — Pacman Edition</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;min-height:100vh;font-family:'Press Start 2P',monospace;color:#fff;padding:12px}
#topbar{display:flex;justify-content:space-between;width:100%;max-width:560px;padding:4px 0;font-size:10px}
#topbar .sc{color:#ffb852}
#topbar .hi{color:#0ff}
#topbar .mt{color:#f80}
#screen-over{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:24px;background:#000;width:100%;max-width:560px;text-align:center;border:2px solid #1a1aee;margin-top:8px}
#screen-over h1{font-size:18px;color:#ffe000;letter-spacing:2px}
#screen-over .sub{font-size:8px;color:#aaa;line-height:2.4}
#screen-over .hs{font-size:8px;color:#0ff;line-height:2.2;margin-top:4px}
.gbtn{background:#1a1aee;border:2px solid #4af;color:#fff;font-family:'Press Start 2P',monospace;font-size:10px;padding:12px 28px;cursor:pointer;letter-spacing:1px;margin-top:4px}
.gbtn:hover{background:#3355ff}
#game-area{display:none;width:100%;max-width:560px;margin-top:4px}
canvas{display:block;width:100%;border:2px solid #1a1aee}
#bottombar{display:flex;justify-content:space-between;align-items:center;width:100%;max-width:560px;padding:6px 0;font-size:8px;color:#555;margin-top:2px}
#d-pad{display:grid;grid-template-columns:repeat(3,48px);grid-template-rows:repeat(2,48px);gap:6px;margin:10px auto;justify-content:center}
#d-pad button{background:#111;border:1px solid #333;color:#fff;font-size:18px;cursor:pointer;border-radius:4px;touch-action:manipulation}
#d-pad button:active{background:#333}
.dp-blank{background:transparent!important;border:none!important;pointer-events:none}
#ghost-legend{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;font-size:7px;color:#555;margin-top:6px}
.gl-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;vertical-align:middle}
</style>
</head>
<body>

<div id="topbar">
  <span>SCORE: <span id="sc" class="sc">0</span></span>
  <span id="mt" class="mt">MAZE: 2:00</span>
  <span>HI: <span id="hi" class="hi">0</span></span>
</div>

<div id="screen-over">
  <h1 id="ov-title">CHASE MAZE</h1>
  <div class="sub" id="ov-sub">
    4 Ghosts · RL AI · Dynamic Maze<br>
    Makan semua dot untuk naik level<br>
    Arrow Keys / WASD untuk bergerak<br>
    Hindari semua ghost!
  </div>
  <div class="hs" id="ov-hs"></div>
  <button class="gbtn" id="gbtn">START GAME</button>
</div>

<div id="game-area">
  <canvas id="c"></canvas>
</div>

<div id="bottombar">
  <div id="lives-row"></div>
  <span id="info-txt">BLINKY · PINKY · INKY · CLYDE</span>
</div>

<div id="d-pad">
  <button class="dp-blank"></button>
  <button id="du">↑</button>
  <button class="dp-blank"></button>
  <button id="dl">←</button>
  <button id="dd">↓</button>
  <button id="dr">→</button>
</div>

<div id="ghost-legend">
  <span><span class="gl-dot" style="background:#ff2020"></span>Blinky — BFS Hunter</span>
  <span><span class="gl-dot" style="background:#ffb8ff"></span>Pinky — Random Walk</span>
  <span><span class="gl-dot" style="background:#00ffff"></span>Inky — RL Agent</span>
  <span><span class="gl-dot" style="background:#ffb852"></span>Clyde — Heat Seeker</span>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const DIRS = [[0,-1],[0,1],[-1,0],[1,0]];
const GCOL = ['#ff2020','#ffb8ff','#00ffff','#ffb852'];

let G = null, animId = null, lastTs = 0;

// ─── HIGH SCORES ───
let HS = [];
try { HS = JSON.parse(localStorage.getItem('chaseMazeHS') || '[]'); } catch(e) {}

function saveHS(score, level) {
  HS.push({ s: score, lv: level, d: new Date().toLocaleDateString('id') });
  HS.sort((a, b) => b.s - a.s);
  HS = HS.slice(0, 5);
  try { localStorage.setItem('chaseMazeHS', JSON.stringify(HS)); } catch(e) {}
  renderHS();
}

function renderHS() {
  const el = document.getElementById('ov-hs');
  document.getElementById('hi').textContent = HS[0]?.s || 0;
  if (!HS.length) { el.textContent = ''; return; }
  el.innerHTML = 'TOP SCORES:<br>' + HS.map((h, i) =>
    `${i+1}. ${h.s} pts &nbsp;·&nbsp; LV${h.lv} &nbsp;·&nbsp; ${h.d}`
  ).join('<br>');
}
renderHS();

// ─── MAZE GENERATOR (Recursive Backtracking) ───
function mulberry32(a) {
  return () => {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function buildMaze(cols, rows, seed) {
  const maze = Array.from({ length: rows }, () => Array(cols).fill(1));
  const rng = mulberry32(seed);

  function carve(x, y) {
    maze[y][x] = 0;
    const dirs = [[0,-2],[0,2],[-2,0],[2,0]].sort(() => rng() - 0.5);
    for (const [dx, dy] of dirs) {
      const nx = x + dx, ny = y + dy;
      if (nx > 0 && nx < cols-1 && ny > 0 && ny < rows-1 && maze[ny][nx] === 1) {
        maze[y + dy/2][x + dx/2] = 0;
        carve(nx, ny);
      }
    }
  }
  carve(1, 1);

  // Extra passages — Pac-Man feel
  for (let i = 0; i < Math.floor(cols * rows * 0.06); i++) {
    const x = 1 + Math.floor(rng() * (cols - 2));
    const y = 1 + Math.floor(rng() * (rows - 2));
    if (maze[y][x] === 1) {
      let f = 0;
      DIRS.forEach(([dx, dy]) => { if (maze[y+dy]?.[x+dx] === 0) f++; });
      if (f >= 2) maze[y][x] = 0;
    }
  }

  maze[1][1] = 0;
  maze[rows-2][cols-2] = 0;
  return maze;
}

function canMove(maze, x, y) {
  return x >= 0 && y >= 0 && y < maze.length && x < maze[0].length && maze[y][x] === 0;
}

function bfsNext(maze, fx, fy, tx, ty) {
  if (fx === tx && fy === ty) return [fx, fy];
  const vis = new Set([`${fx},${fy}`]);
  const q = [[fx, fy, []]];
  while (q.length) {
    const [cx, cy, path] = q.shift();
    for (const [dx, dy] of DIRS) {
      const nx = cx + dx, ny = cy + dy, k = `${nx},${ny}`;
      if (canMove(maze, nx, ny) && !vis.has(k)) {
        vis.add(k);
        const np = [...path, [nx, ny]];
        if (nx === tx && ny === ty) return np[0] || [nx, ny];
        q.push([nx, ny, np]);
      }
    }
  }
  return [fx, fy];
}

// ─── Q-LEARNING AGENT ───
class QLearner {
  constructor() { this.q = {}; this.epsilon = 0.5; this.episodes = 0; }

  key(hx, hy, px, py) { return `${hx},${hy},${px},${py}`; }

  getQ(s) {
    if (!this.q[s]) this.q[s] = [0, 0, 0, 0];
    return this.q[s];
  }

  choose(hx, hy, px, py, validIdx) {
    const s = this.key(hx, hy, px, py);
    if (Math.random() < this.epsilon || !validIdx.length)
      return validIdx[Math.floor(Math.random() * validIdx.length)] ?? null;
    const q = this.getQ(s);
    return validIdx.reduce((b, i) => q[i] > q[b] ? i : b, validIdx[0]);
  }

  update(s, a, reward, hx, hy, px, py) {
    if (a == null) return;
    const ns = this.key(hx, hy, px, py);
    const q = this.getQ(s), nq = this.getQ(ns);
    q[a] += 0.3 * (reward + 0.9 * Math.max(...nq) - q[a]);
  }

  decay() { this.episodes++; this.epsilon = Math.max(0.05, 0.5 - this.episodes * 0.01); }
}

// ─── GHOST CLASS ───
class Ghost {
  constructor(x, y, id, ql) {
    this.x = x; this.y = y; this.id = id; this.ql = ql;
    this.trail = []; this._ps = null; this._pa = null;
  }

  move(maze, px, py, heat) {
    this.trail.push([this.x, this.y]);
    if (this.trail.length > 5) this.trail.shift();

    const valid = DIRS.map((d, i) => [i, ...d])
      .filter(([, dx, dy]) => canMove(maze, this.x + dx, this.y + dy));
    if (!valid.length) return;

    let nx = this.x, ny = this.y;

    if (this.id === 0) {
      // Blinky: BFS shortest path
      [nx, ny] = bfsNext(maze, this.x, this.y, px, py);

    } else if (this.id === 1) {
      // Pinky: random walk
      const c = valid[Math.floor(Math.random() * valid.length)];
      nx = this.x + c[1]; ny = this.y + c[2];

    } else if (this.id === 2) {
      // Inky: Q-Learning RL agent
      const vi = valid.map(v => v[0]);
      const ai = this.ql.choose(this.x, this.y, px, py, vi);
      if (ai != null) {
        const v = valid.find(v => v[0] === ai) || valid[0];
        const pd = Math.abs(this.x - px) + Math.abs(this.y - py);
        if (this._ps != null) {
          const nd = Math.abs(this.x + v[1] - px) + Math.abs(this.y + v[2] - py);
          this.ql.update(this._ps, this._pa, nd < pd ? 0.5 : -0.1,
            this.x + v[1], this.y + v[2], px, py);
        }
        this._ps = this.ql.key(this.x, this.y, px, py);
        this._pa = ai;
        nx = this.x + v[1]; ny = this.y + v[2];
      }

    } else {
      // Clyde: heat-map seeker
      const best = valid.reduce((b, v) => {
        const sc = -(Math.abs(this.x + v[1] - px) + Math.abs(this.y + v[2] - py))
          + (heat[this.y + v[2]]?.[this.x + v[1]] || 0) * 0.4;
        return sc > b[0] ? [sc, v] : b;
      }, [-Infinity, null]);
      if (best[1]) { nx = this.x + best[1][1]; ny = this.y + best[1][2]; }
    }

    this.x = nx; this.y = ny;
  }
}

// ─── GAME INIT ───
function startGame() {
  document.getElementById('screen-over').style.display = 'none';
  document.getElementById('game-area').style.display = 'block';
  G = {
    level: 1, score: 0, lives: 3,
    ql: new QLearner(),
    frame: 0, aframe: 0,
    scAnims: [], qdir: null,
    mazeCD: 120, timeLeft: 100,
    lastTick: Date.now(),
    mazeFlash: 0, state: 'playing'
  };
  initLevel();
  if (animId) cancelAnimationFrame(animId);
  lastTs = 0;
  animId = requestAnimationFrame(loop);
}

function initLevel() {
  // Maze grows each level: starts 13×13, max 25×25
  const base = 13, maxC = 25;
  let cols = Math.min(base + (G.level - 1), maxC);
  if (cols % 2 === 0) cols++;
  const rows = cols;
  G.cols = cols; G.rows = rows;

  const maxPx = Math.min(560, window.innerWidth - 24);
  G.cell = Math.floor(maxPx / cols);
  canvas.width  = cols * G.cell;
  canvas.height = rows * G.cell;

  const seed = G.level * 997 + Math.floor(Date.now() / 1000) % 997;
  G.maze = buildMaze(cols, rows, seed);
  G.heat = Array.from({ length: rows }, () => Array(cols).fill(0));
  G.mazeCD   = 120;
  G.timeLeft = 80 + G.level * 10;
  G.lastTick = Date.now();

  // Place dots on all floor cells except spawn corners
  G.dots = new Set();
  const avoid = new Set(['1,1', `${cols-2},${rows-2}`]);
  for (let y = 0; y < rows; y++)
    for (let x = 0; x < cols; x++)
      if (G.maze[y][x] === 0 && !avoid.has(`${x},${y}`))
        G.dots.add(`${x},${y}`);
  G.totalDots = G.dots.size;

  G.player = { x: 1, y: 1, dir: [1, 0] };

  const numGhosts = Math.min(1 + Math.floor((G.level - 1) / 2), 4);
  const spawns = [
    [cols-2, 1],
    [cols-2, rows-2],
    [1, rows-2],
    [cols-2, Math.floor(rows/2)]
  ];
  G.ghosts = spawns.slice(0, numGhosts).map(([x, y], i) =>
    new Ghost(x, y, i, G.ql)
  );

  // Ghost speed increases with level
  G.aiInterval = Math.max(4, 12 - G.level);

  renderLives();
  renderHUD();
}

// ─── INPUT ───
const KMAP = {
  'ArrowUp':    [0,-1], 'w': [0,-1], 'W': [0,-1],
  'ArrowDown':  [0, 1], 's': [0, 1], 'S': [0, 1],
  'ArrowLeft':  [-1,0], 'a': [-1,0], 'A': [-1,0],
  'ArrowRight': [1, 0], 'd': [1, 0], 'D': [1, 0],
};

document.addEventListener('keydown', e => {
  if (G && G.state === 'playing' && KMAP[e.key]) {
    G.qdir = KMAP[e.key];
    e.preventDefault();
  }
  if ([' ', 'ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))
    e.preventDefault();
});

// D-pad buttons
const DPAD_DIRS = [[0,-1],[0,1],[-1,0],[1,0]];
['du','dd','dl','dr'].forEach((id, i) => {
  const btn = document.getElementById(id);
  btn.addEventListener('pointerdown', e => {
    if (G && G.state === 'playing') G.qdir = DPAD_DIRS[i];
    e.preventDefault();
  });
});

document.getElementById('gbtn').addEventListener('click', () => startGame());

// Touch swipe
let ts0 = null;
document.addEventListener('touchstart', e => {
  ts0 = { x: e.touches[0].clientX, y: e.touches[0].clientY };
}, { passive: true });
document.addEventListener('touchend', e => {
  if (!ts0 || !G || G.state !== 'playing') return;
  const dx = e.changedTouches[0].clientX - ts0.x;
  const dy = e.changedTouches[0].clientY - ts0.y;
  if (Math.abs(dx) > Math.abs(dy)) G.qdir = dx > 0 ? [1,0] : [-1,0];
  else G.qdir = dy > 0 ? [0,1] : [0,-1];
  ts0 = null;
}, { passive: true });

// ─── GAME UPDATE ───
function update() {
  if (!G || G.state !== 'playing') return;
  G.frame++; G.aframe++;

  // Move player
  if (G.qdir) {
    const [dx, dy] = G.qdir; G.qdir = null;
    const nx = G.player.x + dx, ny = G.player.y + dy;
    if (canMove(G.maze, nx, ny)) {
      G.player.x = nx; G.player.y = ny;
      G.player.dir = [dx, dy];
      G.heat[ny][nx] = Math.min((G.heat[ny][nx] || 0) + 1, 20);
      const k = `${nx},${ny}`;
      if (G.dots.has(k)) {
        G.dots.delete(k);
        G.score += 10;
        G.scAnims.push({ x: nx, y: ny, t: '+10', age: 0 });
      }
    }
  }

  // Win condition: all dots eaten
  if (G.dots.size === 0) { levelUp(); return; }

  // Move ghosts
  if (G.frame % G.aiInterval === 0) {
    for (const gh of G.ghosts) {
      gh.move(G.maze, G.player.x, G.player.y, G.heat);
      if (gh.x === G.player.x && gh.y === G.player.y) { die(); return; }
    }
  }

  // Timers
  const now = Date.now();
  if (now - G.lastTick >= 1000) {
    G.lastTick = now;
    G.timeLeft--;
    G.mazeCD--;
    if (G.timeLeft <= 0) { die(); return; }
    if (G.mazeCD <= 0) { reshuffleMaze(); G.mazeCD = 120; }
    renderHUD();
  }

  G.scAnims = G.scAnims.filter(a => { a.age++; return a.age < 40; });
}

function reshuffleMaze() {
  const rng = mulberry32(Date.now() % 9999999);
  let changed = 0;
  let tries = 0;
  while (changed < 6 && tries < 500) {
    tries++;
    const x = 1 + Math.floor(rng() * (G.cols - 2));
    const y = 1 + Math.floor(rng() * (G.rows - 2));
    if (G.maze[y][x] === 1) {
      let f = 0;
      DIRS.forEach(([dx, dy]) => { if (G.maze[y+dy]?.[x+dx] === 0) f++; });
      if (f >= 2) {
        G.maze[y][x] = 0;
        const k = `${x},${y}`;
        if (!G.dots.has(k)) { G.dots.add(k); G.totalDots++; }
        changed++;
      }
    }
  }
  G.mazeFlash = 12;
}

function levelUp() {
  G.ql.decay();
  G.score += G.timeLeft * 5 + 150;
  G.level++;
  document.getElementById('sc').textContent = G.score;
  showOver(
    `LEVEL CLEAR!`,
    `Masuk ke Level ${G.level}<br>Skor: ${G.score}`,
    'LANJUT',
    () => { document.getElementById('screen-over').style.display = 'none';
            document.getElementById('game-area').style.display = 'block';
            G.state = 'playing'; initLevel(); }
  );
}

function die() {
  G.lives--;
  if (G.lives <= 0) {
    saveHS(G.score, G.level);
    G.ql.decay();
    showOver('GAME OVER', `Skor: ${G.score}<br>Level: ${G.level}`, 'MAIN LAGI', () => startGame());
  } else {
    G.player = { x: 1, y: 1, dir: [1, 0] };
    G.ghosts.forEach(gh => { gh.x = G.cols - 2; gh.y = 1; });
    renderLives();
  }
}

function showOver(title, sub, btnTxt, cb) {
  G.state = 'over';
  document.getElementById('game-area').style.display = 'none';
  document.getElementById('screen-over').style.display = 'flex';
  document.getElementById('ov-title').textContent = title;
  document.getElementById('ov-sub').innerHTML = sub;
  renderHS();
  const b = document.getElementById('gbtn');
  b.textContent = btnTxt;
  b.onclick = cb;
}

function renderHUD() {
  document.getElementById('sc').textContent = G.score;
  document.getElementById('hi').textContent = HS[0]?.s || 0;
  const m = Math.floor(G.mazeCD / 60), s = G.mazeCD % 60;
  document.getElementById('mt').textContent = `MAZE: ${m}:${String(s).padStart(2,'0')}`;
  document.getElementById('info-txt').textContent =
    `LV${G.level}  ·  ${G.dots.size}/${G.totalDots} DOT  ·  ❤ ${G.lives}`;
}

function renderLives() {
  const el = document.getElementById('lives-row');
  el.innerHTML = '';
  for (let i = 0; i < (G?.lives || 0); i++) {
    const c = document.createElement('canvas');
    c.width = 16; c.height = 16;
    const cx2 = c.getContext('2d');
    cx2.fillStyle = '#ffe000';
    cx2.beginPath();
    cx2.moveTo(8, 8);
    cx2.arc(8, 8, 7, 0.4, Math.PI * 2 - 0.4);
    cx2.closePath();
    cx2.fill();
    el.appendChild(c);
  }
}

// ─── DRAW ───
function rr(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x+r, y); ctx.lineTo(x+w-r, y);
  ctx.quadraticCurveTo(x+w, y, x+w, y+r);
  ctx.lineTo(x+w, y+h-r); ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
  ctx.lineTo(x+r, y+h); ctx.quadraticCurveTo(x, y+h, x, y+h-r);
  ctx.lineTo(x, y+r); ctx.quadraticCurveTo(x, y, x+r, y);
  ctx.closePath();
}

function draw() {
  if (!G || G.state === 'over') return;
  const { cell, cols, rows, maze, heat, dots, player, ghosts, aframe, scAnims, timeLeft, mazeCD } = G;

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Maze reshuffle flash
  if (G.mazeFlash > 0) {
    ctx.fillStyle = `rgba(80,80,255,${G.mazeFlash / 12 * 0.22})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    G.mazeFlash--;
  }

  // Walls & floor heat
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const rx = x * cell, ry = y * cell;
      if (maze[y][x] === 1) {
        ctx.fillStyle = '#1a1aee';
        rr(rx+1, ry+1, cell-2, cell-2, 3); ctx.fill();
        ctx.strokeStyle = '#4444ff'; ctx.lineWidth = 1;
        rr(rx+1, ry+1, cell-2, cell-2, 3); ctx.stroke();
      } else {
        const h = heat[y][x];
        if (h > 0) {
          ctx.fillStyle = `rgba(255,80,0,${Math.min(h/20, 0.28)})`;
          ctx.fillRect(rx, ry, cell, cell);
        }
      }
    }
  }

  // Dots
  dots.forEach(k => {
    const [x, y] = k.split(',').map(Number);
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(x*cell + cell/2, y*cell + cell/2, Math.max(2, cell * 0.1), 0, Math.PI*2);
    ctx.fill();
  });

  // Exit tile
  const ex = (cols-2)*cell, ey = (rows-2)*cell;
  ctx.fillStyle = '#ffb852';
  rr(ex+1, ey+1, cell-2, cell-2, 3); ctx.fill();
  ctx.fillStyle = '#000';
  ctx.font = `bold ${Math.max(5, cell*0.25)}px 'Press Start 2P'`;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('EXIT', ex + cell/2, ey + cell/2);

  // Ghosts
  for (const gh of ghosts) {
    const col = GCOL[gh.id % 4];
    gh.trail.forEach(([tx, ty], i) => {
      ctx.globalAlpha = (i / gh.trail.length) * 0.18;
      ctx.fillStyle = col;
      ctx.fillRect(tx*cell, ty*cell, cell, cell);
    });
    ctx.globalAlpha = 1;

    const cx = gh.x*cell + cell/2, cy = gh.y*cell + cell/2, r = cell/2 - 1;
    ctx.fillStyle = col;
    ctx.beginPath();
    ctx.arc(cx, cy - r*0.1, r, Math.PI, 0);
    ctx.lineTo(cx + r, cy + r);
    const n = 3, w = r*2/n;
    for (let i = n; i >= 0; i--) {
      const bx = cx - r + i*w;
      ctx.lineTo(bx, cy + r - (i%2===0 ? r*0.4 : 0));
    }
    ctx.closePath(); ctx.fill();
    // Eyes
    [[-r*0.32], [r*0.32]].forEach(([ex2]) => {
      ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.arc(cx+ex2, cy-r*0.3, r*0.27, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = '#00c';
      ctx.beginPath(); ctx.arc(cx+ex2+1, cy-r*0.3, r*0.14, 0, Math.PI*2); ctx.fill();
    });
  }

  // Pac-Man player
  const { x: px, y: py, dir } = player;
  const cx = px*cell + cell/2, cy = py*cell + cell/2, r = cell/2 - 1;
  const tick = (aframe / 3) % 8;
  const mouthDeg = (tick < 4 ? tick : 8 - tick) * 7;
  let ang = 0;
  if (dir[0] === 1) ang = 0;
  else if (dir[0] === -1) ang = Math.PI;
  else if (dir[1] === 1) ang = Math.PI / 2;
  else ang = -Math.PI / 2;
  ctx.fillStyle = '#ffe000';
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.arc(cx, cy, r, ang + mouthDeg * Math.PI/180, ang - mouthDeg * Math.PI/180);
  ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#000';
  ctx.beginPath();
  ctx.arc(cx - Math.sin(ang)*r*0.4, cy - Math.cos(ang)*r*0.4, Math.max(1, r*0.12), 0, Math.PI*2);
  ctx.fill();

  // Score pop-ups
  scAnims.forEach(a => {
    ctx.globalAlpha = 1 - a.age / 40;
    ctx.fillStyle = '#ffff00';
    ctx.font = `${Math.max(6, cell*0.4)}px 'Press Start 2P'`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    ctx.fillText(a.t, a.x*cell + cell/2, a.y*cell - a.age * 0.4);
  });
  ctx.globalAlpha = 1;

  // Maze countdown warning
  if (mazeCD <= 10) {
    ctx.fillStyle = `rgba(255,136,0,${0.6 + Math.sin(G.frame * 0.3) * 0.3})`;
    ctx.font = `${Math.max(8, cell*0.5)}px 'Press Start 2P'`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    ctx.fillText(`MAZE BERUBAH: ${mazeCD}s`, canvas.width/2, 4);
  }

  // Time warning
  if (timeLeft <= 10) {
    ctx.fillStyle = `rgba(255,30,30,${0.5 + Math.sin(G.frame * 0.5) * 0.4})`;
    ctx.font = `${Math.max(8, cell*0.5)}px 'Press Start 2P'`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    ctx.fillText(`WAKTU: ${timeLeft}`, canvas.width/2, canvas.height - 4);
  }
}

// ─── MAIN LOOP ───
function loop(ts) {
  if (ts - lastTs >= 1000 / 60) {
    lastTs = ts;
    update();
    draw();
  }
  animId = requestAnimationFrame(loop);
}
</script>
</body>
</html>