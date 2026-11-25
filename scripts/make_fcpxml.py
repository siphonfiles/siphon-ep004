"""Timeline for DaVinci Resolve (FCPXML 1.8) from the editable package of an episode.

Package layout (made by .github/workflows/resolve-package.yml):
  video/<ep>_graphics_4k.mp4     picture without Thomas (black where he is)        -> V1
  thomas/thomas_NN_<frame>.mp4   every Thomas shot, at its place (name = first frame) -> V2
  audio/<ep>_voice.wav, _music.wav, _bass.wav                                       -> A1, A2, A3
Usage: python3 scripts/make_fcpxml.py <package dir> <path of the package on the Mac> <ep>
"""
import glob, os, subprocess, sys
from xml.sax.saxutils import quoteattr

pkg, mac_root, ep = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3]
FPS = 30


def frames(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0",
                          "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return int(out)


def samples(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return int(round(float(out) * FPS))


def url(rel):
    return quoteattr("file://" + (mac_root + "/" + rel).replace(" ", "%20"))


t = lambda f: f"{f}/{FPS}s"
res, clips = [], []
g_rel = f"video/{ep}_graphics_4k.mp4"
gN = frames(os.path.join(pkg, g_rel))
res.append(f'<asset id="g" name="graphics" start="0s" duration="{t(gN)}" hasVideo="1" format="r1" src={url(g_rel)}/>')
for k, f in enumerate(sorted(glob.glob(os.path.join(pkg, "thomas", "thomas_*.mp4")))):
    rel = "thomas/" + os.path.basename(f)
    f0 = int(os.path.splitext(f)[0].split("_")[-1])
    n = frames(f)
    res.append(f'<asset id="t{k}" name="{os.path.basename(f)[:-4]}" start="0s" duration="{t(n)}" hasVideo="1" '
               f'format="r1" src={url(rel)}/>')
    clips.append(f'<asset-clip ref="t{k}" lane="1" offset="{t(f0)}" start="0s" duration="{t(n)}" '
                 f'name="{os.path.basename(f)[:-4]}"/>')
for lane, name in ((-1, "voice"), (-2, "music"), (-3, "bass")):
    rel = f"audio/{ep}_{name}.wav"
    n = samples(os.path.join(pkg, rel))
    res.append(f'<asset id="{name}" name="{name}" start="0s" duration="{t(n)}" hasAudio="1" audioSources="1" '
               f'audioChannels="1" audioRate="48000" src={url(rel)}/>')
    clips.append(f'<asset-clip ref="{name}" lane="{lane}" offset="0s" start="0s" duration="{t(n)}" name="{name}"/>')

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.8">
  <resources>
    <format id="r1" name="FFVideoFormat2160p30" frameDuration="1/{FPS}s" width="3840" height="2160"/>
    {chr(10).join("    " + r for r in res).strip()}
  </resources>
  <library>
    <event name="Siphon Files {ep}">
      <project name="{ep} edit">
        <sequence format="r1" duration="{t(gN)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
            <asset-clip ref="g" offset="0s" start="0s" duration="{t(gN)}" name="graphics">
              {chr(10).join("              " + c for c in clips).strip()}
            </asset-clip>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
open(os.path.join(pkg, f"{ep}_resolve.fcpxml"), "w").write(xml)
print("fcpxml:", len(clips) - 3, "Thomas shots,", gN, "frames")
