import bpy, os, sys, time
def p(*a): print(*a); sys.stdout.flush()
V = r"C:\Users\prave\OneDrive\Documents\Static_real_estate_architectural_construction_202609061414.mp4"
O = r"C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\cf76b176-32c7-4bd6-b718-0d820a23a53c\scratchpad\frames"
sc = bpy.context.scene
sc.sequence_editor_create()
se = sc.sequence_editor
coll = se.strips if hasattr(se,"strips") else se.sequences
strip = coll.new_movie("clip", V, 1, 1)
n = strip.frame_final_duration
el = strip.elements[0]
sc.render.resolution_x, sc.render.resolution_y = 1200, 675
sc.render.resolution_percentage = 100
sc.render.use_sequencer = True
sc.render.film_transparent = False
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 66
sc.frame_start, sc.frame_end = 1, n
N = 72                                   # sampled frames for the scrubber
t0 = time.time()
for i in range(N):
    f = 1 + round(i*(n-1)/(N-1))
    sc.frame_set(f)
    sc.render.filepath = os.path.join(O, "s%03d.jpg" % i)
    bpy.ops.render.render(write_still=True)
    if i % 12 == 0: p("  %d/%d  (src frame %d)  %.0fs" % (i+1, N, f, time.time()-t0))
p("EXTRACT DONE %d frames in %.0fs" % (N, time.time()-t0))
