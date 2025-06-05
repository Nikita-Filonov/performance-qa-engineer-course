def to_upper_snake_case(value: str) -> str:
    result = ''.join([f'_{char}' if char.isupper() else char.upper() for char in value])

    if result.startswith('_'):
        result = result[1:]

    return result
