from event_planner.models import Event, Speaker, User, SpeakerSession
import os
import django
from django.utils.timezone import now
from pytz import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_backend.settings')


moscow_tz = timezone("Europe/Moscow")
current_moscow_time = now().astimezone(moscow_tz)


def get_schedule(): 
    moscow_tz = timezone("Europe/Moscow") 
    # работает только с московским временем 
    current_moscow_time = now().astimezone(moscow_tz) 
    event = Event.objects.filter(start_event__lte=current_moscow_time,  # ищет текущее мероприятие 
                                 end_event__gte=current_moscow_time).first() 
    if not event:  # если текущего мероприятия нет, находит ближайшее будущее мероприятие 
        event = Event.objects.filter( 
            start_event__gte=current_moscow_time 
        ).first() 
    if not event: 
        return "Нет текущих или предстоящих мероприятий" 
 
    schedule = ( 
        f'Мероприятие: {event} ' 
        f'{event.start_event.strftime("%H:%M")} - {event.end_event.strftime("%H:%M")}\n\n' 
    ) 
    sessions = event.sessions.all().order_by('start_session') 
 
    for session in sessions: 
        schedule += ( 
            f'• {session} ' 
            f'{session.start_session.strftime("%H:%M")} - {session.end_session.strftime("%H:%M")}\n' 
        ) 
        speaker_sessions = session.speaker_sessions.all().order_by('start_session') 
        for speaker_session in speaker_sessions: 
            schedule += ( 
                f'  - Доклад: {speaker_session} от {speaker_session.speaker.name} ' 
                f'{speaker_session.start_session.strftime("%H:%M")} - {speaker_session.end_session.strftime("%H:%M")}\n' 
            ) 
         
        schedule += '\n' 
    return schedule.strip()


def get_user_role(tg_id, username):
    """
    Определяет роль пользователя по Telegram ID (числовой) или username (строка с @).
    Возвращает 'speaker', 'listener', или None, если ничего не нашлось.
    """
    if Speaker.objects.filter(tg_id=f"@{username}").exists():
        return 'speaker'
    elif User.objects.filter(tg_id=tg_id).exists():
        return 'listener'
    return None


def remove_expired_speakers():
    speaker = SpeakerSession.objects.filter(
        end_session__lt=current_moscow_time).delete()
    return speaker
