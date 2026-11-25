"""Generate a ~5 s Thomas clip with LongCat-Video-Avatar 1.6 via a ZeroGPU Space (uses the
account's daily ZeroGPU quota through HF_TOKEN; no paid credits as long as quota remains and
auto-recharge stays off).

Usage: python scripts/longcat_clip.py presenter/clips/inputs/<job>.json out/
"""
import json, os, shutil, sys, time
from gradio_client import Client, handle_file

job = json.load(open(sys.argv[1]))
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
space = job.get("space", "victor/LongCat-Video-Avatar-1.6")

image = job["image"]
cf = job.get("continue_from")
if cf:  # seamless chain: start from the exact frame of the previous clip at the seam
    import subprocess
    image = os.path.join(out_dir, job["name"] + "_seed_frame.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cf["clip"], "-ss", str(cf["at"]), "-frames:v", "1", image], check=True)
    print("continuing from", cf["clip"], "at", cf["at"], "s")
# download_files=False: we fetch the result ourselves, with the token and retries. A 403 on the
# automatic download (ep. 003, b8) lost a clip that had already been generated and paid for.
client = Client(space, token=os.environ["HF_TOKEN"], download_files=False)
t0 = time.time()
res = client.predict(
    handle_file(image), handle_file(job["audio"]), job["prompt"], job["resolution"],
    job["seed"], job["vocal_mode"], job["acceleration"], api_name="/generate")
wall = time.time() - t0
item = res[0] if isinstance(res, (list, tuple)) else res
if isinstance(item, dict) and "video" in item:
    item = item["video"]
dst = os.path.join(out_dir, job["name"] + ".mp4")
if isinstance(item, str) and os.path.exists(item):
    shutil.copy(item, dst)
else:
    import httpx
    url = item.get("url") if isinstance(item, dict) else item
    if url and not url.startswith("http"):
        url = client.src.rstrip("/") + "/gradio_api/file=" + (item.get("path") if isinstance(item, dict) else url)
    print("result url:", url, flush=True)
    for k in range(8):
        try:
            r = httpx.get(url, headers={"Authorization": "Bearer " + os.environ["HF_TOKEN"]},
                          follow_redirects=True, timeout=120)
            r.raise_for_status()
            open(dst, "wb").write(r.content)
            break
        except Exception as ex:
            print("download attempt", k + 1, "failed:", ex, flush=True)
            time.sleep(10 + 10 * k)
    else:
        raise SystemExit("could not download the generated clip: " + str(url))
meta = dict(job, wall_seconds=round(wall, 1), space=space, output=os.path.basename(dst))
json.dump(meta, open(os.path.join(out_dir, job["name"] + ".json"), "w"), indent=2)
print(json.dumps(meta, indent=2))
