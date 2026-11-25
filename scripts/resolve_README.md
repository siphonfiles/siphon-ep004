# Siphon Files — pachet editabil pentru DaVinci Resolve

1. Dezarhivează `ep001_resolve_kit.zip` în `~/work/` → apare folderul `siphon-ep001-resolve`.
2. Pune `ep001_graphics_4k.mp4` (fișierul mare din Release) în `siphon-ep001-resolve/video/`.
3. În Resolve: proiect nou, 3840x2160, 30 fps → File → Import → Timeline… → alege `ep001_resolve.fcpxml`.
   Dacă Resolve cere media, arată-i folderul `siphon-ep001-resolve`.

Piste:
- **V1** grafica și ilustrațiile, fără Thomas (negru unde apare el)
- **V2** fiecare cadru cu Thomas, la locul lui (prim-planurile sunt deja mărite)
- **A1** vocea lui Thomas · **A2** muzica · **A3** loviturile de bas
- `audio/ep001_final_mix_reference.m4a` = mixul final aprobat, doar pentru comparație (nu e pe timeline)

Nivelurile pistelor audio sunt exact cele din master (-14 LUFS împreună); masterul final mai are un limitator
ușor (-1,8 dBFS vârf). La export pentru YouTube: H.264/H.265, 3840x2160, 30 fps, audio AAC, -14 LUFS.
