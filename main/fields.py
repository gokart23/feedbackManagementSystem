from django import forms

class CustomListField(forms.Field):
    """
        Custom form field for ListField model field
    """

    def to_python(self, value):
        value = super(CustomListField, self).to_python(value)
        value = value.split(',')
        if not value:
            return None
        uni = [unicode(item) for item in value if item]
        if uni is None:
            uni = []
        return uni

    def widget_attrs(self, widget):
        attrs = super(CustomListField, self).widget_attrs(widget)
        attrs.update({'class': "custom-tag-input"})
        return attrs

    def prepare_value(self, value):
        if type(value) == list:
            val = ','.join(value)
        else:
            val = value
        return val

