import bpy, numpy as np, os, sys
def p(*a): print(*a); sys.stdout.flush()
SRC  = r"C:\Users\prave\OneDrive\Documents\Gemini_Generated_Image with building.png"
OUTD = r"C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\cf76b176-32c7-4bd6-b718-0d820a23a53c\scratchpad\v5site"
im = bpy.data.images.load(SRC); W,H = im.size
buf = np.empty(W*H*4, dtype=np.float32); im.pixels.foreach_get(buf)
px = buf.reshape(H,W,4)[::-1,:,:3]          # row 0 = top

# clean sky: left of the crane, above the distant hills — real clouds + sun glow
X0,X1 = 0, int(W*0.34)
Y0,Y1 = 0, int(H*0.215)
crop = px[Y0:Y1, X0:X1]
p("crop %dx%d from (%d,%d)" % (crop.shape[1],crop.shape[0],X0,Y0))

def resize(a, nw, nh):
    ys = np.linspace(0, a.shape[0]-1, nh)
    xs = np.linspace(0, a.shape[1]-1, nw)
    y0 = np.floor(ys).astype(int); y1 = np.minimum(y0+1, a.shape[0]-1); fy = (ys-y0)[:,None,None]
    x0 = np.floor(xs).astype(int); x1 = np.minimum(x0+1, a.shape[1]-1); fx = (xs-x0)[None,:,None]
    top = a[y0][:,x0]*(1-fx) + a[y0][:,x1]*fx
    bot = a[y1][:,x0]*(1-fx) + a[y1][:,x1]*fx
    return top*(1-fy) + bot*fy

plate = resize(crop, W, H)

def blur(a, r, passes=2):
    for _ in range(passes):
        pad = np.pad(a, ((r,r),(0,0),(0,0)), mode="edge")
        c = np.cumsum(pad, axis=0); a = (c[2*r:] - c[:-2*r])/(2*r)
        pad = np.pad(a, ((0,0),(r,r),(0,0)), mode="edge")
        c = np.cumsum(pad, axis=1); a = (c[:,2*r:] - c[:,:-2*r])/(2*r)
    return a
plate = blur(plate, max(4, W//200))          # soften the upscale, keep cloud shape

out = np.ones((H,W,4), dtype=np.float32); out[:,:,:3] = np.clip(plate,0,None)
sky = bpy.data.images.new("plate", W, H, alpha=False)
sky.pixels.foreach_set(out[::-1].reshape(-1))
sc = bpy.context.scene
sc.render.image_settings.file_format="JPEG"; sc.render.image_settings.quality=92
sky.save_render(os.path.join(OUTD,"sky_plate.jpg"), scene=sc)
p("sky plate -> %.0f KB" % (os.path.getsize(os.path.join(OUTD,"sky_plate.jpg"))/1024))
