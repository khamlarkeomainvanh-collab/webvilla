from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0015_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='note',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
