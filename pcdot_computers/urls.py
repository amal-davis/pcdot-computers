from django.contrib import admin
from django.urls import path, include
from pcdotapp import views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('set_language/<str:language>/', views.set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('products/', views.products, name='products'),
    path('product/<slug:slug>/', views.product_page, name='product_page'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_product_type/', views.add_product_type, name='add_product_type'),
    path('delete_product_type/<int:delet_product_type>/', views.delete_product_type, name='delete_product_type'),
    path('edit_product_type/<int:edit_type>/', views.edit_product_type, name='edit_product_type'),
    path('add_category/', views.add_category, name='add_category'),
    path('p_delete_form/<int:pk>/', views.p_delete_form, name='p_delete_form'),
    path('add_product/', views.add_product, name='add_product'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('usercreate/', views.usercreate, name='usercreate'),
    path('login_page/', views.login_page, name='login_page'),
    path('signin/', views.signin, name='signin'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('cart_page/', views.cart_page, name='cart_page'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('category/<int:category_id>/', views.category_detail_view, name='category_detail_view'),
    path('search_results/', views.search_results, name='search_results'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_video/', views.add_video, name='add_video'),
    path('delete_video_section/<int:video>/', views.delete_video_section, name='delete_video_section'),
    path('logout/', views.logout, name='logout'),
    path('edit_video/<int:pk>/', views.edit_video, name='edit_video'),
    path('add_find_logo/', views.add_find_logo, name='add_find_logo'),
    path('edit_find_logo/<int:slide_id>/', views.edit_find_logo, name='edit_find_logo'),
    path('delete_find_logo/<int:slide_id>/', views.delete_find_logo, name='delete_find_logo'),
    path('remove_from_wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    path('product_type_view/<int:product_type_id>/', views.product_type_view, name='product_type_view'),
    path('payment_gateway/<int:order_id>/', views.payment_gateway, name='payment_gateway'),
    path('add_desktop_image/', views.add_desktop_image, name='add_desktop_image'),
    path('add_mobile_image/', views.add_mobile_image, name='add_mobile_image'),
    path('delete_desktop_image/<int:image_id>/', views.delete_desktop_image, name='delete_desktop_image'),
    path('delete_mobile_image/<int:image_id>/', views.delete_mobile_image, name='delete_mobile_image'),
    path('edit_desktop_image/<int:image_id>/', views.edit_desktop_image, name='edit_desktop_image'),
    path('edit_mobile_image/<int:image_id>/', views.edit_mobile_image, name='edit_mobile_image'),
    path('payment_process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('payment_redirect/<int:order_id>/', views.payment_redirect, name='payment_redirect'),
    path('orders/', views.order_page, name='order_page'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('setnewpassword/', views.setnewpassword, name='setnewpassword'),
    path('remove_from_session_cart/<int:product_id>/', views.remove_from_session_cart, name='remove_from_session_cart'),
    path('about_us',views.about_us,name='about_us'),
    path('warranty',views.warranty,name='warranty'),
    path('add_link',views.add_link,name='add_link'),
    path('edit_link/<int:link_id>/',views.edit_link,name='edit_link'),
    path('delete_link/<int:link_id>/',views.delete_link,name='delete_link'),
    path('p_delete_category/<int:pk>/',views.p_delete_category,name='p_delete_category'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
