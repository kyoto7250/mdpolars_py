# mdpolars_py
a simple tool for convert markdown table to polars in python3.
This tool is a lightweight tool for testing a code, so note that we are not validating the user's input.

[pandas version is here](https://github.com/kyoto7250/mdpd)

## install
```bash
pip install mdpolars
```

## usage

```python
import polars as pl
import mdpolars

df = mdpolars.from_md("""
+------------+-------+
| id         | score |
+------------+-------+
| 1          | 15    |
| 2          | 11    |
| 3          | 11    |
| 4          | 20    |
+------------+-------+
""", schema=[("id", pl.Int64), ("score", pl.Int64)])

print(df)
# shape: (4, 2)
# ┌─────┬───────┐
# │ id  ┆ score │
# │ --- ┆ ---   │
# │ i64 ┆ i64   │
# ╞═════╪═══════╡
# │ 1   ┆ 15    │
# │ 2   ┆ 11    │
# │ 3   ┆ 11    │
# │ 4   ┆ 20    │
# └─────┴───────┘
```

```python
# the header can be overwritten if the header exists
import mdpolars
df = mdpolars.from_md("""
+------------+-------+
| id         | score |
+------------+-------+
| 1          | 15    |
| 2          | 11    |
| 3          | 11    |
| 4          | 20    |
+------------+-------+
""", schema=["foo", "bar"])

# the default type is str.
print(df)
# shape: (4, 2)
# ┌─────┬─────┐
# │ foo ┆ bar │
# │ --- ┆ --- │
# │ str ┆ str │
# ╞═════╪═════╡
# │ 1   ┆ 15  │
# │ 2   ┆ 11  │
# │ 3   ┆ 11  │
# │ 4   ┆ 20  │
# └─────┴─────┘
```


## accepted table patterns

```markdown
| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |
```

```markdown
+------------+-------------+
| Syntax     | Description |
+------------+-------------+
| Header     | Title       |
| Paragraph  | Text        |
+------------+-------------+
```

```markdown
| Syntax    | Description |
| :-------- | ----------: |
| Header    | Title       |
| Paragraph | Text        |
```

```markdown
| Header    | Title       |
| Paragraph | Text        |
```

## contribute
If you have suggestions for features or improvements to the code, please feel free to create an issue or PR.
