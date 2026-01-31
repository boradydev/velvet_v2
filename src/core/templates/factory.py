from abc import ABC, abstractmethod


class TemplateFactory(ABC):
    @abstractmethod
    def render(self, filename: str, template_dir: str | None = None, **kwargs) -> str:
        """
        :param template_dir: Можно указать путь до папки при вызове рендера
        :param filename: Имя файла для рендера
        :param kwargs: словарь переменных для подстановки в Markdown
        :return: текст из md файла с подставленными переменными
        """
