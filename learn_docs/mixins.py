from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin:

    def get_object(self):
        queryset = self.get_queryset() # соглашаемся с queryset
        queryset = self.filter_queryset() # также соглашаемся с фильтрами
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): ## так достаем из lookup
                filter[field] = self.kwargs.get(field)
        obj = get_object_or_404(queryset, **filter)  # передаем фильтр для поиска
        self.check_object_permissions(self.request, obj)
        return obj