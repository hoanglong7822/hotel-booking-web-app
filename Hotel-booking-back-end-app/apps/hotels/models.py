from django.db import models
class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[
            ("country", "Country"),
            ("state", "State/Province"),
            ("city", "City"),
            ("district", "District"),
            ("ward", "Ward"),
        ]
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    ACCOMMODATION_TYPES = (
    ("hotel", "Hotel"),
    ("homestay", "Homestay"),
    ("villa", "Villa"),
    ("resort", "Resort"),
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Liên kết ForeignKey với Destination
    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hotels"
    )

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.FloatField(default=0)  # điểm đánh giá
    accommodation_type = models.CharField(
        max_length=20,
        choices=ACCOMMODATION_TYPES,
        default="hotel"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Amenity(models.Model):
    AMENITY_TYPES = (
        ("common", "Tiện nghi phổ biến"),
        ("unique", "Tiện nghi độc đáo"),
        ("room", "Tiện nghi phòng"),
    )

    name = models.CharField(max_length=255)
    amenity_type = models.CharField(
        max_length=20,
        choices=AMENITY_TYPES,
        default="common"
    )
    icon = models.CharField(max_length=255, blank=True, null=True)  # nếu muốn icon fontawesome
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_amenity_type_display()})"
class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    room_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)
    quantity = models.IntegerField(default=1)

    check_in_time = models.TimeField(default="14:00")
    check_out_time = models.TimeField(default="12:00")

    # Tiện ích nhiều loại
    amenities = models.ManyToManyField(
        Amenity,
        related_name='rooms',
        blank=True
    )

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hotel", "room_type"]

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"