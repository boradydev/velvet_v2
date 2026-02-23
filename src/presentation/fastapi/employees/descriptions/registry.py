from src.core.paths import PROJECT_DIR
from src.presentation.fastapi.common.descriptions import registry


template_factory = registry.DocsTemplateFactory(
    str(PROJECT_DIR / "src/presentation/fastapi/employees")
)
docs_registry = registry.DocsTemplateRegistry(template_factory)

docs_registry.add(
    "descriptions/register.md",
    str(PROJECT_DIR / "src/presentation/fastapi/employees"),
    # expire_register=str(round(settings.REGISTRATION_EXPIRE_MINUTES / 60)),
    # expire_code=str(settings.CONFIRM_CODE_EXPIRE_MINUTES),
)
