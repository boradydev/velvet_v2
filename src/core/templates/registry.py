from abc import ABC, abstractmethod


class TemplateRegistry(ABC):
    @abstractmethod
    def add(self, filename: str, template_dir: str | None = None, **kwargs) -> None:
        """
        :param template_dir: Можно указать путь до папки с файлом
        :param filename: Имя файла для добавления
        :param kwargs: Словарь переменных для подстановки в Markdown
        """

    @abstractmethod
    def get(self, filename) -> str:
        """
        :param filename: Имя файла для получения
        :return: Текст шаблона
        """
