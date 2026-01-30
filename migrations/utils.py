from pathlib import Path


def sql(filename: str) -> str:
    """
    :param filename: sql file name
    :return: text from SQL script
    """
    sql_path = Path("migrations/sql") / filename
    result = sql_path.read_text(encoding="utf-8")
    return result
