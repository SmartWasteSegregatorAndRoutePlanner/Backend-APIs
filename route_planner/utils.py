def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


def sanitize(data: str) -> str:
    return str(data).replace('\"', '&quot;').replace('\'', '&#39;').replace('<', '&lt;').replace('>', '&gt;')
