from django.db.models import Max


def get_last_index(model, **filter_kwargs):
    # Retrieves the highest assigned index for the model specified
    last_index = (
            model.objects
            .filter(**filter_kwargs)
            .aggregate(max_index=Max('index'))['max_index']
            or 0
    )
    return last_index
