from arim_library.models import IrbisData


class LibraryServices(object):

    @staticmethod
    def search_book(val):

        data = IrbisData.objects.filter(bib_disc__contains=val).values()[:100]

        return data
