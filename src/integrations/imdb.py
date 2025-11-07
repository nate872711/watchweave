import csv, logging
from pathlib import Path

def get_imdb_ratings(csv_path:str):
    out=[]
    if not csv_path: return out
    p=Path(csv_path)
    if not p.exists(): logging.info('IMDb CSV not found at %s', csv_path); return out
    try:
        with p.open(newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f): out.append({'title': row.get('Title'), 'rating': row.get('Your Rating')})
        logging.info('IMDb ratings loaded: %s', len(out))
    except Exception as e: logging.warning('IMDb CSV parse error: %s', e)
    return out
