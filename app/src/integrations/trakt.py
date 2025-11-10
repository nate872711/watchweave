import logging, requests
API='https://api.trakt.tv'

def _headers(config):
    t = config.get('trakt',{})
    return {'Authorization': f"Bearer {t.get('access_token','')}", 'Content-Type':'application/json','trakt-api-version':'2','trakt-api-key': t.get('client_id','')}

def refresh_trakt_token(config):
    t = config.get('trakt',{})
    if not t.get('enabled') or not t.get('refresh_token'): return config
    try:
        res = requests.post(f"{API}/oauth/token", json={'refresh_token': t['refresh_token'],'client_id': t['client_id'],'client_secret': t['client_secret'],'redirect_uri':'urn:ietf:wg:oauth:2.0:oob','grant_type':'refresh_token'}, timeout=15)
        if res.status_code==200:
            data=res.json(); t['access_token']=data['access_token']; t['refresh_token']=data.get('refresh_token', t['refresh_token']); logging.info('Trakt token refreshed')
        else: logging.warning('Trakt refresh failed (%s): %s', res.status_code, res.text)
    except Exception as e: logging.warning('Trakt refresh error: %s', e)
    return config

def get_trakt_watched(config):
    t=config.get('trakt',{})
    if not t.get('enabled'): return []
    try:
        res = requests.get(f"{API}/sync/watched/movies", headers=_headers(config), timeout=20); res.raise_for_status()
        movies=res.json(); out=[{'title':m['movie']['title'],'year':m['movie']['year'],'ids':m['movie']['ids']} for m in movies]
        logging.info('Trakt watched: %s', len(out)); return out
    except Exception as e: logging.warning('Trakt watched error: %s', e); return []

def mark_trakt_watched_imdb(config, imdb_id:str)->bool:
    if not imdb_id: return False
    try:
        res=requests.post(f"{API}/sync/history", headers=_headers(config), json={'movies':[{'ids':{'imdb': imdb_id}}]}, timeout=15)
        if res.status_code in (200,201): logging.info('Marked watched on Trakt imdb=%s', imdb_id); return True
        logging.warning('Mark watched failed: %s - %s', res.status_code, res.text)
    except Exception as e: logging.warning('Trakt mark watched error: %s', e)
    return False
