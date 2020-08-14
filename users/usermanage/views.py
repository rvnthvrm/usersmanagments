from django import forms
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import (
    authentication,
    generics,
    permissions,
    response,
    views,
)
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .models import User
from .serializers import LoginSerializer, UserSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserDashboardView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'html/dashboard.html'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        if request.user.is_superuser:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(**{'is_superuser': request.user.is_superuser}).all()

        return response.Response({'users': [UserSerializer(user).data for user in queryset]})


class LogoutView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def post(self, request):
        logout(request)
        if request.accepted_renderer.format == 'html':
            return render(request, "html/login.html", {"form": LoginForm})

        return response.Response()


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'html/dashboard.html'

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.accepted_renderer.format == 'html':
            queryset = User.objects.all()
            return response.Response({'users': [UserSerializer(user).data for user in queryset]})

        return response.Response(serializer.data)

    def get(self, request):
        create_form = UserCreateForm()
        return render(
            request,
            "html/create.html",
            {"form": create_form}
        )

    def put(self, request):
        count = User.objects.filter(
            **{'{}__iexact'.format(User.USERNAME_FIELD): request.data['email']}
        )

        if not count:
            raise ValidationError('No user found for {} to update'.format(request.data['email']))

        if request.accepted_renderer.format == 'html':
            queryset = User.objects.all()
            return response.Response({'users': [UserSerializer(user).data for user in queryset]})

        return response.Response(request.data)


class ListUsersView(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'html/login.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            queryset = User.objects.all()
            return response.Response({'users': queryset})

        return response.Response([model_to_dict(i) for i in User.objects.all()])


@csrf_exempt
def user_login(request):
    return render(request, "html/login.html", {"form": LoginForm})
