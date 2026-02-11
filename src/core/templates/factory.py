from abc import ABC, abstractmethod


class TemplateFactory(ABC):
    @abstractmethod
    def render(
        self,
        filename: str,
        template_dir: str | None = None,
        **kwargs,
    ) -> str:
        """
        Добавляет готовый шаблон с подставленными переменными в реестр.

        Args:
            filename: Имя файла шаблона
            template_dir: Можно указать путь до папки с шаблонами
            kwargs: Словарь переменных для подстановки в Markdown
        Returns:
            Текст из md файла с подставленными переменными
        """
