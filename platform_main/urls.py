from django.urls import path
from platform_main.views.user import *
from platform_main.views.admin import *
from platform_main.views.integration import *
from platform_main.views.user.campaigns import get_statistic, get_min_price
from platform_main.views.user.register import ChangePassword
from platform_main.views.user.login import home_redirect

urlpatterns = [
    # User
    path('', home_redirect, name='start'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('campaigns/create/', CreateCampaignView.as_view(), name='campaigns_create'),
    path('campaigns/list/', ListCampaignsView.as_view(), name='campaigns_list'),
    path('campaigns/<int:campaign_id>/statistics', CampaignStatistics.as_view(), name='campaigns_statistics'),
    path('campaigns/<int:pk>/delete', DeleteCampaign.as_view(), name='campaigns_delete'),
    path('campaigns/<int:pk>/update', UpdateCampaign.as_view(), name='campaigns_update'),
    path('campaigns/<int:campaign_id>/<str:action>', CampaignAction.as_view(), name='campaigns_action'),
    path('campaigns/create/get_min_price', get_min_price),
    path('invoices/list', ListInvoices.as_view(), name='user_invoices_list'),
    path('invoices/create', CreateInvoice.as_view(), name='user_invoice_create'),
    path('invoices/download/<int:invoice_id>', DownloadInvoice.as_view(), name='user_invoice_download'),

    path('total_statistics', AllStatistics.as_view(), name='total_statistics'),
    path('get_statistic', get_statistic, name='get_statistic'),
    # Admin
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/statistics/', AllStatistics.as_view(), name='admin_total_statistics'),

    # Campaigns
    path('admin/campaigns/<int:campaign_id>/delete/', AdminDeleteCampaignView.as_view(), name='admin_campaign_delete'),
    path('admin/campaigns/list/', AdminCampaignsView.as_view(), name='admin_campaigns_list'),
    path('admin/campaigns/', AdminCreateCampaignView.as_view(), name='admin_campaign_create'),
    path('admin/home/', AdminHomeView.as_view(), name='admin_home'),
    path('admin/campaigns/<int:campaign_id>', AdminCampaign.as_view(), name='admin_campaign'),
    path('admin/campaigns/<int:campaign_id>/update', AdminCampaignUpdate.as_view(), name='admin_campaign_update'),
    path('admin/campaigns/<int:campaign_id>/start',
         AdminCampaignAction.as_view(action="start"),
         name='admin_campaign_action_start'),
    path('admin/campaigns/<int:campaign_id>/stop',
         AdminCampaignAction.as_view(action="stop"),
         name='admin_campaign_action_stop'),

    # Accounts
    path('admin/accounts/list/', AdminAccountsView.as_view(), name='admin_accounts_list'),
    path('admin/accounts/delete/<int:account_id>', AdminDeleteAccountView.as_view(), name='admin_account_delete'),
    path('admin/accounts/<int:account_id>', AdminAccountView.as_view(), name='admin_account'),
    path('admin/accounts/<int:account_id>/stop', AdminStopAccount.as_view(), name='admin_account_stop'),

    # Sources
    path('admin/sources', AdminSourcesView.as_view(), name='admin_sources_list'),
    path('admin/click_prices', AdminSourcesPriceView.as_view(), name='admin_sources_prices'),
    path('admin/sources_prices/create', AdminCreateSourcePrice.as_view(), name='admin_sources_prices_create'),
    path('admin/sources_prices/<int:source_price>/update',
         AdminSourcesUpdate.as_view(),
         name='admin_update_source_price'),
    path('admin/sources_prices/<int:pk>/delete',
         AdminDeleteSourcePrice.as_view(),
         name='admin_delete_source_price'),
    path('admin/sources/create', AdminCreateSource.as_view(), name='admin_create_source'),
    path('admin/sources/<int:pk>/edit', AdminUpdateSource.as_view(), name='admin_update_source'),
    path('admin/sources/<int:pk>/delete', AdminDeleteSource.as_view(), name='admin_delete_source'),

    # Invoices
    path('admin/invoices/<int:pk>/delete', AdminInvoiceDelete.as_view(), name='admin_delete_invoice'),
    path('admin/invoices/<int:pk>/accept', AdminInvoiceAccept.as_view(), name='admin_accept_invoice'),
    path('admin/invoices/list/', AdminListInvoices.as_view(), name='admin_list_invoices'),
    path('admin/invoices/<int:pk>/download', AdminDownloadInvoice.as_view(), name='admin_download_invoice'),

    # Integration
    path('integrations/campaigns', ActiveCampaigns.as_view(), name='integrations_list_campaigns'),
    path('change_password/', ChangePassword.as_view())

]
