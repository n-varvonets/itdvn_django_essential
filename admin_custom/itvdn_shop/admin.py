from django.contrib import admin
from .models import TV, Notebook, Dishwasher, Brand, Category, VacuumCleaner, Item, Promo


# for model in [TV, Notebook, Dishwasher, Brand, Category, VacuumCleaner, Promo]:
#     admin.site.register(model)
class DishwasherInstanceInline(admin.TabularInline):
    model = Dishwasher


@admin.register(Brand)  # то же самое что и admin.site.register(Brand), но через декоратор
class BrandAdmin(admin.ModelAdmin):
    inlines = [DishwasherInstanceInline]  # очень удобная фича, которая позволяет изменять записи по ForeignKey,(сразу несколько
    # моделей которые подвязаны под один инстанс), например по бренду http://i.imgur.com/tRAYpAg.png


@admin.register(Dishwasher)
class DishwasherAdmin(admin.ModelAdmin):
    class Media:
        css = {}  # если хотим изменить внешний вид, то нужно указать путь к css

    list_display = ('model', 'brand_name', 'price',
                    'color', 'test_show_promo', 'colored_name')   # порядок отображения полей модели Dishwasher +
    # test_show_promo - это функция ниже, т.к. промо - это поле М2М +
    # colored_name - фунция что бы вывести цветной текст
    list_filter = ('price', 'brand_name', 'color',)
    fieldsets = (
        ('General info', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('brand_name', 'model'),
        }),
        ('Advanced options', {
            'classes': ('wide', 'extrapretty'),
            'description': ('Описание полей'),
            'fields': ('price', 'color'),
        }),)   # кастомное отображение полей, т.е. один тапл - одно строка в форме(http://i.imgur.com/03DRsOt.png)
    sortable_by = 'price'
    search_fields = ['brand_name__pk']  # зывает по какому полю проводить поиск записи модели
    # exclude = ('price',)
    empty_value_display = '-Без бренда-'
    readonly_fields = ['price']

    def test_show_promo(self, obj):
        """Функция для отображения поля М2М"""
        return obj.promo

    def delete_model(self, request, obj):
        """
        Можно изменить поведение удаления,
        в данном случае если ничего не использовать метод save(), то удаление не будет сохранено,
         т.е. не будет возможности удалить запись, хоть если мы и через ui удалим
        """
        pass

