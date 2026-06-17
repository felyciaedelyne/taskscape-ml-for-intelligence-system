import pygame
import numpy as np
import random
import sys
import time
import json
import os
from collections import deque
import math

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
FPS         = 60
PANEL_W     = 380
MAX_MAZE    = 31
HOLD_DELAY  = 150
HOLD_REPEAT = 80
TITLEBAR_H  = 36
MAX_LIVES   = 9

#ASSETS ICON
LOGO_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/taskscape_logo.png")
GREEN_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/circle_green.png")
BLUE_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/circle_blue.png")
YELLOW_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/circle_yellow.png")
ORANGE_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/circle_orange.png")
RED_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/circle_red.png")
UNLIMITED_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/assets/loop.png")
HEART_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/heart.png")
TURTLE_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/turtle.png")
FREEZE_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/snowflake.png")
SHIELD_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/shield.png")
MAGNET_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/magnet.png")
CHECK_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/check.png")
SKULL_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/skull.png")
ROCKET_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/rocket.png")
RESUME_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/play.png")
PAUSE_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/pause.png")
REPLAY_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/replay.png")
BILL_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/bill.png")
ATTENTION_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/warning.png")
TIMER_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/timer.png")
EXIT_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/exit.png")
GAME_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/game.png")
PENCIL_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/pencil.png")
CANCEL_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/close.png")
GHOST_RED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ghost_2.png")
GHOST_ORANGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ghost_4.png")
GHOST_PINK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ghost_1.png")
GHOST_BLUE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ghost_3.png")
PLAY_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/play.png")
STAR_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/star.png")
BACK_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/back.png")
IDEA_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/idea.png")


# ── SOUND ASSETS ──────────────────────────────
SND_GAMEOVER  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx/gameover.mp3")
SND_LEVELUP   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx/levelup.mp3")
SND_TUGASBITS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx/tugasbits.mp3")

# ── DIFFICULTY TABLE ──────────────────────────
DIFFICULTY = {
    "trial": dict(
        maze_size=9,  num_ghosts=1, ai_speed=28, maze_timer=0,
        dot_bonus=5,  level_bonus=50,
        label="TRIAL", desc="Maze 9x9 • 1 Dosen • Timer: OFF",
        color=(100,255,180), icon=GREEN_ICON,
    ),
    1: dict(
        maze_size=13, num_ghosts=2, ai_speed=24, maze_timer=30,
        dot_bonus=8,  level_bonus=80,
        label="Semester 1", desc="Maze 13x13 • 2 Dosen • Timer: 30s",
        color=(100,220,255), icon=BLUE_ICON,
    ),
    2: dict(
        maze_size=15, num_ghosts=3, ai_speed=20, maze_timer=25,
        dot_bonus=10, level_bonus=100,
        label="Semester 3", desc="Maze 15x15 • 3 Dosen • Timer: 25s",
        color=(255,220,80), icon=YELLOW_ICON,
    ),
    3: dict(
        maze_size=17, num_ghosts=3, ai_speed=16, maze_timer=22,
        dot_bonus=13, level_bonus=130,
        label="Semester 5", desc="Maze 17x17 • 3 Dosen • Timer: 22s",
        color=(255,140,60), icon=ORANGE_ICON,
    ),
    4: dict(
        maze_size=19, num_ghosts=4, ai_speed=13, maze_timer=20,
        dot_bonus=16, level_bonus=180,
        label="Semester 7", desc="Maze 19x19 • 4 Dosen • Timer: 20s",
        color=(220,50,50), icon=RED_ICON,
    ),
    "unlimited": dict(
        maze_size=15, num_ghosts=4, ai_speed=14, maze_timer=20,
        dot_bonus=12, level_bonus=200,
        label="SKRIPSI MODE", desc="Maze Dinamis • 4 Dosen • Timer: 20s ∞",
        color=(255,80,220), icon=UNLIMITED_ICON,
    ),
}

def get_difficulty(level):
    if level in DIFFICULTY:
        return DIFFICULTY[level]
    base = DIFFICULTY[4]
    extra = level - 4
    size = min(base["maze_size"] + extra * 2, MAX_MAZE)
    if size % 2 == 0: size += 1
    return dict(
        maze_size=size, num_ghosts=4,
        ai_speed=max(8, base["ai_speed"] - extra),
        maze_timer=max(12, base["maze_timer"] - extra),
        dot_bonus=base["dot_bonus"] + extra * 2,
        level_bonus=base["level_bonus"] + extra * 30,
        label=f"Semester {level*2-1}",
        desc=f"Maze {size}x{size} • 4 Dosen • Timer: {max(12,20-extra)}s",
        color=(255,100,100), icon=SKULL_ICON,
    )

def get_unlimited_diff(sub):
    base_size = min(15 + (sub-1)*2, MAX_MAZE)
    if base_size % 2 == 0: base_size += 1
    speed = max(8, 14 - (sub-1))
    return dict(
        maze_size=base_size, num_ghosts=4,
        ai_speed=speed, maze_timer=20,
        dot_bonus=12 + sub, level_bonus=200 + sub*50,
        label=f"SKRIPSI x {sub}",
        desc=f"Maze {base_size}x{base_size} • 4 Dosen • 20s",
        color=(255,80,220), icon=UNLIMITED_ICON,
    )

# Colors
C_WALL       = ( 30,  30, 100)
C_WALL_EDGE  = ( 80,  80, 200)
C_FLOOR      = ( 18,  18,  32)
C_DOT        = (255, 230, 100)
C_PANEL      = ( 22,  22,  44)
C_LINE       = ( 70,  70, 120)
C_TEXT       = (230, 230, 255)
C_TEXT_BOLD  = (240, 240, 250)
C_MUTED      = (150, 150, 190)
C_GOLD       = (255, 210,  60)
C_CYAN       = ( 60, 240, 255)
C_BAR_BG     = ( 50,  50,  80)
C_BAR_FILL   = (180,  60, 255)
C_RED        = (255,  90,  90)
C_GREEN      = ( 80, 255, 130)
C_BUTTON_BG  = ( 60,  50, 120)
C_BUTTON_HOV = ( 90,  70, 170)
C_TITLEBAR   = ( 15,  15,  38)
C_TITLE_TXT  = (200, 180, 255)
C_TRIAL_BDR  = ( 60, 220, 140)
C_UNLIM      = (255,  80, 220)
C_NEON_BLUE  = ( 30, 160, 255)

GHOST_COLS   = [(255,60,60),(255,140,60),(255,60,200),(200,60,255)]
GHOST_NAMES  = ["Dosen Killer (BFS)","Dosen Galak (Random)","Dosen AI (Q-Learn)","Dosen Skripsi (Heatmap)"]
GHOST_LABELS = ["Killer","Galak","AI","Skripsi"]

HS_FILE = "taskscape_leaderboard.json"

AVATARS = [
    {"name":"Mahasiswi",  "key":"mahasiswi","color":(255,160,200),"color2":(255,80,140)},
    {"name":"Mahasiswa",  "key":"mahasiswa","color":( 80,180,255),"color2":(200,230,255)},
    {"name":"Lumba-lumba","key":"dolphin",  "color":( 80,220,240),"color2":(255,255,255)},
    {"name":"Si Ngantuk", "key":"sleepy",   "color":(200,160,255),"color2":(255,200,100)},
    {"name":"Kucing Kopi","key":"catcoffee","color":(210,170,110),"color2":(255,200,50)},
    {"name":"Zombie SKS", "key":"zombie",   "color":( 80,220,120),"color2":(200,255,180)},
]

# ─────────────────────────────────────────────
# LEADERBOARD
# ─────────────────────────────────────────────
def load_leaderboard():
    if os.path.exists(HS_FILE):
        try:
            with open(HS_FILE) as f: return json.load(f)
        except: pass
    return []

def save_score(lb, score, level_label, dots, player_name=""):
    from datetime import date
    entry = {"score":score,"level_label":level_label,"dots":dots,"date":str(date.today())}
    if player_name:
        entry["name"] = player_name
    lb.append(entry)
    lb.sort(key=lambda x:-x["score"])
    lb = lb[:20]
    with open(HS_FILE,"w") as f: json.dump(lb, f, indent=2)
    return lb

# ─────────────────────────────────────────────
# MAZE
# ─────────────────────────────────────────────
DIRS = [(0,-1),(0,1),(-1,0),(1,0)]

