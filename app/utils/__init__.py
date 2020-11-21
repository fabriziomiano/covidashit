from config import ITALY_MAP


def region_of_province(province_in: str) -> str:
    """
    Return the corresponding key in ITALY_MAP whose value contains province_in
    :param province_in: str
    :return: str
    """
    region = None
    for r in ITALY_MAP:
        for p in ITALY_MAP[r]:
            if province_in == p:
                region = r
    return region
