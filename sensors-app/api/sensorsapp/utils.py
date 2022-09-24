import json


def to_json(val):
    try:
        return val.datetime.isoformat()
    except:
        pass

    try:
        return val.isoformat()
    except:
        pass

    try:
        assert val.is_finite()
        return float(val)
    except:
        pass

    try:
        json.dumps(val)
        return val
    except:
        return repr(val)


def ensure_json(item):
    if isinstance(item, dict):
        return {key: ensure_json(val) for key, val in item.items()}
    elif isinstance(item, (list, tuple)):
        return [ensure_json(val) for val in item]
    else:
        return to_json(item)
