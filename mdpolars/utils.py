import re

from polars import DataFrame, Utf8, col


def _is_header(extracted):
    """
    >>> _is_header(["---", "---"])
    True
    >>> _is_header([":---", "---:", ":---:"])
    True
    >>> _is_header([":---", "foo", "bar"])
    False
    >>> _is_header(["foo", "bar"])
    False
    """
    partial_pattern = r":*-+:*"
    return all(re.match(partial_pattern, ex) for ex in extracted)


def _extract_line(line: str, possible_separator):
    """
    >>> _extract_line("| foo | bar |", False)
    (['foo', 'bar'], False)
    >>> _extract_line("| foo | bar |", True)
    (['foo', 'bar'], False)
    >>> _extract_line("| --- | --- |", False)
    (['---', '---'], False)
    >>> _extract_line("| --- | --- |", True)
    ([], True)
    """
    # need to accept overlapping patterns.
    vertical_pattern = r"(?=(\|(.*?)\|))"
    plus_pattern = r"(?=(\+(.*?)\+))"
    extracted = [value.strip() for _, value in re.findall(vertical_pattern, line)]
    if possible_separator and not extracted:
        # check this pattern's separator, ex. +-----+----+
        extracted = [value.strip() for _, value in re.findall(plus_pattern, line)]

    if not extracted:
        return [], False

    if possible_separator and _is_header(extracted):
        return [], True

    return extracted, False


def _convert(arraies):
    """
    >>> _convert([])
    []
    >>> _convert([["foo", "bar"]])
    [['foo'], ['bar']]
    >>> _convert([["hoge", "fuga"], ["foo", "bar"]])
    [['hoge', 'foo'], ['fuga', 'bar']]
    """
    if len(arraies) == 0:
        return []
    height = len(arraies[0])
    convert = [[] for _ in range(height)]
    for arr in arraies:
        for idx, element in enumerate(arr):
            convert[idx].append(element)
    return convert


def from_md(table: str, schema=None):
    """

    Args:
        table (str): a markdown table
        schema (list, optional): a header of the columns

    Returns:
        polars.DataFrame
    """
    rows = []
    for line in table.split("\n"):
        extracted, is_schema = _extract_line(line.strip(), len(rows) == 1)
        if is_schema:
            if schema is None:
                schema = rows[0]
            rows.pop(0)
            continue

        if extracted == []:
            continue

        rows.append(extracted)

    dtypes = {}
    if schema is not None:
        for idx in range(len(schema)):
            if isinstance(schema[0], tuple) and len(schema[idx]) >= 2:
                dtypes[schema[idx][0]] = schema[idx][1]
                schema[idx] = schema[idx][0]

    rows = _convert(rows)

    if schema is None:
        schema = [f"column_{i + 1}" for i in range(len(rows))]

    df = DataFrame(rows, schema=schema)
    for column in df.columns:
        if column in dtypes:
            df = df.with_columns(col(column)).cast(dtypes[column], strict=True)
            continue
        if len(df[column]) == 0:
            df = df.with_columns(col(column)).cast(Utf8, strict=True)
    return df
