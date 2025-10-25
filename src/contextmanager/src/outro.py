from models import Model

m = Model()
m.load_ckpt()

out = m.generate()

save(out, "out.png")