from texjam import MetaField, TexJamPlugin
from texjam.path import TempPath


class _ModulePlugin(TexJamPlugin):
    module_name: str
    meta_fields: list[str] = []

    def pre_prompt(self, field: MetaField) -> bool | None:
        if (
            field.key in self.meta_fields
            and self.metadata.get(f'enable_{self.module_name}') is False
        ):
            return True

    def on_paths(self, paths: list[TempPath]) -> list[TempPath] | None:
        if self.metadata.get(f'enable_{self.module_name}') is False:
            return [
                p
                for p in paths
                if p.raw is None
                or p.raw.relative_to(self.texjam.template_source_dir).parts[2]
                != self.module_name
            ]


class LayoutPlugin(_ModulePlugin):
    module_name = 'layout'
    meta_fields = ['fancy_header_footer']


class ReferencePlugin(_ModulePlugin):
    module_name = 'reference'


class EnvironmentPlugin(_ModulePlugin):
    module_name = 'environment'
    meta_fields = ['define_custom_environments']


class MathPlugin(_ModulePlugin):
    module_name = 'math'
    meta_fields = ['display_equation_style', 'define_custom_macros']
