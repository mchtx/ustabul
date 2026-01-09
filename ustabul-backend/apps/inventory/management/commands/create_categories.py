from django.core.management.base import BaseCommand
from apps.inventory.models import PartCategory

# Kategoriler ve alt kategoriler
CATEGORIES = {
    'Motor': [
        'Piston', 'Segman', 'Krank', 'Yatak', 'Subap',
        'Radyatör', 'Termostat', 'Su Pompası'
    ],
    'Fren': [
        'Balata', 'Disk', 'Merkez', 'Kampana', 'Fren Hattı'
    ],
    'Elektrik': [
        'Alternatör', 'Marş Motoru', 'Buji', 'Bobine',
        'Ampul', 'Sigorta', 'Kablo'
    ],
    'Süspansiyon': [
        'Amortisör', 'Yay', 'Rot', 'Rotil', 'Burç', 'Takoz'
    ],
    'Debriyaj': [
        'Debriyaj Seti', 'Debriyaj Balatası', 'Baskı', 'Rulman'
    ],
    'Şanzıman': [
        'Vites Kutusu', 'Debriyaj Balatası', 'Yağ', 'Filtre'
    ],
    'Kaporta': [
        'Kapı', 'Çamurluk', 'Tampon', 'Kaput',
        'Bagaj Kapağı', 'Ayna'
    ],
    'Filtre': [
        'Hava Filtresi', 'Yağ Filtresi', 'Yakıt Filtresi', 'Kabin Filtresi'
    ],
    'Yağ & Sarf': [
        'Motor Yağı', 'Şanzıman Yağı', 'Fren Hidroliği',
        'Soğutma Sıvısı', 'Cam Sileceği'
    ],
}


class Command(BaseCommand):
    help = 'Ön tanımlı parça kategorilerini oluşturur'

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for category_name, subcategories in CATEGORIES.items():
            # Ana kategori (alt kategori olmadan)
            category, created = PartCategory.objects.get_or_create(
                name=category_name,
                subcategory='',
                defaults={'is_active': True}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Kategori oluşturuldu: {category_name}')
                )
            else:
                existing_count += 1

            # Alt kategoriler
            for subcategory in subcategories:
                subcat, created = PartCategory.objects.get_or_create(
                    name=category_name,
                    subcategory=subcategory,
                    defaults={'is_active': True}
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Alt kategori: {subcategory}')
                    )
                else:
                    existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Toplam {created_count} kategori oluşturuldu, '
                f'{existing_count} kategori zaten mevcuttu.'
            )
        )

