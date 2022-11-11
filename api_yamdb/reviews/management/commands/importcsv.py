from django.db.utils import IntegrityError
from django.core.management import BaseCommand, CommandError

from ._importcsv import import_csv


class Command(BaseCommand):
    """Импортер данных из csv."""

    help = 'Импорт данных csv из /static/data/ в базу данных.'

    def handle(self, *args, **kwargs):
        try:
            import_csv()
        except IntegrityError:
            raise CommandError(
                'Очистите базу данных перед загрузкой файлов csv,'
                ' воспользуйтесь менеджмент командой flush')
        except FileNotFoundError:
            raise CommandError(
                'Файлы csv в папке static/data не найдены')
        except Exception:
            raise CommandError(
                'Непредвиденная ошибка при выполнении команды importcsv,'
                ' обратитесь к разработчикам'
            )

        self.stdout.write(self.style.SUCCESS(
            'Все данные из csv файлов загружены в базу данных'
        ))
