from rest_framework.filters import BaseFilterBackend


class SearchFilterBackend(BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		search = request.query_params.get('search[value]')
		search_fields = getattr(view, "xd_content_search_fields", None)
		if search_fields and search and (search := search.strip()):
			search_fields = (search_fields
			                 if isinstance(search_fields, (list, tuple)) else
			                 (search_fields,))
			for field_name in search_fields:
				queryset = queryset.filter(**{
					field_name + "__icontains": search
				})
		return queryset
