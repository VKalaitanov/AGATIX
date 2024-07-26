from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class InvoiceTypes(models.TextChoices):
    BANK = 'bank', _("Bank")
    CAPITALIST = 'capitalist', _("Capitalist")
    USDT = 'usdt', _("USDT")


def build_invoice(d: list, number, email, amount, invoice_type, created_at: datetime):
    d.append(Paragraph('INVOICE'))
    d.append(Paragraph(f'# {number}'))
    d.append(Spacer(1, 20))
    d.append(Paragraph('Agatix Story Limited'))
    d.append(Paragraph('Bank: STANDARD CHARTERED BANK (HONG KONG)'))
    d.append(Paragraph('SWIFT: SCBLHKHH'))
    d.append(Paragraph(f'Date: {created_at.strftime("%d.%m.%Y")}'))
    d.append(Paragraph('Account number: 47413608783'))
    d.append(Paragraph('Bank code: 003'))
    d.append(Paragraph('Branch code: 474'))
    d.append(Paragraph('Account location: Hong Kong SAR'))
    d.append(Paragraph(f'Bill To: {email}'))
    if invoice_type == InvoiceTypes.USDT.value:
        d.append(Paragraph('USDT TRC20: TPpj5Zh9UJ2ruR55VyMcfd1GAxL5xezA5Y'))
    elif invoice_type == InvoiceTypes.CAPITALIST.value:
        d.append(Paragraph(f'Capitalist: U13754983'))
    d.append(Spacer(1, 20))
    d.append(Paragraph(f'Subtotal: {amount}. Tax: 0%. Total: {amount}'))
    d.append(Spacer(1, 20))
    d.append(Paragraph('Agatix Story Limited'))
    d.append(Paragraph('UNIT 1603, 16TH FLOOR, THE L. PLAZA 367 - 375 QUEEN\'S ROAD'))
    d.append(Paragraph('CENTRAL SHEUNG WAN HK, Hong Kong,'))
    d.append(Paragraph('Hong Kong, 999077'))
    d.append(Paragraph('SEO: Vishnevetskii Konstantin'))
    return d


class Invoice(models.Model):
    user = models.ForeignKey('platform_main.User', on_delete=models.PROTECT)
    amount = models.IntegerField()
    type = models.CharField(choices=InvoiceTypes.choices)
    paid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def generate_pdf(self):
        buffer = BytesIO()
        SimpleDocTemplate(buffer, pagesize=A4, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6).build(
            build_invoice([], self.id, self.user.email, self.amount, self.type, self.created_at)
        )
        buffer.seek(0)
        return buffer

    def get_status(self) -> tuple:
        if self.paid:
            return 'paid', 'paid'
        return 'wait', 'waiting'
