#!/usr/bin/env python3
"""more-focus — standalone lofi web app"""
import asyncio, os
from pathlib import Path
from aiohttp import web

PORT        = int(os.environ.get('PORT', 8766))
PREFIX      = os.environ.get('ROUTE_PREFIX', '')   # '' on Render, '/more-focus' behind nginx
HERE        = Path(__file__).parent
INDEX       = HERE / 'index.html'
SOUNDS_DIR  = HERE / 'sounds'
SOUND_NAMES = {'rain','keyboard','white','brown','water','thunder','piano1','piano2'}

_INDEX_CACHE: str | None = None

def _build_index() -> str:
    global _INDEX_CACHE
    if _INDEX_CACHE is None:
        html = INDEX.read_text(encoding='utf-8')
        # replace hardcoded /more-focus prefix with whatever PREFIX is
        html = html.replace('/more-focus/api/sounds/', f'{PREFIX}/api/sounds/')
        _INDEX_CACHE = html
    return _INDEX_CACHE


async def handle_index(request):
    return web.Response(text=_build_index(), content_type='text/html', charset='utf-8')


async def handle_sound(request):
    name = request.match_info['name'].strip()
    if name not in SOUND_NAMES:
        return web.Response(status=404)
    f = SOUNDS_DIR / f'{name}.mp3'
    if not f.exists():
        return web.Response(status=404, text=f'ไม่พบ {name}.mp3')
    return web.FileResponse(f, headers={
        'Cache-Control': 'max-age=86400',
        'Access-Control-Allow-Origin': '*',
    })


async def main():
    app = web.Application()
    root = PREFIX or ''
    app.router.add_get(root + '/',                   handle_index)
    app.router.add_get(root + '/api/sounds/{name}',  handle_sound)
    if root:
        app.router.add_get(root, handle_index)

    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f'more-focus running on port {PORT}  prefix="{PREFIX or "/"}"')
    await asyncio.sleep(float('inf'))


if __name__ == '__main__':
    asyncio.run(main())
