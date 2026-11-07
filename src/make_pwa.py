"""Build the published app: python3 -I src/make_pwa.py  (from repo root)
Inlines words into src.html (via build.py) and adds manifest + service worker hooks, writing ./index.html."""
import re, subprocess, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'src')
subprocess.run([sys.executable, '-I', os.path.join(src, 'build.py'), os.path.join(src, 'words.json')], cwd=src, check=True)
s = open(os.path.join(src, 'dist', 'index.html'), encoding='utf-8').read()
s, n = re.subn(r'<link rel="apple-touch-icon" href="data:image/svg\+xml,[^"]+">',
    '<link rel="apple-touch-icon" href="icon-180.png">\n<link rel="manifest" href="manifest.webmanifest">\n'
    '<meta name="apple-mobile-web-app-title" content="Harf Kilimi">', s)
assert n == 1
assert s.count('</body>') == 1
s = s.replace('</body>', "<script>if('serviceWorker' in navigator){addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});}</script>\n</body>")
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(s)
print('wrote index.html', len(s)//1024, 'KB')
