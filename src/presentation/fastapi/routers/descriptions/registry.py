from jinja2 import Environment, FileSystemLoader

from src.core.paths import PROJECT_DIR
from src.core.settings import settings
from src.core.templates.factory import TemplateFactory
from src.core.templates.registry import TemplateRegistry


class DocsTemplateFactory(TemplateFactory):
    def __init__(self, template_dir: str):
        """
        Инициализирует экземпляр класса с заданным путем к папке.
        :param template_dir: Путь к папке, которая будет использоваться экземпляром.
        """
        self.template_dir = template_dir

    def render(self, filename: str, template_dir: str | None = None, **kwargs) -> str:
        env_dir = template_dir if template_dir else self.template_dir
        env = Environment(loader=FileSystemLoader(env_dir))
        template = env.get_template(filename)
        return template.render(**kwargs)


class DocsTemplateRegistry(TemplateRegistry):
    def __init__(self, factory: TemplateFactory):
        self._factory = factory
        self._docs: dict[str, str] = {}

    def add(self, filename: str, template_dir: str | None = None, **kwargs) -> None:
        self._docs[filename] = self._factory.render(filename, template_dir, **kwargs)

    def get(self, filename: str) -> str:
        return self._docs[filename]


template_factory = DocsTemplateFactory(str(PROJECT_DIR / "src/presentation/fastapi/routers"))
docs_registry = DocsTemplateRegistry(template_factory)

docs_registry.add(
    "descriptions/auth.md",
    str(PROJECT_DIR / "src/presentation/fastapi/routers"),
    expire_register=str(round(settings.UNCONFIRMED_REGISTRATION_EXPIRE_MINUTES / 60)),
    expire_code=str(settings.CONFIRM_CODE_EXPIRE_MINUTES),
)
