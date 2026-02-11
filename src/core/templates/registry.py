from abc import ABC, abstractmethod


class TemplateRegistry(ABC):
    @abstractmethod
    def add(
        self,
        filename: str,
        template_dir: str | None = None,
        **kwargs,
    ) -> None:
        """
        Регистрирует новый шаблон в системе.

        Args:
            filename: Имя файла для добавления.
            template_dir: Путь до папки с файлом.
            kwargs: Переменные для подстановки в Markdown.
        """

    @abstractmethod
    def get(self, filename) -> str:
        """
        Возвращает текст шаблона по его имени.

        Args:
            filename: Имя файла для получения.

        Returns:
            Текст шаблона.
        """
