#!/usr/bin/env python3
"""Minimal pure-standard-library PNG plotting engine (no numpy/matplotlib/PIL).
Supports line plots (multi-series + legend), axis box with ticks/labels, and
value heatmaps. A compact 5x7 bitmap font renders ASCII labels."""
import struct, zlib, math

# ------------------------------------------------------------------ 5x7 font
_F = {
 ' ':[0,0,0,0,0,0,0],
 '0':[0x0E,0x11,0x13,0x15,0x19,0x11,0x0E],'1':[0x04,0x0C,0x04,0x04,0x04,0x04,0x0E],
 '2':[0x0E,0x11,0x01,0x02,0x04,0x08,0x1F],'3':[0x1F,0x02,0x04,0x02,0x01,0x11,0x0E],
 '4':[0x02,0x06,0x0A,0x12,0x1F,0x02,0x02],'5':[0x1F,0x10,0x1E,0x01,0x01,0x11,0x0E],
 '6':[0x06,0x08,0x10,0x1E,0x11,0x11,0x0E],'7':[0x1F,0x01,0x02,0x04,0x08,0x08,0x08],
 '8':[0x0E,0x11,0x11,0x0E,0x11,0x11,0x0E],'9':[0x0E,0x11,0x11,0x0F,0x01,0x02,0x0C],
 'A':[0x0E,0x11,0x11,0x1F,0x11,0x11,0x11],'B':[0x1E,0x11,0x11,0x1E,0x11,0x11,0x1E],
 'C':[0x0E,0x11,0x10,0x10,0x10,0x11,0x0E],'D':[0x1E,0x11,0x11,0x11,0x11,0x11,0x1E],
 'E':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x1F],'F':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x10],
 'G':[0x0E,0x11,0x10,0x17,0x11,0x11,0x0F],'H':[0x11,0x11,0x11,0x1F,0x11,0x11,0x11],
 'I':[0x0E,0x04,0x04,0x04,0x04,0x04,0x0E],'J':[0x07,0x02,0x02,0x02,0x02,0x12,0x0C],
 'K':[0x11,0x12,0x14,0x18,0x14,0x12,0x11],'L':[0x10,0x10,0x10,0x10,0x10,0x10,0x1F],
 'M':[0x11,0x1B,0x15,0x15,0x11,0x11,0x11],'N':[0x11,0x11,0x19,0x15,0x13,0x11,0x11],
 'O':[0x0E,0x11,0x11,0x11,0x11,0x11,0x0E],'P':[0x1E,0x11,0x11,0x1E,0x10,0x10,0x10],
 'Q':[0x0E,0x11,0x11,0x11,0x15,0x12,0x0D],'R':[0x1E,0x11,0x11,0x1E,0x14,0x12,0x11],
 'S':[0x0F,0x10,0x10,0x0E,0x01,0x01,0x1E],'T':[0x1F,0x04,0x04,0x04,0x04,0x04,0x04],
 'U':[0x11,0x11,0x11,0x11,0x11,0x11,0x0E],'V':[0x11,0x11,0x11,0x11,0x11,0x0A,0x04],
 'W':[0x11,0x11,0x11,0x15,0x15,0x15,0x0A],'X':[0x11,0x11,0x0A,0x04,0x0A,0x11,0x11],
 'Y':[0x11,0x11,0x0A,0x04,0x04,0x04,0x04],'Z':[0x1F,0x01,0x02,0x04,0x08,0x10,0x1F],
 '.':[0,0,0,0,0,0x0C,0x0C],'-':[0,0,0,0x0E,0,0,0],"'":[0x04,0x04,0x04,0,0,0,0],
 '(':[0x02,0x04,0x08,0x08,0x08,0x04,0x02],')':[0x08,0x04,0x02,0x02,0x02,0x04,0x08],
 '/':[0x01,0x02,0x02,0x04,0x08,0x08,0x10],'_':[0,0,0,0,0,0,0x1F],
 '=':[0,0,0x1F,0,0x1F,0,0],'+':[0,0x04,0x04,0x1F,0x04,0x04,0],
 ':':[0,0x04,0,0,0x04,0,0],',':[0,0,0,0,0,0x04,0x08],'*':[0,0x15,0x0E,0x1F,0x0E,0x15,0],
 '%':[0x19,0x1A,0x04,0x0B,0x13,0,0],
}
def _glyph(c):
    if c in _F: return _F[c]
    u=c.upper()
    return _F.get(u,_F[' '])

