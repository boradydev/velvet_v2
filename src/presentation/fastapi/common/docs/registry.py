from jinja2 import Environment, FileSystemLoader

from src.core.templates.factory import TemplateFactory
from src.core.templates.registry import TemplateRegistry


class DocsTemplateFactory(TemplateFactory):
    """
    Фабрика для рендеринга Markdown-шаблонов из файловой системы.

    Args:
        template_dir: Путь к директории с шаблонами по умолчанию.
    """

    def __init__(self, template_dir: str):
        self.template_dir = template_dir

    def render(
        self,
        filename: str,
        template_dir: str | None = None,
        **kwargs,
    ) -> str:
        env_dir = template_dir if template_dir else self.template_dir
        env = Environment(loader=FileSystemLoader(env_dir))
        template = env.get_template(filename)
        return template.render(**kwargs)


class DocsTemplateRegistry(TemplateRegistry):
    """
    Реализация реестра шаблонов, использующая фабрику для предварительного рендеринга.

    Хранит отрендеренный контент в словаре для быстрого доступа.

    Args:
        factory: Фабрика для генерации текста из шаблонов.
    """

    def __init__(self, factory: TemplateFactory):
        self._factory = factory
        self._docs: dict[str, str] = {}

    def add(
        self,
        filename: str,
        template_dir: str | None = None,
        **kwargs,
    ) -> None:
        self._docs[filename] = self._factory.render(filename, template_dir, **kwargs)

    def get(self, filename: str) -> str:
        return self._docs[filename]
