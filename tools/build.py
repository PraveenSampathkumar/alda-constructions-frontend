import base64, json, os, sys, re, glob

BASE = r"C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\cf76b176-32c7-4bd6-b718-0d820a23a53c\scratchpad"
S    = os.path.join(BASE, "v5site")
V4   = os.path.join(BASE, "v4site")
FR   = os.path.join(BASE, "frames")
OUT  = os.path.join(S, "alda-live.html")

def uri(p, mime):
    with open(p, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

head  = open(os.path.join(V4, "_head.html"), encoding="utf-8").read()
pages = open(os.path.join(V4, "_pages.html"), encoding="utf-8").read()
base  = open(os.path.join(V4, "tpl_base.html"), encoding="utf-8").read()
nav   = base[base.index('<header class="nav">'):base.index('<main>')]
foot  = base[base.index('<footer>'):base.index('<script>')]
home  = open(os.path.join(S, "_home.html"), encoding="utf-8").read()
scr   = open(os.path.join(S, "_script.html"), encoding="utf-8").read()

files = sorted(glob.glob(os.path.join(FR, "s*.jpg")))
if len(files) < 10:
    sys.exit("only %d frames found in %s" % (len(files), FR))
frames = [uri(f, "image/jpeg") for f in files]
raw = sum(os.path.getsize(f) for f in files)
print("frames : %d, %.2f MB raw -> %.2f MB base64" % (len(files), raw/1e6, sum(map(len, frames))/1e6))

photo = uri(os.path.join(S, "photo.jpg"), "image/jpeg")

doc = head + nav + "<main>\n" + home + pages + "</main>\n" + foot + scr
doc = doc.replace("__FRAMES__", json.dumps(frames)).replace("__PHOTO__", photo)

left = sorted(set(re.findall(r"__[A-Z_]+__", doc)))
if left:
    sys.exit("unreplaced tokens: %s" % left)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

size = os.path.getsize(OUT)
print("built  : %s" % OUT)
print("page   : %.2f MB" % (size/1e6))

# quick structural sanity
for tag in ("section", "div", "main", "header", "footer", "canvas", "article"):
    o = len(re.findall(r"<%s[\s>]" % tag, doc)); c = len(re.findall(r"</%s>" % tag, doc))
    if o != c:
        print("  WARN <%s> %d open / %d close" % (tag, o, c))
print("routes : %d" % len(set(re.findall(r'data-page="([^"]+)"', doc))))
