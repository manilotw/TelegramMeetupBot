from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=150)
    start_event = models.DateTimeField()
    end_event = models.DateTimeField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=150, unique=True)
    stack = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    card_num = models.CharField(
        max_length=12,  null=True, blank=True)
    tg_id = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name='sessions')
    title = models.CharField(max_length=150)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SpeakerSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE,
                                related_name='speaker_sessions')
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE,
                                related_name='speaker_sessions')
    topic = models.CharField(max_length=150)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()

    def __str__(self):
        return self.topic


class User(models.Model):
    tg_id = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(
        max_length=10, default='listener')

    def __str__(self):
        return f"{self.first_name} ({self.role})"


class Question(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE,
                                related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='questions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Question to {self.speaker.name} by user {self.user.first_name}'


class Organizer(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    card_num = models.IntegerField()
