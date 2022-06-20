from django.contrib import admin
from toons.models import Toon, Category, DisplayType, ToonImage, Work, Comment

# Register your models here

admin.site.register(Work)

class ToonInline(admin.StackedInline):
    model = ToonImage
    extra = 1

class ToonAdmin(admin.ModelAdmin):
    inlines = [ToonInline]

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('images'):
            obj.toonimage_set.create(images=afile)

admin.site.register(Toon, ToonAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class DisplayTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

admin.site.register(DisplayType, DisplayTypeAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment)