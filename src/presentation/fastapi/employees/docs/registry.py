from src.core.paths import PROJECT_DIR
from src.presentation.fastapi.common.docs import registry


template_factory = registry.DocsTemplateFactory(
    str(PROJECT_DIR / "src/presentation/fastapi/employees")
)
docs_registry = registry.DocsTemplateRegistry(template_factory)

docs_registry.add("docs/register.md")
docs_registry.add("docs/resend.md")
