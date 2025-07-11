from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile
from .forms import EditProfileForm, EditUserForm, CustomUserCreationForm


def home_view(request):
    return render(request, 'accounts/home.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            code = profile.generate_code()
            sent = send_mail(
                'Verify Your Account',
                f'Your verification code is: {code}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
            # Should return the number of successfully delivered messages
            print("Email sent?", sent)

            request.session['verify_user_id'] = user.id
            return redirect('verify_code')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        u_form = EditUserForm(request.POST, instance=request.user)
        p_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect('profile')
    else:
        u_form = EditUserForm(instance=request.user)
        p_form = EditProfileForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def verify_user(request):
    request.user.is_verified = True
    request.user.save()
    return redirect('profile')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(
            self.request, f"Welcome back, {self.request.user.username}!")
        return super().form_valid(form)


@login_required
def verify_code_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        code = request.POST.get('code')
        if profile.verification_code == code:
            profile.is_verified = True
            profile.verification_code = ''
            profile.save()
            messages.success(request, "✅ Email verified successfully.")
            return redirect('profile')
        else:
            messages.error(request, "❌ Incorrect code. Try again.")
    return render(request, 'accounts/verify.html')

@login_required
def resend_code_view(request):
    profile = request.user.profile
    code = profile.generate_code()
    send_mail(
        'Resend Verification Code',
        f'Your new verification code is: {code}',
        'no-reply@yourapp.com',
        [request.user.email],
        fail_silently=False,
    )
    messages.info(request, "📬 A new verification code has been sent to your email.")
    return redirect('verify_code')

