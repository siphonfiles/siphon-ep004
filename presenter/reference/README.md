# Imaginea de referință a lui Thomas pentru LongCat

| Fișier | Ce e |
|---|---|
| `thomas_ref_v1_source_1344x768.png` | varianta 1 aleasă (Qwen-Image-Edit-2511, seed 11, decor `plate_20251120`) |
| `thomas_ref_v1_centered_1920x1080.png` | aceeași imagine adusă la 1920x1080 pe CPU (Lanczos + sharpening ușor), nimic tăiat; Thomas centrat. **Utilizabilă imediat.** |
| `outpaint_canvas_1920x1080.png` | imaginea mutată spre stânga (Thomas la ~38% din lățime) cu o bandă gri de 245 px în dreapta, de completat |
| (nefolosit, rezervă) `thomas_ref_v1_extended_*.png` | banda din dreapta completată cu Qwen-Image-Edit-2511 (workflow manual `outpaint-ref.yml`, după resetarea cotei); pixelii originali se pun înapoi peste tot în afară de bandă → fața și mâinile rămân identice |

Notă: la 1920x1080 nu apare detaliu nou — sursa e 1344x768. Pentru LongCat (720p) e suficient; pentru thumbnail-uri în HD se poate face o mărire AI separată.

**Decizie (20 nov 2026):** referința finală este `thomas_ref_v1_centered_1920x1080.png` (Thomas centrat). Extinderea spre dreapta nu se mai face.
