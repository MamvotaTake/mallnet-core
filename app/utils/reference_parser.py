import re

def parse_reference(reference: str):
    """
    Expected format: M{mall_id}-P{package_id}
    Example: M1-P3
    """
    match = re.match(r"M(\d+)-P(\d+)", reference)
    if not match:
        raise ValueError("Invalid payment reference format")

    mall_id = int(match.group(1))
    package_id = int(match.group(2))

    return mall_id, package_id
