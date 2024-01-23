from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.contrib import admin
from django.urls import include

urlpatterns = [
                  path('', views.home, name="home"),
                  path('about/', views.about, name="about"),
                  path('contact/', views.contact, name="contact"),
                  path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
                  path('category-title/<val>', views.CategoryTitle.as_view(), name="category-title"),
                  path('product-detail/<int:pk>', views.ProductDetail.as_view(), name="product-detail"),
                  path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path('delete/<int:id>', views.delete_view, name='delete'),
                  path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
                  path('create-view/', views.ProductView.as_view(), name='addproduct'),
                  path('updateProduct/<int:pk>', views.updateProduct.as_view()),

                  path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
                  path('accounts/login', auth_view.LoginView.as_view(template_name='app/login.html',
                                                                     authentication_form=LoginForm), name='login'),
                  path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',
                                                                               form_class=MyPasswordChangeForm,
                                                                               success_url='/passwordchangedone'),
                       name='passwordchange'),
                  path('passwordchangedone',
                       auth_view.PasswordResetDoneView.as_view(template_name='app/passwordchangedone.html'),
                       name='passwordchangedone'),
                  path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

                  path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
                                                                              form_class=MyPasswordResetForm),
                       name="password_reset"),
                  path('password-reset/done/',
                       auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
                       name="password_reset_done"),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
                                                                  form_class=MySetPasswordForm),
                       name="password_reset_confirm"),
                  path('password-reset-complete/',
                       auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
                       name="password_reset_complete"),
                  path('sendemail/', views.contactsendmail, name='contactpage'),
                  path('edit/<int:pk>', views.edit_profile.as_view(), name='admin_edit_profile'),
                  path('AdminUser/', views.AdminUser, name='AdminUser'),
                  path('all/', views.all, name='all'),
                  path('allUsers/', views.allUsers, name='all'),

                  path('insert/', views.insert, name='insert'),
                  path('insertUsers/', views.insertUsers, name='insert'),

                  path('<int:pk>/updateItems', views.updateItems, name='updateItems'),
                  path('<int:pk>/deleteItems', views.deleteItems, name='deleteItems'),
                  path('<int:id>/detail', views.detail, name='detail'),

                  path('allForClients', views.allForClients, name='allForClients'),
                  path('profile1', views.profile, name='profile1'),
                  path('UU', views.UU, name='UU'),
                  path('allEdit', views.allEdit, name='allEdit'),
                  path('<int:pk>/edit', views.edit, name='edit'),
                  path('search_books', views.search_books, name='search_books'),

                  path('AdminUser/<int:pk>/delete', views.updateOnlyUser, name='updateOnlyUser'),
                  path('item_list', views.item_list, name='item_list'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