class Canvas:
    def __init__(self,w,h,bg=(255,255,255)):
        self.w=w;self.h=h
        self.buf=bytearray(bg*(w*h))
    def px(self,x,y,c):
        if 0<=x<self.w and 0<=y<self.h:
            i=(y*self.w+x)*3
            self.buf[i]=c[0];self.buf[i+1]=c[1];self.buf[i+2]=c[2]
    def fill_rect(self,x0,y0,x1,y1,c):
        for y in range(int(y0),int(y1)+1):
            for x in range(int(x0),int(x1)+1):
                self.px(x,y,c)
    def line(self,x0,y0,x1,y1,c,th=1):
        x0,y0,x1,y1=int(round(x0)),int(round(y0)),int(round(x1)),int(round(y1))
        dx=abs(x1-x0);dy=-abs(y1-y0)
        sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1;err=dx+dy
        while True:
            for ox in range(th):
                for oy in range(th):
                    self.px(x0+ox,y0+oy,c)
            if x0==x1 and y0==y1:break
            e2=2*err
            if e2>=dy:err+=dy;x0+=sx
            if e2<=dx:err+=dx;y0+=sy
    def text(self,x,y,s,c=(0,0,0),scale=1):
        cx=x
        for ch in str(s):
            g=_glyph(ch)
            for row in range(7):
                bits=g[row]
                for col in range(5):
                    if bits&(1<<(4-col)):
                        self.fill_rect(cx+col*scale,y+row*scale,cx+col*scale+scale-1,y+row*scale+scale-1,c)
            cx+=6*scale
        return cx
    def text_center(self,xc,y,s,c=(0,0,0),scale=1):
        w=len(str(s))*6*scale
        self.text(int(xc-w/2),y,s,c,scale)
    def text_vert(self,x,yc,s,c=(0,0,0),scale=1):
        # draw rotated-ish: stack characters vertically (simple)
        h=len(str(s))*8*scale
        yy=int(yc-h/2)
        for ch in str(s):
            self.text(x,yy,ch,c,scale);yy+=8*scale
    def save(self,fn):
        raw=bytearray()
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.buf[y*self.w*3:(y+1)*self.w*3])
        comp=zlib.compress(bytes(raw),9)
        def chunk(typ,data):
            c=typ+data
            return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
        png=b'\x89PNG\r\n\x1a\n'
        png+=chunk(b'IHDR',struct.pack('>IIBBBBB',self.w,self.h,8,2,0,0,0))
        png+=chunk(b'IDAT',comp)
        png+=chunk(b'IEND',b'')
        with open(fn,'wb') as f:f.write(png)

# ------------------------------------------------------------------ colors
PALETTE=[(31,119,180),(214,39,40),(44,160,44),(255,127,14),(148,103,189),(140,86,75)]
def heat_color(t):
    t=max(0.0,min(1.0,t))
    # blue -> cyan -> green -> yellow -> red
    stops=[(0.0,(30,60,160)),(0.25,(30,160,200)),(0.5,(40,180,60)),
           (0.75,(240,200,40)),(1.0,(210,40,40))]
    for i in range(len(stops)-1):
        t0,c0=stops[i];t1,c1=stops[i+1]
        if t0<=t<=t1:
            f=(t-t0)/(t1-t0)
            return tuple(int(c0[k]+f*(c1[k]-c0[k])) for k in range(3))
    return stops[-1][1]

# ------------------------------------------------------------------ plotter
class Plot:
    def __init__(self,w=660,h=440,title='',xlabel='',ylabel=''):
        self.c=Canvas(w,h)
        self.w=w;self.h=h
        self.ml=70;self.mr=140;self.mt=42;self.mb=52   # margins (mr wide for legend)
        self.title=title;self.xlabel=xlabel;self.ylabel=ylabel
        self.series=[]
    def _px(self,x,y):
        ax0,ay0,ax1,ay1=self.ml,self.mt,self.w-self.mr,self.h-self.mb
        X=ax0+(x-self.xmin)/(self.xmax-self.xmin)*(ax1-ax0)
        Y=ay1-(y-self.ymin)/(self.ymax-self.ymin)*(ay1-ay0)
        return X,Y
    def add(self,xs,ys,label,color=None):
        self.series.append((xs,ys,label,color))
    def render(self,xr,yr,fn,xticks=6,yticks=6):
        self.xmin,self.xmax=xr;self.ymin,self.ymax=yr
        c=self.c
        ax0,ay0,ax1,ay1=self.ml,self.mt,self.w-self.mr,self.h-self.mb
        # title
        c.text_center((ax0+ax1)/2,10,self.title,(0,0,0),2)
        # grid + ticks
        for i in range(xticks+1):
            x=self.xmin+(self.xmax-self.xmin)*i/xticks
            X,_=self._px(x,self.ymin)
            c.line(X,ay0,X,ay1,(225,225,225),1)
            c.line(X,ay1,X,ay1+5,(0,0,0),1)
            c.text_center(X,ay1+10,('%g'%round(x,3)),(0,0,0),1)
        for i in range(yticks+1):
            y=self.ymin+(self.ymax-self.ymin)*i/yticks
            _,Y=self._px(self.xmin,y)
            c.line(ax0,Y,ax1,Y,(225,225,225),1)
            c.line(ax0-5,Y,ax0,Y,(0,0,0),1)
            lbl='%g'%round(y,3)
            c.text(ax0-8-len(lbl)*6,int(Y-3),lbl,(0,0,0),1)
        # axis box
        c.line(ax0,ay0,ax1,ay0,(0,0,0),1);c.line(ax0,ay1,ax1,ay1,(0,0,0),2)
        c.line(ax0,ay0,ax0,ay1,(0,0,0),2);c.line(ax1,ay0,ax1,ay1,(0,0,0),1)
        # labels
        c.text_center((ax0+ax1)/2,self.h-16,self.xlabel,(0,0,0),2)
        c.text_vert(14,(ay0+ay1)/2,self.ylabel,(0,0,0),2)
        # series
        for idx,(xs,ys,label,color) in enumerate(self.series):
            col=color or PALETTE[idx%len(PALETTE)]
            prev=None
            for x,y in zip(xs,ys):
                X,Y=self._px(x,y)
                if prev:c.line(prev[0],prev[1],X,Y,col,2)
                prev=(X,Y)
        # legend
        lx=ax1+14;ly=ay0+6
        for idx,(xs,ys,label,color) in enumerate(self.series):
            col=color or PALETTE[idx%len(PALETTE)]
            c.line(lx,ly+3,lx+22,ly+3,col,3)
            c.text(lx+28,ly,label,(0,0,0),1)
            ly+=16
        c.save(fn)

