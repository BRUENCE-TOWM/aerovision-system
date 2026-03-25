from django import forms


class BootstrapFormMixin:
    """Apply Bootstrap-friendly classes without pushing logic into templates."""

    textarea_rows = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", self.textarea_rows)
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "form-select"
            else:
                css_class = "form-control"

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()
            widget.attrs.setdefault("placeholder", field.label)
            if name in self.errors:
                widget.attrs["class"] += " is-invalid"
