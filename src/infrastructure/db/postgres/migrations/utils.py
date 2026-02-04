from src.core.paths import PROJECT_DIR


def sql(
    filename: str,
    path_dir: str = "src/infrastructure/db/postgres/migrations/sql",
) -> str:
    """
    Получает SQL скрипт из файла.

    Args:
        filename: Имя SQL скрипта
        path_dir: Путь до папки с SQL скриптами
    Returns:
        Текст из SQL скрипта
    """
    sql_path = PROJECT_DIR / path_dir / filename
    result = sql_path.read_text(encoding="utf-8")
    return result
