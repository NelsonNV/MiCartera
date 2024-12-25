from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe


class BulmaFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        html = f"""
        <div class="file has-name is-right">
            <label class="file-label">
                <input class="file-input" type="file" name="{name}" {self.build_attrs(attrs)}>
                <span class="file-cta">
                    <span class="file-icon">
                        <i class="fas fa-upload"></i>
                    </span>
                    <span class="file-label">
                        {attrs.get('placeholder', 'Choose a file...')}
                    </span>
                </span>
            </label>
        </div>
        """
        return mark_safe(html)
