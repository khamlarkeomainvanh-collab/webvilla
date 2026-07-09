"""
Developed By : somphone bounthanh

"""
from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home_view,name=''),
    path('webpush/', include('webpush.urls')), 
    path('admin/', admin.site.urls),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('queue', views.queue_view, name='queue'),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('add-qty/<int:pk>/', views.add_qty, name='add-qty'),
    path('remove-qty/<int:pk>/', views.remove_qty, name='remove-qty'),
    path('remove_qty_more/<int:pk>/', views.remove_qty_more, name='remove_qty_more'),
    
    path('remove-from-cart/<int:pk>/', views.remove_from_cart_view, name='remove-from-cart'),


    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),

    path('customersignup', views.customer_signup_view),
    path('ajax-send-otp', views.ajax_send_otp, name='ajax-send-otp'),
    path('ajax-verify-otp', views.ajax_verify_otp, name='ajax-verify-otp'),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('my-order', views.my_order_view,name='my-order'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),
    path('download-group-invoice/<int:orderID>', views.download_group_invoice_view, name='download-group-invoice'),
    path('expense-invoice', views.expense_invoice_view, name='expense-invoice'),
    path('revenue-invoice', views.revenue_invoice_view, name='revenue-invoice'),
    path('profit-invoice', views.profit_invoice_view, name='profit-invoice'),

    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('save-customization/<int:pk>', views.save_customization_view, name='save-customization'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),
    path('update-order-status/<int:id>/', views.update_order_status, name='update-order-status'),

    path('export-orders-excel', views.export_orders_excel, name='export-orders-excel'),
    path('export-orders-csv', views.export_orders_csv, name='export-orders-csv'),
    path('export-orders-pdf', views.export_orders_pdf, name='export-orders-pdf'),
    path('ajax-update-order-status/<int:pk>', views.ajax_update_order_status, name='ajax-update-order-status'),
    path('ajax-update-group-status', views.ajax_update_group_status, name='ajax-update-group-status'),
    path('ajax-delete-group', views.ajax_delete_group, name='ajax-delete-group'),
    path('ajax-order-detail/<int:pk>', views.ajax_order_detail, name='ajax-order-detail'),
    path('ajax-check-new-orders', views.ajax_check_new_orders, name='ajax-check-new-orders'),
    path('ajax-check-new-feedback', views.ajax_check_new_feedback, name='ajax-check-new-feedback'),
    path('ajax-queue-position', views.ajax_queue_position, name='ajax-queue-position'),
    path('ajax-item-statuses', views.ajax_item_statuses, name='ajax-item-statuses'),
    path('ajax-day-orders', views.ajax_day_orders, name='ajax-day-orders'),
    path('delete-feedback/<int:pk>', views.delete_feedback_view, name='delete-feedback'),
    path('admin-categories', views.admin_categories_view, name='admin-categories'),
    path('delete-category/<int:pk>', views.delete_category_view, name='delete-category'),
    path('export-products-excel', views.export_products_excel, name='export-products-excel'),
    path('export-customers-excel', views.export_customers_excel, name='export-customers-excel'),
    path('export-feedbacks-excel', views.export_feedbacks_excel, name='export-feedbacks-excel'),
    path('admin-finance', views.admin_finance_view, name='admin-finance'),
    path('add-expense', views.add_expense_view, name='add-expense'),
    path('delete-expense/<int:pk>', views.delete_expense_view, name='delete-expense'),
    path('admin-walkin-sale', views.admin_walkin_sale_view, name='admin-walkin-sale'),
    path('delete-walkin-sale/<int:pk>', views.delete_walkin_sale_view, name='delete-walkin-sale'),
    path('export-walkin-excel', views.export_walkin_excel_view, name='export-walkin-excel'),
    path('walkin-invoice', views.walkin_invoice_view, name='walkin-invoice'),
    path('export-finance-excel', views.export_finance_excel, name='export-finance-excel'),
    path('finance-month-data', views.finance_month_daily_data, name='finance-month-data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ຕື່ມ 2 ບັນທັດນີ້ໃສ່ທາງລຸ່ມສຸດ (ນອກວົງເລັບ urlpatterns)
if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)