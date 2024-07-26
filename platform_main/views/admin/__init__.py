from .login import AdminLoginView
from .campaigns import AdminCampaignsView, AdminDeleteCampaignView, AdminCampaign, AdminCampaignAction, \
    AdminCreateCampaignView, TotalStatistics, AdminHomeView, AdminCampaignUpdate
from .accounts import AdminAccountsView, AdminDeleteAccountView, AdminAccountView, AdminStopAccount
from .sources import AdminSourcesView, AdminCreateSource, AdminUpdateSource, AdminDeleteSource
from .source_prices import AdminSourcesPriceView, AdminSourcesUpdate, AdminCreateSourcePrice, AdminDeleteSourcePrice
from .invoices import AdminListInvoices, AdminInvoiceAccept, AdminInvoiceDelete, AdminDownloadInvoice
