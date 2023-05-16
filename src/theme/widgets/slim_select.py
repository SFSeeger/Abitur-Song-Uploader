from typing import Any, Dict

from django.forms.widgets import Select, SelectMultiple


class SlimSelect(Select):
    template_name = "widgets/slim_select.html"

    def __init__(self, attrs=None, choices=(), create_url=None) -> None:
        super().__init__(attrs, choices)
        self.create_url = create_url

    def get_context(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context(*args, **kwargs)
        context["create_url"] = self.create_url
        return context


class MultipleSlimSelect(SelectMultiple):
    template_name = "widgets/slim_select.html"

    def __init__(self, attrs=None, choices=(), create_url=None) -> None:
        super().__init__(attrs, choices)
        self.create_url = create_url

    def get_context(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context(*args, **kwargs)
        context["create_url"] = self.create_url
        return context
