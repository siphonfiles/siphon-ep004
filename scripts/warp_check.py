import sys, types
from unittest.mock import MagicMock
sys.modules['cairo'] = MagicMock()
sys.path.insert(0, '.')
import numpy as np
from PIL import Image
import scenes as S
S.ILL_DIR = '../../illustrations/ep001/img'
names = sys.argv[1].split(',')
moves = sys.argv[2].split(',')
rows = []
for n, mv in zip(names, moves):
    frames = []
    for u in (0.0, 1.0):
        S._ill_load.cache.clear()
        _, data = S._ill_frame(n, u, mv, t=0.0, fog=None)
        c = S._ill_load(n)
        a = np.frombuffer(bytes(data), np.uint8).reshape(c['h'], c['w'], 4)[..., [2, 1, 0]]
        frames.append(Image.fromarray(a).resize((768, 432)))
    row = Image.new('RGB', (1544, 432)); row.paste(frames[0], (0, 0)); row.paste(frames[1], (776, 0)); rows.append(row)
out = Image.new('RGB', (1544, 440 * len(rows)))
for i, r in enumerate(rows): out.paste(r, (0, i * 440))
out.save(sys.argv[3], quality=88)
