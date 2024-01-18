from django.contrib import admin
from .models import Site, Bot, Contact
from .forms import OwnedModelForm


from django.contrib import admin

admin.site.site_title = "Керування перевіками сайтів"

class OwnedControl(admin.ModelAdmin):
    form = OwnedModelForm
    def save_model(self, request, obj, form, change):
        # Записуємо поточного користувача як власника моделі при збереженні
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.is_user_owner(request.user)
        return super().has_change_permission(request, obj)

# Register your models here.
@admin.register(Site)
class SiteAdmin(OwnedControl):
    list_display = ('label_', 'url_', 'description_', 'is_active_')
    search_fields = ('label', 'url', 'description')
    # list_filter = ('created_at', 'updated_at')

    def label_(self, obj):
        return obj.label.upper()    
    label_.short_description = 'Назва'
    label_.admin_order_field = 'label'
    label_.allow_tags = True

    def url_(self, obj):
        return obj.url
    url_.short_description = 'Адреса'
    url_.admin_order_field = 'url'
    url_.allow_tags = True

    def description_(self, obj):
        return obj.description
    description_.short_description = 'Опис'
    description_.admin_order_field = 'description'
    description_.allow_tags = True

    def is_active_(self, obj):
        return "ТАК" if obj.checking_active else "НІ"
    is_active_.short_description = 'Активний'
    is_active_.admin_order_field = 'is_active'
    is_active_.allow_tags = True

    
    

@admin.register(Bot)
class BotSite(OwnedControl):
    list_display = ('label_', 'is_active_')
    search_fields = ('label',)

    def label_(self, obj):
        return obj.label.upper()
    label_.short_description = 'Назва'
    label_.admin_order_field = 'label'
    label_.allow_tags = True

    def is_active_(self, obj):
        return "ТАК" if obj.is_active else "НІ"
    is_active_.short_description = 'Активна'
    is_active_.admin_order_field = 'is_active'
    is_active_.allow_tags = True



@admin.register(Contact)
class Contact(OwnedControl):
    list_display = ('label_', 'contact_string_', 'is_active_')
    search_fields = ('label', 'contact_string')

    def label_(self, obj):
        return obj.label.upper()
    label_.short_description = 'Назва'
    label_.admin_order_field = 'label'
    label_.allow_tags = True

    def contact_string_(self, obj):
        return obj.contact_string
    contact_string_.short_description = 'Контакт'
    contact_string_.admin_order_field = 'contact_string'
    contact_string_.allow_tags = True

    def is_active_(self, obj):
        return "ТАК" if obj.is_active else "НІ"
    is_active_.short_description = 'Активний'
    is_active_.admin_order_field = 'is_active'
    is_active_.allow_tags = True
