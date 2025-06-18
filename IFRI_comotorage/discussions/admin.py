from django.contrib import admin
from .models import Discussion, Message

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'date_creation')
    search_fields = ('participants__email',)
    filter_horizontal = ('participants',)

    def get_participants(self, obj):
        return ", ".join([str(user.email) for user in obj.participants.all()])
    get_participants.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_expediteur', 'get_discussion', 'date_envoi')
    search_fields = ('expediteur__email', 'contenu')
    list_filter = ('date_envoi',)

    def get_expediteur(self, obj):
        return obj.expediteur.email
    get_expediteur.short_description = "Expéditeur"

    def get_discussion(self, obj):
        return obj.discussion.nom if hasattr(obj.discussion, 'nom') else f"Discussion #{obj.discussion.id}"
    get_discussion.short_description = "Discussion"