class Heatmap:
    def __init__(self,w=660,h=440,title='',xlabel='',ylabel=''):
        self.c=Canvas(w,h);self.w=w;self.h=h
        self.ml=70;self.mr=90;self.mt=42;self.mb=52
        self.title=title;self.xlabel=xlabel;self.ylabel=ylabel
    def render(self,xr,yr,func,fn,xticks=6,yticks=6,zlabel=''):
        xmin,xmax=xr;ymin,ymax=yr;c=self.c
        ax0,ay0,ax1,ay1=self.ml,self.mt,self.w-self.mr,self.h-self.mb
        vals={}
        vmin=1e18;vmax=-1e18
        for py in range(int(ay0),int(ay1)):
            fy=(ay1-py)/(ay1-ay0)
            y=ymin+(ymax-ymin)*fy
            for px in range(int(ax0),int(ax1)):
                fx=(px-ax0)/(ax1-ax0)
                x=xmin+(xmax-xmin)*fx
                v=func(x,y);vals[(px,py)]=v
                if v<vmin:vmin=v
                if v>vmax:vmax=v
        rng=(vmax-vmin) or 1.0
        for (px,py),v in vals.items():
            c.px(px,py,heat_color((v-vmin)/rng))
        c.text_center((ax0+ax1)/2,10,self.title,(0,0,0),2)
        for i in range(xticks+1):
            x=xmin+(xmax-xmin)*i/xticks;X=ax0+(ax1-ax0)*i/xticks
            c.line(X,ay1,X,ay1+5,(0,0,0),1);c.text_center(X,ay1+10,'%g'%round(x,3),(0,0,0),1)
        for i in range(yticks+1):
            y=ymin+(ymax-ymin)*i/yticks;Y=ay1-(ay1-ay0)*i/yticks
            c.line(ax0-5,Y,ax0,Y,(0,0,0),1);lbl='%g'%round(y,3)
            c.text(ax0-8-len(lbl)*6,int(Y-3),lbl,(0,0,0),1)
        c.line(ax0,ay0,ax1,ay0,(0,0,0),1);c.line(ax0,ay1,ax1,ay1,(0,0,0),2)
        c.line(ax0,ay0,ax0,ay1,(0,0,0),2);c.line(ax1,ay0,ax1,ay1,(0,0,0),1)
        c.text_center((ax0+ax1)/2,self.h-16,self.xlabel,(0,0,0),2)
        c.text_vert(14,(ay0+ay1)/2,self.ylabel,(0,0,0),2)
        # colorbar
        cbx0=ax1+18;cbx1=ax1+34
        for py in range(int(ay0),int(ay1)):
            t=(ay1-py)/(ay1-ay0)
            c.fill_rect(cbx0,py,cbx1,py,heat_color(t))
        c.line(cbx0,ay0,cbx1,ay0,(0,0,0),1);c.line(cbx0,ay1,cbx1,ay1,(0,0,0),1)
        c.line(cbx0,ay0,cbx0,ay1,(0,0,0),1);c.line(cbx1,ay0,cbx1,ay1,(0,0,0),1)
        c.text(cbx0-6,int(ay0-12),'%g'%round(vmax,2),(0,0,0),1)
        c.text(cbx0-6,int(ay1+4),'%g'%round(vmin,2),(0,0,0),1)
        c.text(cbx1+6,int((ay0+ay1)/2-6),zlabel,(0,0,0),1)
        c.save(fn)

if __name__=='__main__':
    p=Plot(title='FONT TEST',xlabel='ETA',ylabel='F(ETA)')
    p.add([0,0.5,1],[0,0.4,0],'M=1');p.add([0,0.5,1],[0,0.25,0],'M=4')
    p.render((0,1),(0,0.5),'font_test.png')
    print('wrote font_test.png')
