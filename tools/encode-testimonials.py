"""Compress testimonial videos for the web.

Usage:  python tools/encode-testimonials.py
Reads every .mp4 in Testimonial/ (kept out of git), writes a 720x1280 H.264 MP4
and a poster JPG per video into assets/video/testimonials/, named from the file
name. Then list each video in LOCAL_VIDEOS in tools/build-site.py and rebuild.
Requires the imageio-ffmpeg package:  python -m pip install imageio-ffmpeg
"""
import glob, os, re, subprocess, sys
from pathlib import Path

try:
    import imageio_ffmpeg
except ImportError:
    sys.exit("Install ffmpeg first:  python -m pip install imageio-ffmpeg")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Testimonial"
OUT = ROOT / "assets" / "video" / "testimonials"
OUT.mkdir(parents=True, exist_ok=True)
exe = imageio_ffmpeg.get_ffmpeg_exe()


def slug(name):
    s = re.sub(r"(?i)(testimon(y|ial)|\bdr\.?)", " ", Path(name).stem)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


for f in sorted(SRC.glob("*.mp4")):
    base = slug(f.name)
    mp4, jpg = OUT / f"{base}.mp4", OUT / f"{base}.jpg"
    if not mp4.exists():
        subprocess.run([exe, "-y", "-i", str(f),
            "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0x08243D,fps=30",
            "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k", "-ac", "2", str(mp4)], check=True, capture_output=True)
    if not jpg.exists():
        subprocess.run([exe, "-y", "-ss", "1", "-i", str(mp4), "-frames:v", "1", "-q:v", "4", str(jpg)], check=True, capture_output=True)
    print(f"{base}: {mp4.stat().st_size / 1e6:.1f} MB")
print("done")
