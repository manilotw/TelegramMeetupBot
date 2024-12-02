from django.contrib import admin
from event_planner.models import Event, Speaker, Session, SpeakerSession, User, Question, Organizer
from event_planner.utils import get_schedule
from telebot import TeleBot
import os

# Получаем токен для бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')
    search_fields = ('name', 'location')
    list_filter = ('date',)
    ordering = ('date',)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'stack')
    search_fields = ('name', 'stack')
    ordering = ('name',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'event')
    search_fields = ('title', 'event__name')
    list_filter = ('event',)
    ordering = ('event__date',)


@admin.register(SpeakerSession)
class SpeakerSessionAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'topic',)
    search_fields = ('speaker__name', 'topic')
    ordering = ('session__event__date',)


@admin.action(description="Рассылка о изменении в расписании")
def send_massage_to_all_users(modeladmin, request, queryset):
    errors = []
    bot = TeleBot(TELEGRAM_BOT_TOKEN)
    users = User.objects.all()
    massage_text = get_schedule()

    for user in users:
        try:
            bot.send_message(user.tg_id, massage_text)
        except Exception as e:
            errors.append(f"Не удалось отправить сообщение пользователю {user.tg_id}: {str(e)}")
            print(f"Ошибка для {user.tg_id}: {str(e)}")
    modeladmin.message_user(
        request, "Сообщения отправлены всем пользователям!")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = [send_massage_to_all_users]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_speaker_name', 'created_at', 'get_user_first_name')
    search_fields = ('speaker__name', 'created_at')
    list_filter = ('speaker__name',)
    ordering = ('speaker__name',)

    # Метод для получения имени speaker
    def get_speaker_name(self, obj):
        return obj.speaker.name if obj.speaker else 'Не указано'
    get_speaker_name.admin_order_field = 'speaker__name'  # Позволяет сортировать
    get_speaker_name.short_description = 'Докладчик'

    # Метод для получения имени user
    def get_user_first_name(self, obj):
        return obj.user.first_name if obj.user else 'Не указано'
    get_user_first_name.admin_order_field = 'user__first_name'  # Позволяет сортировать
    get_user_first_name.short_description = 'Имя пользователя'


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('card_num',)
    list_filter = ('card_num',)
    ordering = ('card_num',)
