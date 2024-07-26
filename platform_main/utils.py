def clean_form_errors(form) -> dict:
    errors = {}
    for key, val in form.errors.as_data().items():
        errors[key] = [el.message for el in val]
    return errors
