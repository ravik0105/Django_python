from django import forms
class AdminDateWidget(forms.DateInput):
    class Media:
        js = [
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js',
        ]

    def __init__(self, attrs=None, format=None):
        attrs = {'class': 'vDateField', 'size': '10', **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class AdminTimeWidget(forms.TimeInput):
    class Media:
        js = [
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js',
        ]

    def __init__(self, attrs=None, format=None):
        attrs = {'class': 'vTimeField', 'size': '8', **(attrs or {})}
        super().__init__(attrs=attrs, format=format)
