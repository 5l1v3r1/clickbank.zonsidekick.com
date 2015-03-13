# -*- coding: utf-8 -*-

from wtforms.compat import string_types
from wtforms.validators import DataRequired, StopValidation


class required(DataRequired):
    field_flags = ('required', )

    def __call__(self, form, field):
        if not field.data or (isinstance(field.data, string_types) and not field.data.strip()):
            field.errors[:] = []
            raise StopValidation('Invalid %(text)s' % {
                'text': field.label.text,
            })
