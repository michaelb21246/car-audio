# generate_feed.py
import os, subprocess, email.utils
from pathlib import Path
from xml.sax.saxutils import escape

BASE_URL = "https://YOUR_USERNAME.github.io/car-audio"  # update after Pages is live
EP_DIR = Path("episodes")

def get_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    secs = int(float(out.stdout.strip()))
    return f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}"

items = []
for f in sorted(EP_DIR.glob("*.mp3"), key=os.path.getmtime, reverse=True):
    size = f.stat().st_size
    mtime = email.utils.formatdate(f.stat().st_mtime)
    items.append(f"""
    <item>
      <title>{escape(f.stem)}</title>
      <enclosure url="{BASE_URL}/episodes/{f.name}" length="{size}" type="audio/mpeg"/>
      <guid>{BASE_URL}/episodes/{f.name}</guid>
      <pubDate>{mtime}</pubDate>
      <itunes:duration>{get_duration(f)}</itunes:duration>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
  <title>My Car Audio Feed</title>
  <link>{BASE_URL}</link>
  <description>Personal KB summaries, read aloud</description>
  <language>en-us</language>
  {''.join(items)}
</channel>
</rss>"""

Path("feed.xml").write_text(feed, encoding="utf-8")
print(f"Wrote feed.xml with {len(items)} episodes")