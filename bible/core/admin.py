from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url as r
from django.template.response import TemplateResponse
from django.urls import path

from bible.core.forms import IncludeVersiclesForm
from bible.core.models import Book, Versicle, Lection


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'chapters', 'testament', 'order']
    list_filter = ['testament']
    search_fields = ('name', 'abbreviation')

    def chapters(self, obj):
        versicles = obj.versicle_set.all()
        if versicles:
            last_chapter = versicles.last().chapter

            return last_chapter

        return 'N/A'

    chapters.short_description = 'capítulos'


class VersicleInlineModel(admin.TabularInline):
    model = Versicle
    extra = 1

    readonly_fields = ('book', 'chapter', 'number', 'text')


@admin.register(Versicle)
class VersicleModelAdmin(admin.ModelAdmin):
    list_display = ['versicle', 'book', 'chapter', 'number']
    list_filter = ['book__testament', 'book__name']
    list_per_page = 300

    search_fields = ('book__abbreviation', 'chapter')
    search_help_text = 'Formato da busca: 1jo 1.'

    def versicle(self, obj):
        return str(obj)

    versicle.short_description = 'versículo'


@admin.register(Lection)
class LectionModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/lection/changelist.html'

    inlines = [VersicleInlineModel]

    list_display = ['lection', 'books', 'chapters', 'order']
    search_fields = ('order__exact',)
    search_help_text = 'Buscar apenas pela ordem da leitura.'
    list_per_page = 20

    def lection(self, obj):
        return str(obj)

    lection.short_description = 'leitura'

    def books(self, obj):
        if books := obj.versicle_set.all().values_list(
            'book__name', flat=True).order_by('book__order').distinct():
                return ', '.join(books).title()

        return 'N/A'

    books.short_description = 'livros'

    def chapters(self, obj):
        versicles = obj.versicle_set.all()

        if versicles:
            books = versicles.values_list(
                'book__name', flat=True).order_by('book__order').distinct()

            display_chapters = ''
            for book in books:
                chapters = set(
                    versicles.filter(book__name=book).values_list(
                        'chapter', flat=True).order_by('chapter'))

                chapters = ', '.join(str(ch) for ch in sorted(chapters))
                if display_chapters:
                    display_chapters += ' - ' + chapters
                else:
                    display_chapters += chapters

            return display_chapters

        return 'N/A'

    chapters.short_description = 'capítulos'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('include/', self.admin_site.admin_view(self.include_versicles), name='core_lection_include_versicles'),
        ]
        return my_urls + urls

    def include_versicles(self, request):
        context = dict(self.admin_site.each_context(request),)
        lections = Lection.objects.all()

        context['old_testament'] = Book.objects.old_testament()
        context['new_testament'] = Book.objects.new_testament()
        context['lections'] = lections
        context['title'] = 'Incluir versículos na leitura'

        if request.method == 'POST':
            form = IncludeVersiclesForm(request.POST)
            context['form'] = form

            if not form.is_valid():
                self.message_user(
                    request, 'Erro ao incluir os versísculos na leitura.', messages.ERROR)
                return TemplateResponse(request, 'admin/lection/include_versicles.html', context)

            lection = Lection.objects.get(pk=form.cleaned_data.get('lection'))
            book = Book.objects.get(pk=form.cleaned_data.get('book'))

            init, final = form.cleaned_data.get('chapters').split('-')
            versicles = book.versicle_set.filter(
                chapter__gte=init, chapter__lte=final)

            for versicle in versicles:
                versicle.lection = lection

            Versicle.objects.bulk_update(versicles, ['lection'])

            self.message_user(
                request, 'Versísculos incluídos na leitura.', messages.SUCCESS)

            if '_addanother' in request.POST:
                return TemplateResponse(request, 'admin/lection/include_versicles.html', context)
            else:
                return HttpResponseRedirect(r('admin:core_lection_changelist'))

        context['form'] = IncludeVersiclesForm
        return TemplateResponse(request, 'admin/lection/include_versicles.html', context)