def build_maze(cols, rows, seed):
    rng = random.Random(seed)
    maze = np.ones((rows,cols),dtype=np.int8)
    def carve(x,y):
        maze[y,x]=0
        steps=[(0,-2),(0,2),(-2,0),(2,0)]
        rng.shuffle(steps)
        for dx,dy in steps:
            nx,ny=x+dx,y+dy
            if 0<nx<cols-1 and 0<ny<rows-1 and maze[ny,nx]==1:
                maze[y+dy//2,x+dx//2]=0; carve(nx,ny)
    carve(1,1)
    extra=int(cols*rows*0.08); opened=0; attempts=0
    while opened<extra and attempts<5000:
        attempts+=1
        x=rng.randint(1,cols-2); y=rng.randint(1,rows-2)
        if maze[y,x]!=1: continue
        f=sum(maze[y+dy,x+dx]==0 for dx,dy in DIRS if 0<=x+dx<cols and 0<=y+dy<rows)
        if f>=2: maze[y,x]=0; opened+=1
    maze[1,1]=0
    heat=np.zeros((rows,cols),dtype=np.float32)
    dots={(x,y) for y in range(rows) for x in range(cols) if maze[y,x]==0 and (x,y)!=(1,1)}
    return maze,heat,dots

def can_move(maze,x,y):
    r,c=maze.shape
    return 0<=x<c and 0<=y<r and maze[y,x]==0

def bfs_next(maze,fx,fy,tx,ty):
    if fx==tx and fy==ty: return fx,fy
    vis={(fx,fy)}; q=deque([(fx,fy,[])])
    while q:
        cx,cy,path=q.popleft()
        for dx,dy in DIRS:
            nx,ny=cx+dx,cy+dy
            if can_move(maze,nx,ny) and (nx,ny) not in vis:
                vis.add((nx,ny)); np_=path+[(nx,ny)]
                if nx==tx and ny==ty: return np_[0] if np_ else (nx,ny)
                q.append((nx,ny,np_))
    return fx,fy

# ─────────────────────────────────────────────
# Q-LEARNING
# ─────────────────────────────────────────────
class QLearner:
    def __init__(self):
        self.q={}; self.alpha=0.25; self.gamma=0.95
        self.epsilon=0.6; self.episodes=0
    def _q(self,s):
        if s not in self.q: self.q[s]=[0.0]*4
        return self.q[s]
    def choose(self,hx,hy,px,py,vi,maze):
        s=(hx,hy,px,py)
        if not vi: return None,s,-1
        ai=random.choice(vi) if random.random()<self.epsilon else max(vi,key=lambda i:self._q(s)[i])
        return DIRS[ai],s,ai
    def update(self,s,a,r,hx,hy,px,py):
        if a<0: return
        ns=(hx,hy,px,py); qs=self._q(s); nqs=self._q(ns)
        qs[a]+=self.alpha*(r+self.gamma*max(nqs)-qs[a])
    def decay(self):
        self.episodes+=1; self.epsilon=max(0.05,0.6-self.episodes*0.008)

# ─────────────────────────────────────────────
# GHOST (DOSEN)
# ─────────────────────────────────────────────
class Ghost:
    def __init__(self,x,y,gid,agent=None):
        self.x=x; self.y=y; self.id=gid; self.agent=agent
        self.trail=deque(maxlen=8); self._ps=None; self._pa=-1
    def move(self,maze,px,py,heat,level):
        self.trail.append((self.x,self.y))
        valid=[(i,dx,dy) for i,(dx,dy) in enumerate(DIRS) if can_move(maze,self.x+dx,self.y+dy)]
        if not valid: return
        pd=abs(self.x-px)+abs(self.y-py)
        if self.id==0:
            nx,ny=bfs_next(maze,self.x,self.y,px,py)
        elif self.id==1:
            li=level if isinstance(level,int) else 0
            if random.random()<0.3+(li-1)*0.05:
                _,dx,dy=random.choice(valid); nx,ny=self.x+dx,self.y+dy
            else:
                best=-999; best_pos=(self.x,self.y)
                for _,dx,dy in valid:
                    cx2,cy2=self.x+dx,self.y+dy
                    sc=-(abs(cx2-px)+abs(cy2-py))*(1+random.random()*0.3)
                    if sc>best: best=sc; best_pos=(cx2,cy2)
                nx,ny=best_pos
        elif self.id==2:
            vi=[i for i,dx,dy in valid]
            action,s,ai=self.agent.choose(self.x,self.y,px,py,vi,maze)
            if action:
                nx,ny=self.x+action[0],self.y+action[1]
                if self._ps is not None:
                    nd=abs(nx-px)+abs(ny-py)
                    r=1.0 if nd<pd else -0.2
                    r+=0.5 if nd<5 else 0
                    self.agent.update(self._ps,self._pa,r,nx,ny,px,py)
                self._ps,self._pa=s,ai
            else: nx,ny=self.x,self.y
        else:
            best=-999; best_pos=(self.x,self.y)
            for _,dx,dy in valid:
                cx2,cy2=self.x+dx,self.y+dy
                sc=-(abs(cx2-px)+abs(cy2-py))+float(heat[cy2,cx2])*0.5+(2.0 if abs(cx2-px)+abs(cy2-py)<8 else 0)
                if sc>best: best=sc; best_pos=(cx2,cy2)
            nx,ny=best_pos
        self.x,self.y=nx,ny

# ─────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────
def draw_ghost(surf,col,cx,cy,r):
    pygame.draw.ellipse(surf,col,(cx-r,cy-int(r*0.6),r*2,int(r*1.8)))
    pygame.draw.rect(surf,col,(cx-r,int(cy-r*0.1),r*2,int(r*1.1)))
    w=(r*2)//4
    for i in range(4):
        if i%2==0: pygame.draw.rect(surf,(18,18,32),(cx-r+i*w,int(cy+r*0.85),w//2+2,8))
    for ex in (cx-r//3,cx+r//3):
        pygame.draw.circle(surf,(255,255,255),(ex,cy-r//3),max(3,int(r/2.5)))
        pygame.draw.circle(surf,(20,40,220),(ex+2,cy-r//3),max(2,r//4))
    hw=r+4; hh=max(4,r//3)
    pygame.draw.rect(surf,(20,20,80),(cx-hw//2,cy-r-hh,hw,hh))
    pygame.draw.rect(surf,(20,20,80),(cx-hw//2-4,cy-r-hh-5,hw+8,5))

def draw_avatar(surf,avatar,cx,cy,r,aframe,direction):
    key=avatar["key"]; col=avatar["color"]; col2=avatar["color2"]
    if key=="mahasiswi":
        pygame.draw.circle(surf,col,(cx,cy),r)
        hair_col=(80,40,20)
        pygame.draw.ellipse(surf,hair_col,(cx-r,cy-r,r*2,r+4))
        pygame.draw.rect(surf,hair_col,(cx-r-2,cy-r//2,5,r+2),border_radius=3)
        pygame.draw.rect(surf,hair_col,(cx+r-3,cy-r//2,5,r+2),border_radius=3)
        pygame.draw.circle(surf,(255,220,180),(cx,cy+2),r-4)
        for ex in (cx-r//3,cx+r//3):
            pygame.draw.circle(surf,(60,30,10),(ex,cy-2),max(2,r//4))
        pygame.draw.arc(surf,(200,100,100),(cx-r//4,cy+r//6,r//2,r//4),math.pi,2*math.pi,2)
        tick=(aframe//10)%2
        lc=(0,200,100) if tick==0 else (0,150,80)
        pygame.draw.rect(surf,lc,(cx-r//2,cy+r-4,r,r//2),border_radius=2)
    elif key=="mahasiswa":
        pygame.draw.circle(surf,col,(cx,cy),r)
        hair_col=(50,30,10)
        pygame.draw.ellipse(surf,hair_col,(cx-r+2,cy-r,r*2-4,r//2+4))
        for hx in range(cx-r+4,cx+r-2,5):
            hy=cy-r+2+((hx*3)%5)
            pygame.draw.polygon(surf,hair_col,[(hx,cy-r+2),(hx+3,cy-r-5),(hx+6,cy-r+2)])
        pygame.draw.circle(surf,(255,220,170),(cx,cy+2),r-4)
        for ex in (cx-r//3,cx+r//3):
            pygame.draw.ellipse(surf,(80,50,30),(ex-3,cy-4,6,5))
            pygame.draw.circle(surf,(40,20,0),(ex,cy-2),max(2,r//5))
        pygame.draw.arc(surf,(60,60,80),(cx-r+1,cy-r+1,r*2-2,r),math.pi,2*math.pi,3)
        for hx in (cx-r+1,cx+r-4):
            pygame.draw.circle(surf,(80,80,100),(hx,cy-r//2),4)
        pygame.draw.line(surf,(150,80,80),(cx-r//4,cy+r//4),(cx+r//4,cy+r//4),2)
    elif key=="dolphin":
        pygame.draw.ellipse(surf,col,(cx-r,cy-r//2,r*2,r))
        pygame.draw.ellipse(surf,col,(cx+r//2-2,cy-r//6,r//2+2,r//3))
        pygame.draw.polygon(surf,col,[(cx,cy-r//2),(cx+r//4,cy-r-4),(cx+r//2,cy-r//2)])
        pygame.draw.polygon(surf,col2,[(cx-r+2,cy),(cx-r-6,cy-r//3),(cx-r-6,cy+r//3)])
        pygame.draw.circle(surf,(20,20,40),(cx+r//3,cy-r//8),max(2,r//5))
        pygame.draw.circle(surf,(255,255,255),(cx+r//3+1,cy-r//8-1),max(1,r//8))
        cap_cx=cx+r//6; cap_cy=cy-r//2-2
        pygame.draw.rect(surf,(20,20,80),(cap_cx-r//3,cap_cy,r//1.5,r//4),border_radius=1)
        pygame.draw.rect(surf,(20,20,80),(cap_cx-r//2,cap_cy-r//5,r,r//5))
    elif key=="sleepy":
        pygame.draw.circle(surf,col,(cx,cy),r)
        for i,hx in enumerate(range(cx-r+2,cx+r,4)):
            hy=cy-r+2+((i*3)%5)
            pygame.draw.circle(surf,(100,60,20),(hx,hy),2)
        pygame.draw.circle(surf,(255,215,170),(cx,cy+1),r-4)
        for ex in (cx-r//3,cx+r//3):
            pygame.draw.line(surf,(60,30,10),(ex-4,cy-3),(ex+4,cy-3),2)
        if (aframe//20)%2==0:
            zz_s=pygame.font.Font(None,max(12,r)).render("z",True,col2)
            surf.blit(zz_s,(cx+r-4,cy-r))
        pygame.draw.ellipse(surf,(200,200,220),(cx-r//2,cy+r//3,r,r//2))
    elif key=="catcoffee":
        pygame.draw.circle(surf,col,(cx,cy),r)
        pygame.draw.polygon(surf,col,[(cx-r+4,cy-r+4),(cx-r-2,cy-r-8),(cx-r//2,cy-r+2)])
        pygame.draw.polygon(surf,col,[(cx+r-4,cy-r+4),(cx+r+2,cy-r-8),(cx+r//2,cy-r+2)])
        pygame.draw.polygon(surf,col2,[(cx-r+5,cy-r+5),(cx-r,cy-r-5),(cx-r//2+2,cy-r+4)])
        pygame.draw.circle(surf,(255,230,190),(cx,cy+2),r-3)
        for ex in (cx-r//3,cx+r//3):
            pygame.draw.ellipse(surf,(60,30,10),(ex-2,cy-4,4,5))
        for dy in (cy-2,cy+2):
            pygame.draw.line(surf,(100,80,60),(cx-r+3,dy),(cx-r//2,dy),1)
            pygame.draw.line(surf,(100,80,60),(cx+r-3,dy),(cx+r//2,dy),1)
        cup_x=cx+r//3; cup_y=cy+r//3
        pygame.draw.rect(surf,(180,100,50),(cup_x-4,cup_y,8,7),border_radius=2)
        pygame.draw.arc(surf,(180,100,50),(cup_x+2,cup_y+1,5,5),math.pi*1.5,math.pi*0.5,2)
        tick=(aframe//8)%3
        sy2=cup_y-2-tick
        pygame.draw.arc(surf,(200,200,200),(cup_x-2,sy2,4,5),0,math.pi,1)
    elif key=="zombie":
        pygame.draw.circle(surf,col,(cx,cy),r)
        for i in range(8):
            ang=math.radians(i*45)
            hx=cx+int(math.cos(ang)*(r-2))
            hy=cy+int(math.sin(ang)*(r-2))
            pygame.draw.circle(surf,(40,80,40),(hx,hy),3)
        pygame.draw.circle(surf,col,(cx,cy+1),r-4)
        for ex in (cx-r//3,cx+r//3):
            d2=max(2,r//5)
            pygame.draw.line(surf,col2,(ex-d2,cy-d2-2),(ex+d2,cy+d2-2),2)
            pygame.draw.line(surf,col2,(ex+d2,cy-d2-2),(ex-d2,cy+d2-2),2)
        pygame.draw.arc(surf,(100,200,100),(cx-r//3,cy+2,r//1.5,r//3),0,math.pi,2)
        tick2=(aframe//15)%2
        sc=(255,255,200) if tick2==0 else (255,255,100)
        pygame.draw.rect(surf,sc,(cx+r//3,cy-r//3,r//2,r//3),border_radius=1)

def draw_avatar_preview(surf,avatar,cx,cy,r):
    draw_avatar(surf,avatar,cx,cy,r,0,(1,0))

def draw_rr(surf,color,rect,radius=6,width=0):
    pygame.draw.rect(surf,color,rect,width,border_radius=radius)

def draw_btn_content(surf, rect, icon_path, icon_size, text, font, text_color, gap=8):
    """Draw icon + text centered inside rect, clipped to fit."""
    icon_surf = None
    if icon_path and os.path.exists(icon_path):
        try:
            raw = pygame.image.load(icon_path).convert_alpha()
            icon_surf = pygame.transform.smoothscale(raw, (icon_size, icon_size))
        except:
            pass
    text_surf = font.render(text, True, text_color)
    total_w = text_surf.get_width() + (icon_size + gap if icon_surf else 0)
    if total_w > rect.width - 16:
        small_font = pygame.font.Font(None, max(14, font.size(" ")[1] - 4))
        text_surf = small_font.render(text, True, text_color)
        total_w = text_surf.get_width() + (icon_size + gap if icon_surf else 0)
    start_x = rect.centerx - total_w // 2
    cy = rect.centery
    if icon_surf:
        surf.blit(icon_surf, (start_x, cy - icon_size // 2))
        surf.blit(text_surf, text_surf.get_rect(midleft=(start_x + icon_size + gap, cy)))
    else:
        surf.blit(text_surf, text_surf.get_rect(center=(rect.centerx, cy)))

# ─────────────────────────────────────────────
# SCORE ANIM
# ─────────────────────────────────────────────
class ScoreAnim:
    def __init__(self,x,y,text):
        self.x=x; self.y=y; self.text=text; self.age=0; self.max_age=45
        self.MAZE_X=0; self.MAZE_Y=0
    @property
    def alive(self): return self.age<self.max_age
    def set_pos(self,mx,my): self.MAZE_X=mx; self.MAZE_Y=my
    def draw(self,surf,font,cell):
        alpha=max(0,255-int(255*self.age/self.max_age))
        t=font.render(self.text,True,C_GOLD); t.set_alpha(alpha)
        surf.blit(t,(self.MAZE_X+self.x*cell+cell//2-t.get_width()//2,
                     self.MAZE_Y+self.y*cell-self.age*2))
        self.age+=1

# ─────────────────────────────────────────────
# GAME
# ─────────────────────────────────────────────
class Game:
    def __init__(self):
        # ── SOUND: inisialisasi mixer SEBELUM pygame.init() penuh ──
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption("TASKSCAPE — Maze Deadline Dodger")
        info=pygame.display.Info()
        self.SW=info.current_w; self.SH=info.current_h
        self.screen=pygame.display.set_mode((self.SW,self.SH),pygame.NOFRAME)
        os.environ['SDL_VIDEO_CENTERED']='1'
        pygame.mouse.set_visible(True)

        self.logo_surf = None
        if os.path.exists(LOGO_FILE):
            try:
                raw = pygame.image.load(LOGO_FILE).convert_alpha()
                lw, lh = raw.get_size()
                target_w = min(700, self.SW - 100)
                scale = target_w / lw
                target_h = int(lh * scale)
                if target_h > 280:
                    scale = 280 / lh
                    target_w = int(lw * scale)
                    target_h = 280
                self.logo_surf = pygame.transform.smoothscale(raw, (target_w, target_h))
                self.logo_w, self.logo_h = target_w, target_h
            except Exception as e:
                print("Logo load failed:", e)
                self.logo_surf = None

        # ── SOUND: load semua sound effect ──────────────────────────
        def _load_snd(path):
            try:
                snd = pygame.mixer.Sound(path)
                return snd
            except Exception as e:
                print(f"[Sound] Gagal load {os.path.basename(path)}: {e}")
                return None

        self.snd_gameover  = _load_snd(SND_GAMEOVER)
        self.snd_levelup   = _load_snd(SND_LEVELUP)
        self.snd_tugasbits = _load_snd(SND_TUGASBITS)

        # Volume masing-masing sound
        if self.snd_tugasbits: self.snd_tugasbits.set_volume(0.55)
        if self.snd_levelup:   self.snd_levelup.set_volume(0.80)
        if self.snd_gameover:  self.snd_gameover.set_volume(1.00)
        # ────────────────────────────────────────────────────────────

        self.lb=load_leaderboard()
        self.agent=QLearner()
        self.score=0; self.lives=5; self.anim_frame=0

        self.state="splash"
        self._splash_start=pygame.time.get_ticks()
        self._splash_duration=3500
        self._splash_clicked=False

        self.player_name=""
        self._name_active=True
        self.score_anims=[]; self.maze_flash=0
        self.dots_eaten=0; self.total_dots_eaten_run=0
        self.paused=False
        self._esc_yes_rect=None; self._esc_no_rect=None
        self._countdown_val=0; self._countdown_ms=0; self._countdown_dest="playing"
        self._powerup_timer=25
        self._powerup_active=None
        self._powerup_on_floor=None
        self._powerup_spawn_ms=0
        self._POWERUP_TYPES=["extra_life","slow_ghost","freeze_ghost","shield","dot_magnet"]
        self.selected_avatar=0; self.show_avatar_menu=False; self.avatar_rects=[]
        self.mouse_pos=(0,0)
        self._dragging=False; self._drag_offset=(0,0)
        self._held_dir=None; self._hold_start=0; self._last_rep=0
        self.start_button_rect=None; self.retry_button_rect=None
        self._level_clear_timer=0; self._level_clear_msg=""
        self._life_bonus_timer=0
        self.start_level="trial"
        self.level="trial"
        self.unlimited_sub=1
        self.level_card_rects=[]
        self._lc_cont_rect=None
        self._lc_quit_rect=None
        self._maze_reshuffle_last=time.time()
        self._maze_reshuffle_next=0

        self._login_exit_rect=None
        self._login_input_rect=None
        self._login_start_rect=None
        self._login_av_rects=[]

        self.fxxl=pygame.font.Font(None,72); self.fxl=pygame.font.Font(None,48)
        self.flg=pygame.font.Font(None,36);  self.fmd=pygame.font.Font(None,28)
        self.fsm=pygame.font.Font(None,22);  self.fxs=pygame.font.Font(None,18)
        self.ftb=pygame.font.Font(None,20)

        self._init_round(); self._setup_layout()

    def _diff(self):
        if self.level=="unlimited":
            return get_unlimited_diff(self.unlimited_sub)
        return get_difficulty(self.level)

    def _maze_size(self):
        n=self._diff()["maze_size"]
        if n%2==0: n+=1
        return n,n

    def _setup_layout(self):
        cols,rows=self._maze_size()
        aw=self.SW-PANEL_W; ah=self.SH-TITLEBAR_H
        self.CELL=max(22,min(38,aw//cols,ah//rows))
        self.MAZE_W=cols*self.CELL; self.MAZE_H=rows*self.CELL
        self.MAZE_X=(self.SW-PANEL_W-self.MAZE_W)//2
        self.MAZE_Y=TITLEBAR_H+(ah-self.MAZE_H)//2
        for a in self.score_anims: a.set_pos(self.MAZE_X,self.MAZE_Y)

    def _init_round(self):
        d=self._diff()
        cols,rows=self._maze_size()
        seed=(self.level if isinstance(self.level,int) else 0)*1237+int(time.time())%1000
        if self.level=="unlimited":
            seed=self.unlimited_sub*997+int(time.time())%1000
        self.maze,self.heat,self.dots=build_maze(cols,rows,seed)
        self.total_dots=len(self.dots); self.cols=cols; self.rows=rows
        self.ai_speed=d["ai_speed"]
        self.maze_timer_max=d["maze_timer"]; self.maze_timer=self.maze_timer_max
        self.player=[1,1]; self.player_dir=[1,0]
        self.last_tick=time.time(); self.frame=0
        self.score_anims=[]; self.dots_eaten=0
        self._powerup_timer=25; self._powerup_active=None
        self._powerup_on_floor=None; self._powerup_spawn_ms=0
        self._maze_reshuffle_last=time.time()
        self._maze_reshuffle_next=self.maze_timer_max
        num_g=d["num_ghosts"]
        spawns=[(cols-2,1),(cols-2,rows-2),(1,rows-2),(cols//2,1)]
        self.ghosts=[Ghost(spawns[i][0],spawns[i][1],i,
                           self.agent if i==2 else None) for i in range(num_g)]

    def move_player(self,dx,dy):
        if self.state!="playing" or self.paused: return
        nx,ny=self.player[0]+dx,self.player[1]+dy
        if not can_move(self.maze,nx,ny): return
        self.player=[nx,ny]; self.player_dir=[dx,dy]
        self.heat[ny,nx]+=1.2
        if self._powerup_on_floor and (nx,ny)==(self._powerup_on_floor[0],self._powerup_on_floor[1]):
            self._activate_powerup(self._powerup_on_floor[2])
            self._powerup_on_floor=None
        if (nx,ny) in self.dots:
            self.dots.discard((nx,ny)); self.dots_eaten+=1; self.total_dots_eaten_run+=1
            d=self._diff()
            pts=d["dot_bonus"]+((self.level*2) if isinstance(self.level,int) else 0)
            self.score+=pts
            a=ScoreAnim(nx,ny,f"+{pts}"); a.set_pos(self.MAZE_X,self.MAZE_Y)
            self.score_anims.append(a)
            # ── SOUND: putar suara saat mengumpulkan tugas/dot ──
            if self.snd_tugasbits:
                self.snd_tugasbits.play()
        if len(self.dots)==0: self._next_level()
        else: self._check_col()

    def _check_col(self):
        px,py=self.player
        for gh in self.ghosts:
            if gh.x==px and gh.y==py:
                if self._powerup_active and self._powerup_active["type"]=="shield":
                    self._powerup_active=None
                    a=ScoreAnim(px,py,"PERISAI!"); a.set_pos(self.MAZE_X,self.MAZE_Y)
                    self.score_anims.append(a)
                    return
                self._lose_life(); return

    def _lose_life(self):
        self.lives-=1
        if self.lives<=0:
            # ── SOUND: putar suara game over ──
            if self.snd_gameover:
                pygame.mixer.stop()   # hentikan suara lain dulu
                self.snd_gameover.play()
            lbl=self._diff()["label"]
            self.lb=save_score(self.lb,self.score,lbl,self.total_dots_eaten_run,self.player_name)
            self.state="game_over"
            self.msg_title="DEADLINE TERLEWAT!"
            self.msg_sub=f"Skor: {self.score:,} | {lbl} | Tugas: {self.total_dots_eaten_run:,}"
            self.score=0; self.dots_eaten=0; self.total_dots_eaten_run=0
            self.lives=5; self.unlimited_sub=1
        else:
            self.player=[1,1]; self.player_dir=[1,0]
            for gh in self.ghosts: gh.x,gh.y=self.cols-2,1

    def _next_level(self):
        # ── SOUND: putar suara level up / semester selesai ──
        if self.snd_levelup:
            pygame.mixer.stop()   # hentikan suara lain dulu agar tidak tumpang tindih
            self.snd_levelup.play()
        d=self._diff()
        bonus=self.dots_eaten*d["dot_bonus"]+d["level_bonus"]
        self.score+=bonus
        self._level_clear_msg=d["label"]
        self._level_clear_timer=90
        self._confirm_prev_diff=d
        self._confirm_bonus=bonus
        self._confirm_next_lives=min(self.lives+1,MAX_LIVES) if self.lives<MAX_LIVES else self.lives
        self._confirm_life_gained=self.lives<MAX_LIVES
        if self.level=="unlimited":
            next_level="unlimited"; next_sub=self.unlimited_sub+1
        elif self.level=="trial":
            next_level=1; next_sub=None
        else:
            next_level=self.level+1; next_sub=None
        if next_level=="unlimited":
            from_sub=(self.unlimited_sub+1) if self.level=="unlimited" else 1
            self._confirm_next_diff=get_unlimited_diff(from_sub)
        else:
            self._confirm_next_diff=get_difficulty(next_level)
        self._confirm_next_level=next_level
        self._confirm_next_sub=next_sub
        self.paused=True
        self.state="level_confirm"

    def _apply_next_level(self):
        if self._confirm_life_gained:
            self.lives+=1
            self._life_bonus_timer=120
        if self._confirm_next_level=="unlimited":
            self.level="unlimited"
            if self._confirm_next_sub:
                self.unlimited_sub=self._confirm_next_sub
            else:
                self.unlimited_sub=1
        else:
            self.level=self._confirm_next_level
        self._init_round()
        self._setup_layout()
        self.maze_flash=30
        self.paused=False
        self.state="countdown"
        self._countdown_ms=pygame.time.get_ticks()
        self._countdown_dest="playing"

    def _step_ai(self):
        if self.paused: return
        frozen=self._powerup_active and self._powerup_active["type"]=="freeze_ghost"
        if not frozen:
            for gh in self.ghosts:
                gh.move(self.maze,self.player[0],self.player[1],self.heat,self.level)
        self.agent.decay(); self._check_col()

    _POWERUP_META={
        "extra_life": {"label":"+1 NYAWA","icon":HEART_ICON,"color":(255,100,150),"duration":0},
        "slow_ghost":  {"label":"DOSEN LAMBAT","icon":TURTLE_ICON,"color":(100,255,200),"duration":10*60},
        "freeze_ghost":{"label":"DOSEN BEKU","icon":FREEZE_ICON,"color":(100,200,255),"duration":5*60},
        "shield":      {"label":"PERISAI","icon":SHIELD_ICON,"color":(255,220,80),"duration":15*60},
        "dot_magnet":  {"label":"TUGAS MAGNET","icon":MAGNET_ICON,"color":(200,100,255),"duration":8*60},
    }

    def _spawn_powerup(self):
        floors=[(x,y) for y in range(self.rows) for x in range(self.cols)
                if self.maze[y,x]==0
                and (x,y)!=tuple(self.player)
                and (x,y) not in {(g.x,g.y) for g in self.ghosts}
                and (x,y) not in self.dots]
        if not floors: return
        pos=random.choice(floors)
        ptype=random.choice(self._POWERUP_TYPES)
        self._powerup_on_floor=(pos[0],pos[1],ptype)
        self._powerup_spawn_ms=pygame.time.get_ticks()

    def _activate_powerup(self,ptype):
        meta=self._POWERUP_META[ptype]
        if ptype=="extra_life":
            if self.lives<MAX_LIVES: self.lives+=1
            a=ScoreAnim(self.player[0],self.player[1],meta["label"])
            a.set_pos(self.MAZE_X,self.MAZE_Y); self.score_anims.append(a)
            return
        if ptype=="slow_ghost":
            self.ai_speed=max(self.ai_speed+18,40)
        self._powerup_active={"type":ptype,"frames":meta["duration"]}
        a=ScoreAnim(self.player[0],self.player[1],meta["label"])
        a.set_pos(self.MAZE_X,self.MAZE_Y); self.score_anims.append(a)

    def _tick_powerup(self):
        self._powerup_timer-=1
        if self._powerup_timer<=0 and self._powerup_on_floor is None:
            self._spawn_powerup()
            self._powerup_timer=25
        if self._powerup_on_floor:
            age_ms=pygame.time.get_ticks()-self._powerup_spawn_ms
            if age_ms>10000:
                self._powerup_on_floor=None
                self._powerup_timer=15

    def _tick_active_powerup_frame(self):
        if not self._powerup_active: return
        self._powerup_active["frames"]-=1
        if self._powerup_active["frames"]<=0:
            expired=self._powerup_active["type"]
            if expired=="slow_ghost":
                self.ai_speed=self._diff()["ai_speed"]
            self._powerup_active=None

    def _apply_dot_magnet(self):
        if not (self._powerup_active and self._powerup_active["type"]=="dot_magnet"): return
        px,py=self.player
        for dx in range(-2,3):
            for dy in range(-2,3):
                nx2,ny2=px+dx,py+dy
                if (nx2,ny2) in self.dots:
                    self.dots.discard((nx2,ny2)); self.dots_eaten+=1; self.total_dots_eaten_run+=1
                    d=self._diff(); self.score+=d["dot_bonus"]

    def _reshuffle_maze(self):
        if not self.dots: return
        rng=random.Random(int(time.time()))
        opened=0; tries=0; target=random.randint(6,12)
        while opened<target and tries<1500:
            tries+=1; x=rng.randint(1,self.cols-2); y=rng.randint(1,self.rows-2)
            if self.maze[y,x]==1:
                f=sum(can_move(self.maze,x+dx,y+dy) for dx,dy in DIRS)
                if f>=2:
                    self.maze[y,x]=0; opened+=1
        self.maze_flash=40
        self._maze_reshuffle_last=time.time()
        self._maze_reshuffle_next=self.maze_timer_max

    # ═══════════════════════════════════════════
    # DRAW: SPLASH SCREEN
    # ═══════════════════════════════════════════
    def _draw_splash(self):
        self.screen.fill((0,0,0))
        t=pygame.time.get_ticks()
        elapsed=t-self._splash_start
        for i in range(0, self.SW, 80):
            alpha=int(30+20*math.sin(t*0.002+i*0.05))
            pygame.draw.line(self.screen,(0,alpha,alpha*2),(i,0),(i,self.SH),1)
        for j in range(0, self.SH, 80):
            alpha=int(30+20*math.sin(t*0.002+j*0.05))
            pygame.draw.line(self.screen,(0,alpha,alpha*2),(0,j),(self.SW,j),1)
        cx=self.SW//2; cy=self.SH//2
        fade_in=min(255,int(elapsed/600*255))
        fade_out=255
        if elapsed>self._splash_duration-600:
            fade_out=max(0,int((self._splash_duration-elapsed)/600*255))
        alpha=min(fade_in,fade_out)
        if self.logo_surf:
            scale=1.0+0.015*math.sin(t*0.003)
            lw=int(self.logo_w*scale); lh=int(self.logo_h*scale)
            scaled=pygame.transform.smoothscale(self.logo_surf,(lw,lh))
            glow_surf=pygame.Surface((lw+40,lh+40),pygame.SRCALPHA)
            glow_intensity=int(60+40*math.sin(t*0.004))
            for gi in range(3):
                gp=glow_intensity//(gi+1)
                pygame.draw.rect(glow_surf,(0,160,255,gp),(gi*5,gi*5,lw+40-gi*10,lh+40-gi*10),border_radius=20)
            glow_surf.set_alpha(alpha)
            self.screen.blit(glow_surf,(cx-lw//2-20,cy-lh//2-30))
            scaled.set_alpha(alpha)
            self.screen.blit(scaled,(cx-lw//2,cy-lh//2-20))
        if elapsed>1500:
            blink=(t//600)%2==0
            if blink:
                hint=self.fmd.render("Klik atau tekan ENTER untuk mulai",True,C_NEON_BLUE)
                hint.set_alpha(alpha)
                self.screen.blit(hint,hint.get_rect(center=(cx,cy+self.logo_h//2+30)))
        for i in range(5):
            filled=i<int(elapsed/(self._splash_duration/5))
            dcol=C_NEON_BLUE if filled else (40,40,80)
            pygame.draw.circle(self.screen,dcol,(cx-40+i*20,cy+self.logo_h//2+65),5)

    # ═══════════════════════════════════════════
    # DRAW: TITLEBAR
    # ═══════════════════════════════════════════
    def _draw_titlebar(self):
        pygame.draw.rect(self.screen,C_TITLEBAR,(0,0,self.SW,TITLEBAR_H))
        pygame.draw.line(self.screen,C_LINE,(0,TITLEBAR_H-1),(self.SW,TITLEBAR_H-1),1)
        d=self._diff()
        ts=self.ftb.render(f"TASKSCAPE  —  {d['label']}",True,C_TITLE_TXT)
        self.screen.blit(ts,(12,TITLEBAR_H//2-ts.get_height()//2))
        if self.player_name:
            ns=self.ftb.render(f"{self.player_name}",True,C_GOLD)
            self.screen.blit(ns,ns.get_rect(center=(self.SW//2,TITLEBAR_H//2)))
        av=AVATARS[self.selected_avatar]
        al=self.ftb.render(f"Avatar: {av['name']}",True,av["color"])
        self.screen.blit(al,(self.SW-PANEL_W-al.get_width()-20,TITLEBAR_H//2-al.get_height()//2))
        bsz=22; gap=8; rm=12
        cx0=self.SW-rm-bsz; mx0=cx0-bsz-gap; cy0=TITLEBAR_H//2-bsz//2
        self.close_rect=pygame.Rect(cx0,cy0,bsz,bsz)
        self.minimize_rect=pygame.Rect(mx0,cy0,bsz,bsz)
        hc=self.close_rect.collidepoint(self.mouse_pos)
        hm=self.minimize_rect.collidepoint(self.mouse_pos)
        pygame.draw.circle(self.screen,(255,80,80) if hc else (200,60,60),(cx0+bsz//2,cy0+bsz//2),bsz//2)
        p=5
        pygame.draw.line(self.screen,(255,255,255),(cx0+p,cy0+p),(cx0+bsz-p,cy0+bsz-p),2)
        pygame.draw.line(self.screen,(255,255,255),(cx0+bsz-p,cy0+p),(cx0+p,cy0+bsz-p),2)
        pygame.draw.circle(self.screen,(255,210,80) if hm else (200,165,40),(mx0+bsz//2,cy0+bsz//2),bsz//2)
        pygame.draw.line(self.screen,(255,255,255),(mx0+5,cy0+bsz//2),(mx0+bsz-5,cy0+bsz//2),2)

    # ═══════════════════════════════════════════
    # DRAW: AVATAR OVERLAY
    # ═══════════════════════════════════════════
    def _draw_avatar_overlay(self):
        ov=pygame.Surface((self.SW,self.SH),pygame.SRCALPHA); ov.fill((0,0,0,220))
        self.screen.blit(ov,(0,0))
        t=self.fxl.render("Pilih Avatar Mahasiswa",True,C_GOLD)
        self.screen.blit(t,t.get_rect(center=(self.SW//2,TITLEBAR_H+50)))
        n=len(AVATARS); cw,ch=160,200; tw=n*cw+(n-1)*20
        sx=self.SW//2-tw//2; sy=TITLEBAR_H+100; self.avatar_rects=[]
        for i,av in enumerate(AVATARS):
            x=sx+i*(cw+20); rect=pygame.Rect(x,sy,cw,ch); self.avatar_rects.append(rect)
            isel=i==self.selected_avatar; ihov=rect.collidepoint(self.mouse_pos)
            bg=(60,60,140) if isel else ((45,45,90) if ihov else (30,30,60))
            draw_rr(self.screen,bg,rect,12)
            draw_rr(self.screen,av["color"] if isel else C_LINE,rect,12,3 if isel else (2 if ihov else 1))
            pcx=x+cw//2; pcy=sy+70
            pygame.draw.circle(self.screen,(15,15,40),(pcx,pcy),42)
            pygame.draw.circle(self.screen,av["color"],(pcx,pcy),42,2)
            draw_avatar_preview(self.screen,av,pcx,pcy,36)
            ns=self.fmd.render(av["name"],True,av["color"] if isel else C_TEXT)
            self.screen.blit(ns,ns.get_rect(center=(x+cw//2,sy+135)))
            if isel:
                bs=self.fsm.render("TERPILIH",True,C_GREEN)
                self.screen.blit(bs,bs.get_rect(center=(x+cw//2,sy+160)))
        cb=pygame.Rect(self.SW//2-130,sy+ch+30,260,55); self.avatar_close_rect=cb
        hov=cb.collidepoint(self.mouse_pos)
        draw_rr(self.screen,C_BUTTON_HOV if hov else C_BUTTON_BG,cb,12)
        draw_rr(self.screen,C_TEXT_BOLD,cb,12,2)
        ct=self.flg.render("Konfirmasi & Tutup",True,C_TEXT)
        self.screen.blit(ct,ct.get_rect(center=cb.center))

    # ═══════════════════════════════════════════
    # DRAW: LOGIN PAGE
    # ═══════════════════════════════════════════
    def _draw_login(self):
        self.screen.fill((10,8,22))
        t=pygame.time.get_ticks()
        for i in range(20):
            bx=int((math.sin(t*0.0002+i*1.4)*0.45+0.5)*self.SW)
            by=int((math.cos(t*0.00015+i*0.85)*0.4+0.5)*self.SH)
            pygame.draw.circle(self.screen,(40,30,60),(bx,by),3)
        cx=self.SW//2

        logo_y = TITLEBAR_H + 18
        if self.logo_surf:
            scale = min(1.0, 460 / self.logo_w)
            lw = int(self.logo_w * scale); lh = int(self.logo_h * scale)
            if lh > 120:
                scale = 120 / self.logo_h
                lw = int(self.logo_w * scale); lh = 120
            small_logo = pygame.transform.smoothscale(self.logo_surf, (lw, lh))
            self.screen.blit(small_logo, small_logo.get_rect(center=(cx, logo_y + lh//2)))
            logo_bottom = logo_y + lh + 10
        else:
            title=self.fxl.render("TASKSCAPE",True,C_NEON_BLUE)
            self.screen.blit(title,title.get_rect(center=(cx,logo_y+24)))
            logo_bottom = logo_y + 60

        name_label=self.flg.render("Nama Mahasiswa",True,C_GOLD)
        label_y = logo_bottom + 10
        self.screen.blit(name_label,name_label.get_rect(center=(cx,label_y)))

        inp_w,inp_h=420,52; inp_x=cx-inp_w//2; inp_y=label_y+28
        self._login_input_rect=pygame.Rect(inp_x,inp_y,inp_w,inp_h)
        border_col=C_CYAN if self._name_active else C_LINE
        draw_rr(self.screen,(20,18,50),self._login_input_rect,12)
        draw_rr(self.screen,border_col,self._login_input_rect,12,2)
        blink=((t//500)%2==0)
        cursor=" |" if (self._name_active and blink) else ""
        name_surf=self.flg.render(self.player_name+cursor,True,C_TEXT)
        self.screen.blit(name_surf,name_surf.get_rect(midleft=(inp_x+16,inp_y+inp_h//2)))
        hint_t=self.fxs.render("Maks. 18 karakter  |  Enter untuk lanjut",True,C_MUTED)
        self.screen.blit(hint_t,hint_t.get_rect(center=(cx,inp_y+inp_h+14)))

        av_label_y = inp_y + inp_h + 58
        av_label=self.flg.render("Pilih Avatar",True,C_GOLD)
        self.screen.blit(av_label,av_label.get_rect(center=(cx,av_label_y)))

        n=len(AVATARS); cw,ch=128,162; gap=14
        tw=n*cw+(n-1)*gap; sx=cx-tw//2; sy=av_label_y+22
        self._login_av_rects=[]
        for i,av in enumerate(AVATARS):
            x=sx+i*(cw+gap); rect=pygame.Rect(x,sy,cw,ch)
            self._login_av_rects.append(rect)
            isel=i==self.selected_avatar; ihov=rect.collidepoint(self.mouse_pos)
            bg=(55,45,120) if isel else ((40,35,80) if ihov else (25,22,55))
            draw_rr(self.screen,bg,rect,12)
            draw_rr(self.screen,av["color"] if isel else (C_LINE if ihov else (40,35,70)),rect,12,3 if isel else 1)
            pcx=x+cw//2; pcy=sy+50
            pygame.draw.circle(self.screen,(15,12,40),(pcx,pcy),34)
            pygame.draw.circle(self.screen,av["color"],(pcx,pcy),34,2)
            draw_avatar_preview(self.screen,av,pcx,pcy,26)
            ns=self.fsm.render(av["name"],True,av["color"] if isel else C_TEXT)
            self.screen.blit(ns,ns.get_rect(center=(x+cw//2,sy+96)))
            if isel:
                try:
                    check_img = pygame.image.load(CHECK_ICON).convert_alpha()
                    check_img = pygame.transform.smoothscale(check_img, (18, 18))
                    check_rect = check_img.get_rect(center=(x + cw//2 - 28, sy + 116))
                    self.screen.blit(check_img, check_rect)
                    ts = self.fxs.render("Dipilih", True, C_GREEN)
                    self.screen.blit(ts, ts.get_rect(midleft=(check_rect.right + 6, sy + 116)))
                except:
                    ts=self.fxs.render("Dipilih",True,C_GREEN)
                    self.screen.blit(ts,ts.get_rect(center=(x+cw//2,sy+116)))

        can_start=bool(self.player_name.strip())
        btn_w,btn_h=360,58; bx=cx-btn_w//2; by=sy+ch+20
        self._login_start_rect=pygame.Rect(bx,by,btn_w,btn_h)
        hov=self._login_start_rect.collidepoint(self.mouse_pos) and can_start
        bg_col=(60,100,40) if (can_start and not hov) else ((80,140,55) if hov else (40,35,65))
        border_col2=C_GREEN if can_start else C_MUTED
        draw_rr(self.screen,bg_col,self._login_start_rect,14)
        draw_rr(self.screen,border_col2,self._login_start_rect,14,3)
        btn_txt = "Pilih Semester & Mulai" if can_start else "Masukkan nama dulu"
        icon_path = GAME_ICON if can_start else PENCIL_ICON
        txt_color = (255,255,255) if can_start else C_MUTED
        draw_btn_content(self.screen, self._login_start_rect, icon_path, 24,
                         btn_txt, self.fmd, txt_color, gap=8)

        ex_w,ex_h=160,44
        ex_x=self.SW-ex_w-24; ex_y=self.SH-ex_h-18
        self._login_exit_rect=pygame.Rect(ex_x,ex_y,ex_w,ex_h)
        hov_ex=self._login_exit_rect.collidepoint(self.mouse_pos)
        draw_rr(self.screen,(80,25,25) if hov_ex else (50,18,18),self._login_exit_rect,10)
        draw_rr(self.screen,(255,80,80),self._login_exit_rect,10,2)
        draw_btn_content(self.screen, self._login_exit_rect, EXIT_ICON, 20,
                         "Keluar", self.fmd, (255,120,120), gap=8)

    # ═══════════════════════════════════════════
    # DRAW: LEVEL SELECT
    # ═══════════════════════════════════════════
    def _draw_level_select(self):
        self.screen.fill((10,8,22))
        t=pygame.time.get_ticks()
        for i in range(30):
            bx=int((math.sin(t*0.0003+i*1.1)*0.38+0.5)*self.SW)
            by=int((math.cos(t*0.0002+i*0.8)*0.38+0.5)*self.SH)
            pygame.draw.circle(self.screen,(40,30,70),(bx,by),3)

        cx=self.SW//2
        title=self.fxxl.render("PILIH SEMESTER",True,C_GOLD)
        self.screen.blit(title,title.get_rect(center=(cx,TITLEBAR_H+42)))
        sub=self.fsm.render("Makin tinggi semester, makin banyak dosen yang mengejarmu!",True,C_MUTED)
        self.screen.blit(sub,sub.get_rect(center=(cx,TITLEBAR_H+82)))

        levels_order=["trial",1,2,3,4,"unlimited"]
        n=len(levels_order)
        available_w=self.SW-80
        card_w=min(200,(available_w-(n-1)*18)//n)
        card_h=240; gap=18
        total_w=n*card_w+(n-1)*gap
        sx=max(40,cx-total_w//2)
        sy=TITLEBAR_H+108

        self.level_card_rects=[]
        for i,lv in enumerate(levels_order):
            d=get_difficulty(lv) if lv!="unlimited" else DIFFICULTY["unlimited"]
            x=sx+i*(card_w+gap)
            rect=pygame.Rect(x,sy,card_w,card_h)
            self.level_card_rects.append((lv,rect))
            is_unlim=(lv=="unlimited"); is_trial=(lv=="trial")
            hov=rect.collidepoint(self.mouse_pos)
            col=d["color"]

            shadow=pygame.Rect(x+4,sy+4,card_w,card_h)
            draw_rr(self.screen,(0,0,0),shadow,18)

            if is_unlim:
                bg=(70,10,55) if not hov else (100,15,80)
                border=C_UNLIM
            elif is_trial:
                bg=(12,48,30) if not hov else (20,68,44)
                border=C_TRIAL_BDR
            else:
                bg=(28,28,60) if not hov else (42,42,90)
                border=col
            draw_rr(self.screen,bg,rect,18)
            draw_rr(self.screen,border,rect,18,3 if hov else 2)

            try:
                icon_img = pygame.image.load(d["icon"]).convert_alpha()
                icon_img = pygame.transform.smoothscale(icon_img, (40, 40))
                self.screen.blit(icon_img, icon_img.get_rect(center=(x+card_w//2, sy+34)))
            except:
                icon_s = self.fxl.render("?", True, col)
                self.screen.blit(icon_s, icon_s.get_rect(center=(x+card_w//2, sy+34)))

            lbl_s=self.fmd.render(d["label"],True,col)
            self.screen.blit(lbl_s,lbl_s.get_rect(center=(x+card_w//2,sy+68)))

            ms=d["maze_size"]
            size_s=self.fsm.render(f"Maze {ms}×{ms}",True,C_TEXT)
            self.screen.blit(size_s,size_s.get_rect(center=(x+card_w//2,sy+92)))

            ghost_imgs = []
            if lv == "trial":          ghost_imgs = [GHOST_RED]
            elif lv == 1:              ghost_imgs = [GHOST_RED, GHOST_ORANGE]
            elif lv == 2:              ghost_imgs = [GHOST_RED, GHOST_ORANGE, GHOST_PINK]
            elif lv == 3:              ghost_imgs = [GHOST_RED, GHOST_ORANGE, GHOST_PINK]
            elif lv in (4,"unlimited"):ghost_imgs = [GHOST_RED, GHOST_ORANGE, GHOST_PINK, GHOST_BLUE]

            ghost_size = 28; spacing = ghost_size + 4
            total_ghost_w = len(ghost_imgs) * ghost_size + (len(ghost_imgs)-1) * 4
            ghost_start_x = x + card_w//2 - total_ghost_w//2
            ghost_y = sy + 102
            for gi, gpath in enumerate(ghost_imgs):
                try:
                    ghost_img = pygame.image.load(gpath).convert_alpha()
                    ghost_img = pygame.transform.smoothscale(ghost_img, (ghost_size, ghost_size))
                    self.screen.blit(ghost_img, (ghost_start_x + gi * spacing, ghost_y))
                except:
                    pass

            timer_str="Timer: OFF" if d["maze_timer"]==0 else f"Timer: {d['maze_timer']}s"
            tc=C_TRIAL_BDR if d["maze_timer"]==0 else (C_UNLIM if is_unlim else C_GOLD)
            ts=self.fsm.render(timer_str,True,tc)
            self.screen.blit(ts,ts.get_rect(center=(x+card_w//2,sy+140)))

            spd_map={28:"Dosen Lambat",24:"Dosen Pelan",20:"Sedang",
                     16:"Dosen Cepat",13:"Sangat Cepat",14:"Cepat"}
            spd_str=spd_map.get(d["ai_speed"],f"AI:{d['ai_speed']}")
            sp_s=self.fxs.render(spd_str,True,C_MUTED)
            self.screen.blit(sp_s,sp_s.get_rect(center=(x+card_w//2,sy+162)))

            if hov:
                btn_rect = pygame.Rect(x + card_w//2 - 50, sy + card_h - 50, 100, 36)
                draw_rr(self.screen,C_BUTTON_HOV,btn_rect,10)
                draw_rr(self.screen,(200,200,255),btn_rect,10,2)
                draw_btn_content(self.screen, btn_rect, PLAY_ICON, 16, "MAIN", self.fmd, (255,255,255), gap=6)

        back_rect=pygame.Rect(cx-120,sy+card_h+28,240,48)
        self.ls_back_rect=back_rect
        hov_b=back_rect.collidepoint(self.mouse_pos)
        draw_rr(self.screen,C_BUTTON_HOV if hov_b else C_BUTTON_BG,back_rect,12)
        draw_rr(self.screen,C_TEXT_BOLD,back_rect,12,2)
        draw_btn_content(self.screen, back_rect, BACK_ICON, 20, "Kembali", self.flg, C_TEXT, gap=8)

        note_text = "Nyawa +1 tiap selesaikan semester (maks. 9)  |  Namamu masuk Leaderboard!"
        try:
            warning_img = pygame.image.load(IDEA_ICON).convert_alpha()
            warning_img = pygame.transform.smoothscale(warning_img, (18,18))
            note = self.fxs.render(note_text, True, C_MUTED)
            total_w2 = warning_img.get_width() + 8 + note.get_width()
            start_x2 = cx - total_w2//2
            ny = sy + card_h + 92
            self.screen.blit(warning_img, (start_x2, ny-1))
            self.screen.blit(note, (start_x2 + 26, ny))
        except:
            note=self.fxs.render(note_text, True, C_MUTED)
            self.screen.blit(note, note.get_rect(center=(cx,sy+card_h+92)))

    # ═══════════════════════════════════════════
    # DRAW: LEVEL CONFIRM
    # ═══════════════════════════════════════════
    def _draw_level_confirm(self):
        surf=pygame.Surface((self.SW,self.SH),pygame.SRCALPHA)
        surf.fill((0,0,0,170))
        self.screen.blit(surf,(0,0))
        cx=self.SW//2; cy=self.SH//2
        box_w,box_h=560,490
        bx=cx-box_w//2; by=cy-box_h//2
        pygame.draw.rect(self.screen,(25,25,55),(bx,by,box_w,box_h),border_radius=16)
        pygame.draw.rect(self.screen,C_GOLD,(bx,by,box_w,box_h),3,border_radius=16)
        y=by+22

        try:
            level_img = pygame.image.load(STAR_ICON).convert_alpha()
            level_img = pygame.transform.smoothscale(level_img, (38,38))
            self.screen.blit(level_img, level_img.get_rect(center=(cx-140, y+19)))
            self.screen.blit(level_img, level_img.get_rect(center=(cx+140, y+19)))
        except:
            pass
        title=self.fxl.render("LEVEL CLEAR!", True, C_GOLD)
        self.screen.blit(title, title.get_rect(center=(cx, y+19)))
        y += 50

        prev=self._confirm_prev_diff
        nxt=self._confirm_next_diff

        col_label_x = bx + 30
        col_val_x   = bx + box_w - 30

        def row(label, val, col=C_TEXT):
            nonlocal y
            lbl_s = self.fmd.render(label, True, C_MUTED)
            val_s = self.fmd.render(str(val), True, col)
            self.screen.blit(lbl_s, (col_label_x, y))
            self.screen.blit(val_s, val_s.get_rect(right=col_val_x, top=y))
            y += 27

        hdr=self.fsm.render("— Hasil Belajarmu —",True,C_CYAN)
        self.screen.blit(hdr,hdr.get_rect(centerx=cx,top=y)); y+=25
        row("Semester Selesai", prev["label"])
        row("Tugas Dikumpulkan", f"{self.dots_eaten:,}")
        row("Total Nilai", f"{self.score:,}", C_GOLD)

        if self._confirm_life_gained:
            lbl_s = self.fmd.render("Nyawa Bonus", True, C_MUTED)
            val_s = self.fmd.render("+1", True, (255,120,150))
            self.screen.blit(lbl_s, (col_label_x, y))
            self.screen.blit(val_s, val_s.get_rect(right=col_val_x, top=y))
            try:
                heart_img = pygame.image.load(HEART_ICON).convert_alpha()
                heart_img = pygame.transform.smoothscale(heart_img, (18,18))
                hx_pos = col_val_x - val_s.get_width() - 24
                self.screen.blit(heart_img, (hx_pos, y + 2))
            except:
                pass
            y += 27

        lives_val = self._confirm_next_lives
        lbl_s = self.fmd.render("Nyawa Tersisa", True, C_MUTED)
        self.screen.blit(lbl_s, (col_label_x, y))
        try:
            heart_img = pygame.image.load(HEART_ICON).convert_alpha()
            heart_img = pygame.transform.smoothscale(heart_img, (18,18))
            hearts_w = lives_val * 22 - 2
            hx_start = col_val_x - hearts_w
            for i in range(lives_val):
                self.screen.blit(heart_img, (hx_start + i*22, y + 2))
        except:
            val_s = self.fmd.render(str(lives_val), True, (255,100,100))
            self.screen.blit(val_s, val_s.get_rect(right=col_val_x, top=y))
        y += 30

        pygame.draw.line(self.screen, C_LINE, (bx+20,y), (bx+box_w-20,y), 1)
        y += 12

        hdr2=self.fsm.render("— Semester Berikutnya —",True,(255,180,80))
        self.screen.blit(hdr2,hdr2.get_rect(centerx=cx,top=y)); y+=25
        row("Ukuran Labirin", nxt["desc"].split("•")[0].strip())
        row("Jumlah Dosen", f"{nxt['num_ghosts']} dosen")
        spd=nxt["ai_speed"]
        if spd>=25: spd_lbl="Santai"
        elif spd>=18: spd_lbl="Normal"
        elif spd>=13: spd_lbl="Cepat"
        else: spd_lbl="Panik!"
        spd_col=C_GREEN if spd>=25 else (C_GOLD if spd>=18 else C_RED)
        row("Kecepatan Dosen", spd_lbl, spd_col)
        tmr=nxt["maze_timer"]
        row("Timer Labirin", f"{tmr}s" if tmr>0 else "OFF",
            C_GREEN if tmr==0 else (C_GOLD if tmr>=20 else C_RED))

        btn_w,btn_h=220,48
        btn_y=by+box_h-btn_h-20
        cont_rect=pygame.Rect(cx-btn_w-16, btn_y, btn_w, btn_h)
        mx2,my2=pygame.mouse.get_pos()
        hov_cont=cont_rect.collidepoint(mx2,my2)
        draw_rr(self.screen,C_BUTTON_HOV if hov_cont else C_BUTTON_BG,cont_rect,10)
        draw_rr(self.screen,C_GOLD,cont_rect,10,2)
        draw_btn_content(self.screen, cont_rect, PLAY_ICON, 20, "LANJUT", self.fmd, C_GOLD, gap=8)

        quit_rect=pygame.Rect(cx+16, btn_y, btn_w, btn_h)
        hov_quit=quit_rect.collidepoint(mx2,my2)
        draw_rr(self.screen,(80,30,30) if hov_quit else (50,20,20),quit_rect,10)
        draw_rr(self.screen,C_RED,quit_rect,10,2)
        draw_btn_content(self.screen, quit_rect, CANCEL_ICON, 20, "KEMBALI KE MENU", self.fsm, C_RED, gap=8)

        self._lc_cont_rect=cont_rect
        self._lc_quit_rect=quit_rect

    # ═══════════════════════════════════════════
    # DRAW: MAZE
    # ═══════════════════════════════════════════
    def _draw_maze(self):
        pygame.draw.rect(self.screen,C_FLOOR,
                        (self.MAZE_X-20,self.MAZE_Y-20,self.MAZE_W+40,self.MAZE_H+40))
        cell=self.CELL
        is_unlim=(self.level=="unlimited")
        is_trial=(self.level=="trial")
        if is_trial:
            draw_rr(self.screen,C_TRIAL_BDR,
                   (self.MAZE_X-4,self.MAZE_Y-4,self.MAZE_W+8,self.MAZE_H+8),6,3)
        if is_unlim:
            t2=pygame.time.get_ticks()
            pulse=int(127+127*math.sin(t2*0.003))
            pygame.draw.rect(self.screen,(pulse,0,pulse//2),
                            (self.MAZE_X-4,self.MAZE_Y-4,self.MAZE_W+8,self.MAZE_H+8),3,
                            border_radius=6)
        if self.maze_flash>0:
            fs=pygame.Surface((self.MAZE_W,self.MAZE_H),pygame.SRCALPHA)
            alpha=int(self.maze_flash/40*150)
            fs.fill((255,200,0,alpha) if self.maze_flash>20 else (100,200,255,alpha))
            self.screen.blit(fs,(self.MAZE_X,self.MAZE_Y))
            self.maze_flash-=1

        for y in range(self.rows):
            for x in range(self.cols):
                rx=self.MAZE_X+x*cell; ry=self.MAZE_Y+y*cell
                if self.maze[y,x]==1:
                    draw_rr(self.screen,C_WALL,(rx+2,ry+2,cell-4,cell-4),4)
                    draw_rr(self.screen,C_WALL_EDGE,(rx+2,ry+2,cell-4,cell-4),4,2)
                else:
                    h=self.heat[y,x]
                    if h>2:
                        hs2=pygame.Surface((cell,cell),pygame.SRCALPHA)
                        hs2.fill((180,60,255,min(int(h*12),100)))
                        self.screen.blit(hs2,(rx,ry))

        for dx2,dy2 in self.dots:
            cx3=self.MAZE_X+dx2*cell+cell//2; cy3=self.MAZE_Y+dy2*cell+cell//2
            pygame.draw.circle(self.screen,C_DOT,(cx3,cy3),max(3,cell//6))
            pygame.draw.circle(self.screen,C_GOLD,(cx3,cy3),max(1,cell//12),1)

        for gh in self.ghosts:
            col=GHOST_COLS[gh.id]
            for tx,ty in gh.trail:
                ts2=pygame.Surface((cell//2,cell//2),pygame.SRCALPHA)
                ts2.fill((*col,35))
                self.screen.blit(ts2,(self.MAZE_X+tx*cell,self.MAZE_Y+ty*cell))

        for gh in self.ghosts:
            col=GHOST_COLS[gh.id]
            cx3=self.MAZE_X+gh.x*cell+cell//2; cy3=self.MAZE_Y+gh.y*cell+cell//2
            r=cell//2-1
            lbl=self.fxs.render(GHOST_LABELS[gh.id],True,col)
            self.screen.blit(lbl,lbl.get_rect(center=(cx3,cy3-r-18)))
            draw_ghost(self.screen,col,cx3,cy3,r)

        px=self.MAZE_X+self.player[0]*cell+cell//2
        py=self.MAZE_Y+self.player[1]*cell+cell//2
        draw_avatar(self.screen,AVATARS[self.selected_avatar],px,py,
                   cell//2-1,self.anim_frame,self.player_dir)

        for a in self.score_anims[:]:
            a.draw(self.screen,self.fxs,cell)
            if not a.alive: self.score_anims.remove(a)

        if self._powerup_on_floor:
            fx,fy,ftype=self._powerup_on_floor
            meta=self._POWERUP_META[ftype]
            age_ms=pygame.time.get_ticks()-self._powerup_spawn_ms
            blink=(age_ms>7000 and (pygame.time.get_ticks()//200)%2==0)
            if not blink:
                pcx=self.MAZE_X+fx*cell+cell//2; pcy=self.MAZE_Y+fy*cell+cell//2
                pulse=int(180+75*math.sin(pygame.time.get_ticks()*0.005))
                ps=pygame.Surface((cell,cell),pygame.SRCALPHA)
                pygame.draw.circle(ps,(*meta["color"],pulse),(cell//2,cell//2),cell//2-2)
                self.screen.blit(ps,(self.MAZE_X+fx*cell,self.MAZE_Y+fy*cell))
                try:
                    icon_img = pygame.image.load(meta["icon"]).convert_alpha()
                    icon_img = pygame.transform.smoothscale(icon_img, (24, 24))
                    self.screen.blit(icon_img, icon_img.get_rect(center=(pcx, pcy)))
                except:
                    it=self.fxs.render("?",True,(255,255,255))
                    self.screen.blit(it,it.get_rect(center=(pcx,pcy)))

        if self._powerup_active:
            pa=self._powerup_active
            meta=self._POWERUP_META[pa["type"]]
            total_f=meta["duration"]; rem=pa["frames"]
            ratio=rem/total_f if total_f>0 else 0
            bw=self.MAZE_W; bh=10; bx2=self.MAZE_X; by2=self.MAZE_Y-18
            pygame.draw.rect(self.screen,(40,35,60),(bx2,by2,bw,bh),border_radius=5)
            pygame.draw.rect(self.screen,meta["color"],(bx2,by2,int(bw*ratio),bh),border_radius=5)
            pygame.draw.rect(self.screen,(180,180,180),(bx2,by2,bw,bh),1,border_radius=5)
            try:
                icon_img = pygame.image.load(meta["icon"]).convert_alpha()
                icon_img = pygame.transform.smoothscale(icon_img, (22, 22))
                icon_rect = icon_img.get_rect(midleft=(bx2, by2-14))
                self.screen.blit(icon_img, icon_rect)
                pt = self.fsm.render(f"{meta['label']} ({rem//60}s)", True, meta["color"])
                self.screen.blit(pt, (icon_rect.right + 8, by2 - 24))
            except:
                pt=self.fsm.render(f"{meta['label']} ({rem//60}s)", True, meta["color"])
                self.screen.blit(pt, pt.get_rect(midleft=(bx2,by2-14)))

        if self.maze_timer_max>0 and self.dots and not self.paused:
            secs_left=self.maze_timer
            total=self.maze_timer_max
            ratio_t=secs_left/total if total>0 else 0
            if ratio_t>0.5:   fill_col=(255,180,40)
            elif ratio_t>0.2: fill_col=(255,120,20)
            else:              fill_col=(255,50,50)

            sw_w=190; sw_h=42
            sw_x=self.MAZE_X
            sw_y=self.MAZE_Y-sw_h-14

            draw_rr(self.screen,(20,18,50),(sw_x,sw_y,sw_w,sw_h),10)
            fill_w=max(0,int((sw_w-4)*ratio_t))
            draw_rr(self.screen,fill_col,(sw_x+2,sw_y+2,fill_w,sw_h-4),8)
            draw_rr(self.screen,fill_col,(sw_x,sw_y,sw_w,sw_h),10,2)

            try:
                timer_img = pygame.image.load(TIMER_ICON).convert_alpha()
                timer_img = pygame.transform.smoothscale(timer_img, (22,22))
                timer_rect = timer_img.get_rect(midleft=(sw_x+8, sw_y+sw_h//2))
                self.screen.blit(timer_img, timer_rect)
                sw_lbl=self.fmd.render(f"{secs_left}s", True, (255,255,255))
                self.screen.blit(sw_lbl, sw_lbl.get_rect(midleft=(timer_rect.right+6, sw_y+sw_h//2)))
            except:
                sw_lbl=self.fmd.render(f"{secs_left}s", True, (255,255,255))
                self.screen.blit(sw_lbl, sw_lbl.get_rect(midleft=(sw_x+10, sw_y+sw_h//2)))

            sw_sub=self.fxs.render("Maze berubah", True, (210,210,210))
            self.screen.blit(sw_sub, sw_sub.get_rect(midright=(sw_x+sw_w-8, sw_y+sw_h//2)))

            if secs_left<=5:
                pulse2=int(pygame.time.get_ticks()/200)%2
                col3=C_RED if pulse2 else C_GOLD
                try:
                    warning_img = pygame.image.load(ATTENTION_ICON).convert_alpha()
                    warning_img = pygame.transform.smoothscale(warning_img, (28,28))
                    wy = self.MAZE_Y-sw_h-20
                    self.screen.blit(warning_img, (self.MAZE_X, wy-14))
                    wt=self.flg.render(f"LABIRIN BERUBAH DALAM {secs_left}s!", True, col3)
                    self.screen.blit(wt, (self.MAZE_X+40, wy-6))
                except:
                    wt=self.flg.render(f"LABIRIN BERUBAH DALAM {secs_left}s!", True, col3)
                    self.screen.blit(wt, wt.get_rect(midleft=(self.MAZE_X,self.MAZE_Y-sw_h-20)))

        if self._level_clear_timer>0:
            alpha=min(255,self._level_clear_timer*4)
            d=self._diff()
            msg=self.fxl.render(f"{self._level_clear_msg} SELESAI! +{d['level_bonus']} Poin", True, C_GREEN)
            msg.set_alpha(alpha)
            msg_rect = msg.get_rect(center=(self.SW//2,self.MAZE_Y+self.MAZE_H//2))
            try:
                check_img = pygame.image.load(CHECK_ICON).convert_alpha()
                check_img = pygame.transform.smoothscale(check_img, (34,34))
                self.screen.blit(check_img, (msg_rect.x-42, msg_rect.y+2))
            except:
                pass
            self.screen.blit(msg,msg_rect)
            self._level_clear_timer-=1

        if self._life_bonus_timer>0:
            alpha2=min(255,self._life_bonus_timer*4)
            lm=self.fxl.render("+1 NYAWA!", True, (255,100,150))
            lm.set_alpha(alpha2)
            lm_rect = lm.get_rect(center=(self.SW//2,self.MAZE_Y+self.MAZE_H//2+55))
            try:
                heart_img = pygame.image.load(HEART_ICON).convert_alpha()
                heart_img = pygame.transform.smoothscale(heart_img, (30,30))
                self.screen.blit(heart_img, (lm_rect.x-40, lm_rect.y+3))
            except:
                pass
            self.screen.blit(lm,lm_rect)
            self._life_bonus_timer-=1

    # ═══════════════════════════════════════════
    # DRAW: PANEL
    # ═══════════════════════════════════════════
    def _draw_panel(self):
        px0=self.SW-PANEL_W
        pygame.draw.rect(self.screen,C_PANEL,(px0,TITLEBAR_H,PANEL_W,self.SH-TITLEBAR_H))
        draw_rr(self.screen,C_LINE,(px0,TITLEBAR_H,PANEL_W,self.SH-TITLEBAR_H),0,3)
        d=self._diff(); col=d["color"]
        lbl=self.fxl.render(d["label"],True,col)
        self.screen.blit(lbl,(px0+20,TITLEBAR_H+10))
        if self.level=="trial":
            h=self.fxs.render("Mode latihan — timer OFF",True,C_TRIAL_BDR)
            self.screen.blit(h,(px0+20,TITLEBAR_H+48))
        if self.level=="unlimited":
            h=self.fxs.render(f"Sub #{self.unlimited_sub} • 4 Dosen • Labirin Dinamis",True,C_UNLIM)
            self.screen.blit(h,(px0+20,TITLEBAR_H+48))
        if self.paused:
            pb=pygame.Surface((PANEL_W-40,34),pygame.SRCALPHA)
            pb.fill((255,0,0,150))
            self.screen.blit(pb,(px0+20,TITLEBAR_H+62))
            try:
                pause_img = pygame.image.load(PAUSE_ICON).convert_alpha()
                pause_img = pygame.transform.smoothscale(pause_img, (18,18))
                self.screen.blit(pause_img, (px0+28, TITLEBAR_H+66))
                paused_text = self.fmd.render("PAUSED", True, C_TEXT)
                self.screen.blit(paused_text, (px0+52, TITLEBAR_H+67))
            except:
                self.screen.blit(self.fmd.render("PAUSED",True,C_TEXT),(px0+25,TITLEBAR_H+68))

        av=AVATARS[self.selected_avatar]; avy=TITLEBAR_H+100
        draw_avatar_preview(self.screen,av,px0+28,avy+14,14)
        self.screen.blit(self.fsm.render(f"Avatar: {av['name']}",True,av["color"]),(px0+50,avy+6))
        ab=pygame.Rect(px0+50,avy+22,PANEL_W-80,20)
        draw_rr(self.screen,C_BUTTON_HOV if ab.collidepoint(self.mouse_pos) else C_BUTTON_BG,ab,4)
        self.screen.blit(self.fxs.render("Ganti Avatar",True,C_TEXT),(ab.x+10,ab.y+3))
        self.av_change_rect=ab

        stats=[
            ("SCORE", f"{self.score:,}", C_GOLD),
            ("LEVEL", d["label"], col),
            ("NYAWA", None, C_RED),
            ("TUGAS", f"{self.dots_eaten}/{self.total_dots}", C_TEXT_BOLD),
            ("DOSEN", str(len(self.ghosts)), C_MUTED),
        ]
        yo=TITLEBAR_H+142
        for i,(lbl2,val,vc) in enumerate(stats):
            y = yo + i*36
            if lbl2 == "NYAWA":
                try:
                    heart_img = pygame.image.load(HEART_ICON).convert_alpha()
                    heart_img = pygame.transform.smoothscale(heart_img, (16,16))
                    hx = px0 + 30
                    hy = y + 2
                    for h in range(self.lives):
                        self.screen.blit(heart_img, (hx + h*19, hy))
                    for h in range(MAX_LIVES - self.lives):
                        empty = heart_img.copy()
                        empty.set_alpha(45)
                        self.screen.blit(empty, (hx + (self.lives+h)*19, hy))
                except:
                    vs=self.flg.render(f"{self.lives}/{MAX_LIVES}", True, vc)
                    self.screen.blit(vs, (px0+30, y))
            else:
                vs=self.flg.render(val, True, vc)
                self.screen.blit(vs, (px0+30, y))
            self.screen.blit(self.fsm.render(lbl2,True,C_MUTED),(px0+30,y+24))

        gy=yo+len(stats)*36+12
        self.screen.blit(self.fsm.render("DOSEN AI:",True,C_TEXT_BOLD),(px0+20,gy))
        for i,gh in enumerate(self.ghosts):
            gc=GHOST_COLS[gh.id]
            gs=self.fxs.render(f"  {GHOST_NAMES[gh.id]}",True,gc)
            self.screen.blit(gs,(px0+25,gy+22+i*18))

        by3=gy+22+len(self.ghosts)*18+12
        draw_rr(self.screen,C_BAR_BG,(px0+20,by3,PANEL_W-40,22),11)
        dp=(self.dots_eaten/self.total_dots) if self.total_dots else 0
        draw_rr(self.screen,C_BAR_FILL,(px0+20,by3,int((PANEL_W-40)*dp),22),11)
        self.screen.blit(self.fxs.render("Progress Tugas",True,C_TEXT),(px0+25,by3+26))

        lby=by3+52
        self.screen.blit(self.fsm.render("TOP 5 SCORES",True,C_GOLD),(px0+20,lby))
        for i,e in enumerate(self.lb[:5]):
            lbl3=e.get("level_label",str(e.get("level","?")))
            name_str=e.get("name","")
            if name_str:
                rt=f"{i+1}. {e['score']:,}  [{name_str}]"
            else:
                rt=f"{i+1}. {e['score']:,}  ({lbl3})"
            self.screen.blit(self.fxs.render(rt,True,C_TEXT if i>0 else C_GOLD),(px0+20,lby+24+i*18))

        pu_y=lby+24+5*18+14
        self.screen.blit(self.fsm.render("POWERUP",True,C_GOLD),(px0+20,pu_y))
        if self._powerup_active:
            pa=self._powerup_active; meta=self._POWERUP_META[pa["type"]]
            pt=self.fxs.render(f"{meta['label']} — {pa['frames']//60}s",True,meta["color"])
            self.screen.blit(pt,(px0+20,pu_y+18))
        elif self._powerup_on_floor:
            _,_,ftype=self._powerup_on_floor
            meta=self._POWERUP_META[ftype]
            blink=(pygame.time.get_ticks()//400)%2==0
            pc=meta["color"] if blink else C_MUTED
            pt=self.fxs.render(f"^ {meta['label']} di lantai!",True,pc)
            self.screen.blit(pt,(px0+20,pu_y+18))
        else:
            secs=self._powerup_timer
            pt=self.fxs.render(f"Muncul dalam {secs}s",True,C_MUTED)
            self.screen.blit(pt,(px0+20,pu_y+18))

    def _btn(self,x,y,w,h,text,hover=False,color=None,border=None,text_color=None):
        bg=C_BUTTON_HOV if hover else (color or C_BUTTON_BG)
        draw_rr(self.screen,bg,(x,y,w,h),15)
        draw_rr(self.screen,border or C_TEXT_BOLD,(x,y,w,h),15,4)
        ts=self.fxl.render(text,True,text_color or C_TEXT)
        self.screen.blit(ts,ts.get_rect(center=(x+w//2,y+h//2)))
        return pygame.Rect(x,y,w,h)

    # ═══════════════════════════════════════════
    # DRAW: GAME OVER
    # ═══════════════════════════════════════════
    def _draw_game_over_overlay(self):
        ov=pygame.Surface((self.SW,self.SH-TITLEBAR_H),pygame.SRCALPHA)
        ov.fill((0,0,0,200)); self.screen.blit(ov,(0,TITLEBAR_H))
        cx=self.SW//2; cy=TITLEBAR_H+(self.SH-TITLEBAR_H)//2
        s=self.fxxl.render(self.msg_title,True,C_RED)
        self.screen.blit(s,s.get_rect(center=(cx,cy-100)))
        words=self.msg_sub.split(); lines=[]; cur=[]
        for w in words:
            test=' '.join(cur+[w])
            if self.flg.size(test)[0]<self.SW*0.7: cur.append(w)
            else: lines.append(' '.join(cur)); cur=[w]
        if cur: lines.append(' '.join(cur))
        for i,line in enumerate(lines):
            ls=self.flg.render(line,True,C_TEXT_BOLD)
            self.screen.blit(ls,ls.get_rect(center=(cx,cy-20+i*50)))

        btn_w, btn_h = 320, 72
        btn_x = cx - btn_w // 2
        btn_y = cy + 120
        retry_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        self.retry_button_rect = retry_rect
        hov = retry_rect.collidepoint(self.mouse_pos)
        draw_rr(self.screen, C_BUTTON_HOV if hov else C_BUTTON_BG, retry_rect, 15)
        draw_rr(self.screen, C_TEXT_BOLD, retry_rect, 15, 4)
        draw_btn_content(self.screen, retry_rect, REPLAY_ICON, 26, "MAIN LAGI", self.fxl, C_TEXT, gap=10)

        lslink=pygame.Rect(cx-150,btn_y+btn_h+18,300,45); self.go_ls_rect=lslink
        draw_rr(self.screen,(40,35,80) if not lslink.collidepoint(self.mouse_pos) else (60,50,110),lslink,8)
        draw_btn_content(self.screen, lslink, BILL_ICON, 22, "Pilih Semester Lain", self.fmd, C_CYAN, gap=8)

    # ═══════════════════════════════════════════
    # DRAW: PAUSED OVERLAY
    # ═══════════════════════════════════════════
    def _draw_paused_overlay(self):
        ov=pygame.Surface((self.SW,self.SH),pygame.SRCALPHA)
        ov.fill((0,0,0,185)); self.screen.blit(ov,(0,0))
        cx=self.SW//2; cy=self.SH//2
        pw,ph=520,320; pr=pygame.Rect(cx-pw//2,cy-ph//2,pw,ph)
        draw_rr(self.screen,(18,18,50),pr,22)
        draw_rr(self.screen,C_CYAN,pr,22,3)

        try:
            pause_img = pygame.image.load(PAUSE_ICON).convert_alpha()
            pause_img = pygame.transform.smoothscale(pause_img, (42, 42))
            self.screen.blit(pause_img, pause_img.get_rect(center=(cx, cy-105)))
        except:
            icon_t=self.fxxl.render("||",True,C_CYAN)
            self.screen.blit(icon_t,icon_t.get_rect(center=(cx,cy-105)))

        title=self.fxl.render("Istirahat Sebentar",True,C_TEXT_BOLD)
        self.screen.blit(title,title.get_rect(center=(cx,cy-60)))
        pygame.draw.line(self.screen,C_LINE,(cx-180,cy-28),(cx+180,cy-28),1)

        d=self._diff()
        info_text=self.fmd.render(
            f"Nilai: {self.score:,}   |   {d['label']}",
            True, C_GOLD
        )
        self.screen.blit(info_text, info_text.get_rect(center=(cx, cy-2)))

        try:
            heart_img = pygame.image.load(HEART_ICON).convert_alpha()
            heart_img = pygame.transform.smoothscale(heart_img, (22,22))
            hearts_total_w = self.lives * 26 - 4
            hx_start = cx - hearts_total_w // 2
            for i in range(self.lives):
                self.screen.blit(heart_img, (hx_start + i*26, cy+24))
            for i in range(MAX_LIVES - self.lives):
                empty = heart_img.copy(); empty.set_alpha(50)
                self.screen.blit(empty, (hx_start + (self.lives+i)*26, cy+24))
        except:
            lives_t = self.fmd.render(f"Nyawa: {self.lives}", True, C_RED)
            self.screen.blit(lives_t, lives_t.get_rect(center=(cx, cy+28)))

        btn_w,btn_h=300,60; bx=cx-btn_w//2; by2=cy+60
        self._pause_resume_rect=pygame.Rect(bx,by2,btn_w,btn_h)
        hov=self._pause_resume_rect.collidepoint(self.mouse_pos)
        draw_rr(self.screen,(40,120,75) if not hov else (55,165,100),self._pause_resume_rect,16)
        draw_rr(self.screen,C_GREEN,self._pause_resume_rect,16,3)
        draw_btn_content(self.screen, self._pause_resume_rect, RESUME_ICON, 24,
                         "Lanjutkan", self.flg, (255,255,255), gap=10)

        hint=self.fxs.render("P = Lanjutkan  |  ESC = Keluar ke pilihan semester",True,C_MUTED)
        self.screen.blit(hint,hint.get_rect(center=(cx,by2+btn_h+18)))

    def _draw_esc_confirm(self):
        ov=pygame.Surface((self.SW,self.SH),pygame.SRCALPHA)
        ov.fill((0,0,0,210)); self.screen.blit(ov,(0,0))
        cx=self.SW//2; cy=self.SH//2
        pw,ph=500,280; pr=pygame.Rect(cx-pw//2,cy-ph//2,pw,ph)
        draw_rr(self.screen,(28,22,65),pr,20)
        draw_rr(self.screen,C_RED,pr,20,3)

        try:
            warning_img = pygame.image.load(ATTENTION_ICON).convert_alpha()
            warning_img = pygame.transform.smoothscale(warning_img, (30,30))
            icon_rect = warning_img.get_rect(center=(cx-145, cy-80))
            self.screen.blit(warning_img, icon_rect)
            t1=self.fxl.render("Menyerah dari Deadline?", True, C_RED)
            self.screen.blit(t1, t1.get_rect(midleft=(icon_rect.right+10, cy-80)))
        except:
            t1=self.fxl.render("Menyerah dari Deadline?", True, C_RED)
            self.screen.blit(t1, t1.get_rect(center=(cx,cy-80)))

        t2=self.fmd.render("Progress semester ini akan hilang.",True,C_MUTED)
        self.screen.blit(t2,t2.get_rect(center=(cx,cy-30)))

        yr=pygame.Rect(cx-220,cy+20,200,65); self._esc_yes_rect=yr
        hy=yr.collidepoint(self.mouse_pos)
        draw_rr(self.screen,(160,35,35) if hy else (110,25,25),yr,14)
        draw_rr(self.screen,C_RED,yr,14,3)
        draw_btn_content(self.screen, yr, CHECK_ICON, 22, "Ya, Menyerah", self.flg, (255,255,255), gap=8)

        nr=pygame.Rect(cx+20,cy+20,200,65); self._esc_no_rect=nr
        hn=nr.collidepoint(self.mouse_pos)
        draw_rr(self.screen,(35,110,40) if hn else (25,75,30),nr,14)
        draw_rr(self.screen,C_GREEN,nr,14,3)
        draw_btn_content(self.screen, nr, CANCEL_ICON, 22, "Terus Berjuang!", self.flg, (255,255,255), gap=8)

        hint=self.fxs.render("Klik tombol untuk memilih",True,C_MUTED)
        self.screen.blit(hint,hint.get_rect(center=(cx,cy+110)))

    def _draw_countdown(self,remaining):
        ov=pygame.Surface((self.SW,self.SH),pygame.SRCALPHA)
        ov.fill((0,0,0,160)); self.screen.blit(ov,(0,0))
        cx=self.SW//2; cy=self.SH//2
        labels={3:"Bersedia...",2:"Siap-siap...",1:"Mulaiii!"}
        label=labels.get(remaining,"Mulaiii!")
        elapsed_in_sec=(pygame.time.get_ticks()-self._countdown_ms)%1000
        scale=1.0+0.22*(1-elapsed_in_sec/1000)
        r=int(75*scale)
        col_map={3:(255,180,50),2:(50,200,255),1:(80,255,130)}
        col=col_map.get(remaining,C_GOLD)
        pygame.draw.circle(self.screen,col,(cx,cy),r,5)
        ct=self.fxxl.render(str(remaining),True,col)
        self.screen.blit(ct,ct.get_rect(center=(cx,cy)))
        st = self.flg.render(label, True, C_TEXT_BOLD)
        text_rect = st.get_rect(center=(cx, cy+100))
        self.screen.blit(st, text_rect)
        if remaining == 1:
            try:
                rocket_img = pygame.image.load(ROCKET_ICON).convert_alpha()
                rocket_img = pygame.transform.smoothscale(rocket_img, (32, 32))
                rocket_rect = rocket_img.get_rect(midleft=(text_rect.right + 10, text_rect.centery))
                self.screen.blit(rocket_img, rocket_rect)
            except:
                pass

    # ═══════════════════════════════════════════
    # MAIN LOOP
    # ═══════════════════════════════════════════
    def run(self):
        clock=pygame.time.Clock()
        KEY_DIR={pygame.K_UP:(0,-1),pygame.K_w:(0,-1),
                 pygame.K_DOWN:(0,1),pygame.K_s:(0,1),
                 pygame.K_LEFT:(-1,0),pygame.K_a:(-1,0),
                 pygame.K_RIGHT:(1,0),pygame.K_d:(1,0)}
        while True:
            now_ms=pygame.time.get_ticks()
            self.mouse_pos=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    mx,my=event.pos
                    if self.state not in ("splash","login","level_select"):
                        if my<TITLEBAR_H:
                            if hasattr(self,'close_rect') and self.close_rect.collidepoint(mx,my):
                                pygame.quit(); sys.exit()
                            elif hasattr(self,'minimize_rect') and self.minimize_rect.collidepoint(mx,my):
                                pygame.display.iconify()
                            continue

                    if self.state=="splash":
                        self.state="login"; continue

                    if self.show_avatar_menu:
                        for i,r in enumerate(self.avatar_rects):
                            if r.collidepoint(mx,my): self.selected_avatar=i
                        if hasattr(self,'avatar_close_rect') and self.avatar_close_rect.collidepoint(mx,my):
                            self.show_avatar_menu=False
                            if self.state=="playing": self.paused=False
                    elif self.state=="level_select":
                        if hasattr(self,'ls_back_rect') and self.ls_back_rect.collidepoint(mx,my):
                            self.state="login"
                        else:
                            for lv,rect in self.level_card_rects:
                                if rect.collidepoint(mx,my):
                                    self.score=0; self.lives=5; self.total_dots_eaten_run=0
                                    self.level=lv
                                    if lv=="unlimited": self.unlimited_sub=1
                                    self.start_level=lv
                                    self._init_round(); self._setup_layout()
                                    self.state="countdown"
                                    self._countdown_ms=pygame.time.get_ticks()
                                    self._countdown_dest="playing"
                                    break
                    elif self.state=="esc_confirm":
                        if self._esc_yes_rect and self._esc_yes_rect.collidepoint(mx,my):
                            self.state="level_select"; self.paused=False
                        elif self._esc_no_rect and self._esc_no_rect.collidepoint(mx,my):
                            self.paused=True
                            self.state="countdown"
                            self._countdown_ms=pygame.time.get_ticks()
                            self._countdown_dest="playing"
                    elif self.state=="level_confirm":
                        if self._lc_cont_rect and self._lc_cont_rect.collidepoint(mx,my):
                            self._apply_next_level()
                        elif self._lc_quit_rect and self._lc_quit_rect.collidepoint(mx,my):
                            self.state="level_select"; self.paused=False
                    elif self.state=="login":
                        if hasattr(self,'_login_av_rects'):
                            for i,r in enumerate(self._login_av_rects):
                                if r.collidepoint(mx,my): self.selected_avatar=i
                        if self._login_start_rect and self._login_start_rect.collidepoint(mx,my):
                            if self.player_name.strip(): self.state="level_select"
                        if self._login_input_rect and self._login_input_rect.collidepoint(mx,my):
                            self._name_active=True
                        if self._login_exit_rect and self._login_exit_rect.collidepoint(mx,my):
                            pygame.quit(); sys.exit()
                    elif self.state=="paused":
                        if hasattr(self,'_pause_resume_rect') and self._pause_resume_rect and self._pause_resume_rect.collidepoint(mx,my):
                            self.state="countdown"
                            self._countdown_ms=pygame.time.get_ticks()
                            self._countdown_dest="playing"
                    elif self.state in ("playing","countdown"):
                        if hasattr(self,'av_change_rect') and self.av_change_rect.collidepoint(mx,my):
                            self.show_avatar_menu=True; self.paused=True
                    elif self.state=="game_over":
                        if hasattr(self,'retry_button_rect') and self.retry_button_rect and self.retry_button_rect.collidepoint(mx,my):
                            self.score=0; self.lives=5; self.total_dots_eaten_run=0
                            self.level=self.start_level
                            if self.level=="unlimited": self.unlimited_sub=1
                            self._init_round(); self._setup_layout()
                            self.state="countdown"
                            self._countdown_ms=pygame.time.get_ticks()
                            self._countdown_dest="playing"
                        elif hasattr(self,'go_ls_rect') and self.go_ls_rect.collidepoint(mx,my):
                            self.state="level_select"

                if event.type==pygame.KEYDOWN:
                    if self.state=="splash":
                        if event.key in (pygame.K_RETURN,pygame.K_SPACE,pygame.K_ESCAPE):
                            self.state="login"
                        continue

                    if self.state=="login":
                        if event.key==pygame.K_BACKSPACE:
                            self.player_name=self.player_name[:-1]
                        elif event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                            if self.player_name.strip(): self.state="level_select"
                        elif len(self.player_name)<18:
                            ch=event.unicode
                            if ch.isprintable() and ch!="": self.player_name+=ch
                        continue

                    if event.key==pygame.K_ESCAPE:
                        if self.show_avatar_menu:
                            self.show_avatar_menu=False
                            if self.state=="playing": self.paused=False
                        elif self.state=="level_select": self.state="login"
                        elif self.state=="esc_confirm": pass
                        elif self.state in ("playing","paused"):
                            self.state="esc_confirm"; self.paused=True
                        elif self.state=="countdown": pass
                        else: pygame.quit(); sys.exit()
                    if event.key==pygame.K_p and not self.show_avatar_menu:
                        if self.state=="playing" and not self.paused:
                            self.paused=True; self.state="paused"
                        elif self.state=="paused":
                            self.state="countdown"
                            self._countdown_ms=pygame.time.get_ticks()
                            self._countdown_dest="playing"
                    if (self.state=="playing" and not self.paused
                            and not self.show_avatar_menu and event.key in KEY_DIR):
                        d=KEY_DIR[event.key]; self._held_dir=d
                        self._hold_start=now_ms; self._last_rep=now_ms
                        self.move_player(*d)
                    if event.key in (pygame.K_RETURN,pygame.K_SPACE) and not self.show_avatar_menu:
                        if self.state=="game_over":
                            self.score=0; self.lives=5; self.total_dots_eaten_run=0
                            self.level=self.start_level
                            if self.level=="unlimited": self.unlimited_sub=1
                            self._init_round(); self._setup_layout()
                            self.state="countdown"
                            self._countdown_ms=pygame.time.get_ticks()
                            self._countdown_dest="playing"

                if event.type==pygame.KEYUP:
                    if event.key in KEY_DIR and KEY_DIR.get(event.key)==self._held_dir:
                        self._held_dir=None

            # Hold move
            if (self.state=="playing" and not self.paused and not self.show_avatar_menu
                    and self._held_dir):
                if now_ms-self._hold_start>=HOLD_DELAY:
                    if now_ms-self._last_rep>=HOLD_REPEAT:
                        self.move_player(*self._held_dir); self._last_rep=now_ms

            # Splash auto-advance
            if self.state=="splash":
                elapsed=pygame.time.get_ticks()-self._splash_start
                if elapsed>=self._splash_duration:
                    self.state="login"

            # Game logic
            if self.state=="playing" and not self.paused and not self.show_avatar_menu:
                now=time.time()
                if now-self.last_tick>=1.0:
                    self.last_tick=now
                    if self.maze_timer_max>0:
                        self.maze_timer-=1
                        self._maze_reshuffle_next=self.maze_timer
                        if self.maze_timer<=0:
                            self._reshuffle_maze(); self.maze_timer=self.maze_timer_max
                            self._maze_reshuffle_next=self.maze_timer_max
                    self._tick_powerup()
                self.frame+=1; self.anim_frame+=1
                if self.frame%self.ai_speed==0: self._step_ai()
                self._tick_active_powerup_frame()
                self._apply_dot_magnet()
                if len(self.dots)==0: self._next_level()

            # Countdown
            if self.state=="countdown":
                elapsed_ms=pygame.time.get_ticks()-self._countdown_ms
                remaining=3-elapsed_ms//1000
                if remaining<1:
                    self.paused=False
                    self.state=self._countdown_dest

            # ── RENDER ──
            self.screen.fill((12,10,24))

            if self.state=="splash":
                self._draw_splash()
            elif self.state=="login":
                self._draw_login()
            elif self.state=="level_select":
                self._draw_level_select()
            else:
                self._draw_titlebar()
                self._draw_maze()
                self._draw_panel()
                if self.state=="game_over":
                    self._draw_game_over_overlay()
                if self.state=="paused":
                    self._draw_paused_overlay()
                if self.state=="esc_confirm":
                    self._draw_esc_confirm()
                if self.state=="level_confirm":
                    self._draw_level_confirm()
                if self.state=="countdown":
                    elapsed_ms=pygame.time.get_ticks()-self._countdown_ms
                    remaining=3-elapsed_ms//1000
                    self._draw_countdown(max(1,remaining))

            if self.show_avatar_menu:
                self._draw_avatar_overlay()

            pygame.display.flip()
            clock.tick(FPS)

if __name__=="__main__":
    Game().run()
