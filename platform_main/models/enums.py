from django.utils.translation import gettext_lazy as _
from django.db import models


class Geo(models.TextChoices):
    UK = 'gb', _("United Kingdom")
    US = 'us', _("United States")
    ARGENTINA = 'ar', _("Argentina")
    AUSTRALIA = 'au', _("Australia")
    AUSTRIA = 'at', _("Austria")
    BELGIUM = 'be', _("Belgium")
    BRAZIL = 'br', _("Brazil")
    BULGARIA = 'bg', _("Bulgaria")
    CANADA = 'ca', _("Canada")
    CHILE = 'cl', _("Chile")
    CHINA = 'cn', _("China")
    COLOMBIA = 'co', _("Colombia")
    CROATIA = 'hr', _("Croatia")
    CZECH_REPUBLIC = 'cz', _("Czech Republic")
    DENMARK = 'dk', _("Denmark")
    ESTONIA = 'ee', _("Estonia")
    FINLAND = 'fi', _("Finland")
    FRANCE = 'fr', _("France")
    GERMANY = 'de', _("Germany")
    GREECE = 'gr', _("Greece")
    HUNGARY = 'hu', _("Hungary")
    INDIA = 'in', _("India")
    IRELAND = 'ie', _("Ireland")
    ISRAEL = 'il', _("Israel")
    ITALY = 'it', _("Italy")
    JAPAN = 'jp', _("Japan")
    LATVIA = 'lv', _("Latvia")
    LITHUANIA = 'lt', _("Lithuania")
    LUXEMBOURG = 'lu', _("Luxembourg")
    MALAYSIA = 'my', _("Malaysia")
    MEXICO = 'mx', _("Mexico")
    NETHERLANDS = 'nl', _("Netherlands")
    NEW_ZEALAND = 'nz', _("New Zealand")
    NIGERIA = 'ng', _("Nigeria")
    NORWAY = 'no', _("Norway")
    POLAND = 'pl', _("Poland")
    PORTUGAL = 'pt', _("Portugal")
    ROMANIA = 'ro', _("Romania")
    RUSSIA = 'ru', _("Russia")
    SAUDI_ARABIA = 'sa', _("Saudi Arabia")
    SINGAPORE = 'sg', _("Singapore")
    SLOVAKIA = 'sk', _("Slovakia")
    SLOVENIA = 'si', _("Slovenia")
    SOUTH_AFRICA = 'za', _("South Africa")
    SPAIN = 'es', _("Spain")
    SWEDEN = 'se', _("Sweden")
    SWITZERLAND = 'ch', _("Switzerland")
    THAILAND = 'th', _("Thailand")
    TURKEY = 'tr', _("Turkey")


class EmailType(models.TextChoices):
    NO_EMAIL = '0', _("No email")
    EMAIL = '1', _("Email")


class MobileOS(models.TextChoices):
    ANDROID = 'android', _("Android")
    IOS = 'ios', _("IOS")


class DesktopOS(models.TextChoices):
    WINDOWS = 'windows', _("Windows")
    LINUX = 'linux', _("Linux")
    MAC_OS = 'macos', _("MacOS")


class OperationalSystem(models.TextChoices):
    WINDOWS = 'windows', _("Windows")
    LINUX = 'linux', _("Linux")
    MAC_OS = 'macos', _("MacOS")
    ANDROID = 'android', _("Android")
    IOS = 'ios', _("IOS")


class Platform(models.TextChoices):
    DESKTOP = 'desktop', ("Desktop")
    MOBILE = 'mobile', ("Mobile")


class Format(models.TextChoices):
    POP = "pop", _("Pop")
    BANNER = "banner", _("Banner")
    REDIRECT = "redirect", _("Redirect")
