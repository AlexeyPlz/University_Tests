from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

POINTS = [(i, i) for i in range(11)]


class Level(models.TextChoices):
    EASY = 'Легкий'
    AVERAGE = 'Средний'
    HARD = 'Сложный'


class Type(models.TextChoices):
    VOCABULARY = 'Лексика'
    GRAMMAR = 'Грамматика'
    PHRASEOLOGY = 'Фразеология'
    VERBS = 'Глаголы'
    LEVEL = 'Тест уровня'


class Task(models.Model):
    text = models.CharField(max_length=100, null=False, blank=False, verbose_name='Текст')
    level = models.CharField(max_length=7, choices=Level.choices, default=Level.AVERAGE, verbose_name='Уровень')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='tasks', verbose_name='Автор')

    class Meta:
        ordering = ['id']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'{self.text} - {self.level} - {self.author}'


class Answer(models.Model):

    text = models.CharField(max_length=100, null=False, blank=False, verbose_name='Текст')
    point = models.IntegerField(choices=POINTS, default=5, verbose_name='Очки')
    is_right = models.BooleanField(null=False, blank=False, default=False, verbose_name='Правильный ли ответ')
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=False, blank=False, related_name='answers', verbose_name='Задание')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.text} - {self.point} - {self.is_right} - {self.task}'


class Test(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Заглавие')
    text = models.CharField(max_length=300, null=False, blank=False, verbose_name='Описание')
    type = models.CharField(max_length=11, choices=Type.choices, default=Type.LEVEL, verbose_name='Тип')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='tests', verbose_name='Автор')
    tasks = models.ManyToManyField(Task, related_name='tests', verbose_name='Задания')

    class Meta:
        ordering = ['id']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'{self.title} - {self.text} - {self.author}'


class Result(models.Model):
    points = models.IntegerField(null=False, blank=False, verbose_name='Набранные очки')
    date = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name='Дата')
    test = models.ForeignKey(Test, on_delete=models.PROTECT, null=False, blank=False, related_name='results', verbose_name='Тест')
    student = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='results', verbose_name='Ученик')

    class Meta:
        ordering = ['id']
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return f'{self.points} - {self.date} - {self.test} - {self.student}'


class ResultAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT, null=False, blank=False, related_name='result_answers', verbose_name='Ответ')
    result = models.ForeignKey(Result, on_delete=models.PROTECT, null=False, blank=False, related_name='result_answers', verbose_name='Результат')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ответ результата'
        verbose_name_plural = 'Ответы результата'

    def __str__(self):
        return f'{self.answer} - {self.result}'
