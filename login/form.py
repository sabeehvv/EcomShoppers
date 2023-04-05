from django import forms


class loginform(forms.Form):
    options = [
        ('password','Password'),
        ('otp','OTP'),
    ]
    phone_Number = forms.CharField(label='Phone Number',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Phone number"}))
    password = forms.CharField(label='Password',max_length=20, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
   # otp = forms.CharField(label='One Time Password', max_length=6, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"One Time Password",'autocomplete': 'off', 'id': 'otp_field'}))

