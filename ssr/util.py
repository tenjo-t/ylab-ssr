class SSRError(Exception):
    pass


def flatten(iter):
    return [
        z
        for y in iter
        for z in (
            flatten(y) if hasattr(y, "__iter__") and not isinstance(y, str) else (y,)
        )
    ]
