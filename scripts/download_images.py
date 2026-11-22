"""Download the starter collection's Unsplash images for reliable local serving."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

IMAGES = ['photo-1501004318641-b39e6451bec6', 'photo-1497250681960-ef046c08a56e', 'photo-1596547609652-9cf5d8d76921', 'photo-1618375569909-3c8616cf7733', 'photo-1593482892290-f54927ae2b7a', 'photo-1459411552884-841db9b3cc2a', 'photo-1515586000433-45406d8e6662', 'photo-1566907225472-2f5a93116a32', 'photo-1416879595882-3373a0480b5b', 'photo-1485955900006-10f4d324d411']
DEST = Path(__file__).resolve().parent.parent / 'static' / 'images'
REPLACEMENTS = {
    'photo-1593482892290-f54927ae2b7a': 'https://images.pexels.com/photos/4575430/pexels-photo-4575430.jpeg?auto=compress&cs=tinysrgb&w=1400',
    'photo-1566907225472-2f5a93116a32': 'https://images.pexels.com/photos/20013414/pexels-photo-20013414.jpeg?auto=compress&cs=tinysrgb&w=1400',
}
for photo_id in (1327838, 143133, 7676083, 594137, 6954409, 11838530, 16753186):
    key = f'pexels-photo-{photo_id}'
    IMAGES.append(key)
    REPLACEMENTS[key] = f'https://images.pexels.com/photos/{photo_id}/{key}.jpeg?auto=compress&cs=tinysrgb&w=1400'

def download(photo):
    target = DEST / f'{photo}.jpg'
    if target.exists():
        return f'Already downloaded: {photo}'
    try:
        url = REPLACEMENTS.get(photo, f'https://images.unsplash.com/{photo}?auto=format&fit=crop&w=1400&q=85')
        request = Request(url, headers={'User-Agent': 'Planteer/1.0'})
        with urlopen(request, timeout=30) as response:
            content = response.read()
        from PIL import Image
        from io import BytesIO
        with Image.open(BytesIO(content)) as image:
            image.convert('RGB').save(target, 'JPEG', quality=87)
        return f'Downloaded: {photo}'
    except Exception as error:
        return f'FAILED {photo}: {error}'

if __name__ == '__main__':
    DEST.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(download, IMAGES):
            print(result)
