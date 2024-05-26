import yaml
from anyascii import anyascii

def normalize_str(_str) -> str:
    _str = anyascii(str(_str))
    _str = _str.lower()
    _str = _str.replace(' ', '_')
    _str = _str.replace('-', '_')
    return _str

def get(key: str, default={}):
    if normalize_str(key) not in globals():
        return default
    return globals()[normalize_str(key)]

def normalize_dict(d: dict) -> dict:
    # Recursively normalize a dictionary
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_dict[normalize_str(k)] = normalize_dict(v)
        else:
            new_dict[normalize_str(k)] = v
    return new_dict

with open('config.yml', 'r') as file:
    raw_cfg = yaml.safe_load(file)
    globals().update(normalize_dict(raw_cfg))