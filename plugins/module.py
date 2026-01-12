from texjam import TempPath, TexJamPlugin
from texjam.config import MetaField


class ModuleFilterPlugin(TexJamPlugin):
    modules: list[str] = [
        'layout',
        'font',
        'reference',
        'citation',
        'math',
        'environment',
    ]

    def enabled(self, module_name: str) -> bool:
        if 'modules' in self.metadata:
            return module_name in self.metadata['modules']
        return False

    @property
    def enabled_modules(self) -> list[str]:
        if 'modules' in self.metadata:
            return self.metadata['modules']
        return []

    def get_module_name(self, path: TempPath) -> str | None:
        if path.raw is None:
            return None
        parts = path.raw.relative_to(self.texjam.template_source_dir).parts
        if len(parts) < 3 or parts[1] != 'preamble':
            return None
        if parts[2] in self.modules:
            return parts[2]
        return None

    def pre_prompt(self, name: str, field: MetaField) -> bool | None:
        for module_name in self.modules:
            if name == f'{module_name}_options':
                return not self.enabled(module_name)

    def on_paths(self, paths: list[TempPath]) -> list[TempPath] | None:
        filtered_paths = []
        for path in paths:
            module_name = self.get_module_name(path)
            if module_name is None or self.enabled(module_name):
                filtered_paths.append(path)
        return filtered_paths
