import re
IMDB_RE = re.compile(r'(tt\d{7,8})')

def extract_imdb_id_from_guid(guid: str):
    if not guid: return None
    m = IMDB_RE.search(guid); return m.group(1) if m else None
