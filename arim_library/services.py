from arim_library.models import IrbisData


class LibraryServices(object):

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def search_book(val):

        data = IrbisData.objects.filter(bib_disc__icontains=val).values()

        return data
