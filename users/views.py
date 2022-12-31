from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import  make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from PIL import Image,ImageOps
from urllib.request import urlopen
from django.core.files import File
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your views here.


class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer = loginserializer(data=data)
        if serializer.is_valid():
            email=serializer.data['email']
            password=serializer.data['password']

            user = authenticate(email=email,password=password)

            if user is None:
                return Response({
                "status":400,
                "message":"invalid email or password"
                })
            else:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        else:
            return Response({
                "status":400,
                "message":"invalid email or password"
            })

class RegisterAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = userserializer(data=data)
        if serializer.is_valid():
            email=serializer.data['email']
            password = make_password(serializer.data['password'])
            first_name =serializer.data['first_name']
            last_name =serializer.data['last_name']
            user =User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email=email,
                password=password,
                is_active=True
            )
            return Response({
                "status":200,
                "message":"registrartion successfull"
            })
        else:
            return Response({
                "status":400,
                "message":"something went wrong",
                "errors":serializer.errors
            })


class ImageConvertionAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        serializer = inputimageserializer(data=data)
        if serializer.is_valid():
            images=Images.objects.create(
                user=request.user,
                input_image=serializer.validated_data['input_image']
            )
            images.save()
            input_iamge_url = request.build_absolute_uri(images.input_image.url)

            ########################### a. Thumbnail (200x300)########################################

            out_thumb= Image.open(urlopen(input_iamge_url))
            out_thumb.thumbnail((200, 300))
            out_thumb_io =BytesIO()
            out_thumb.save(out_thumb_io, format='JPEG')
            thumbnail_file = InMemoryUploadedFile(out_thumb_io, None, 'thumbnail.jpg','image/jpeg',sys.getsizeof(out_thumb_io), None)
            images.Thumbnail.save('thumbnail.jpg', thumbnail_file)
            images.save()
            thumbnail_url = request.build_absolute_uri(images.Thumbnail.url)

            ############################### b. Medium(500x500) #######################################
            out_medium = Image.open(urlopen(input_iamge_url))
            medium =out_medium.resize((500,500),Image.Resampling.LANCZOS)
            medium_io=BytesIO()
            medium.save(medium_io,format='JPEG')
            medium_file = InMemoryUploadedFile(medium_io,None,'medium.jpg','images/jpeg',sys.getsizeof(medium_io),None)
            images.medium.save('medium.jpg',medium_file)
            images.save()
            medium_url =request.build_absolute_uri(images.medium.url)

            ############################## b. Large (1024x768)#############################################

            out_large = Image.open(urlopen(input_iamge_url))
            large=out_large.resize((1024,768),Image.Resampling.LANCZOS)
            large_io=BytesIO()
            large.save(large_io,format='JPEG')
            large_file = InMemoryUploadedFile(large_io,None,'large.jpg','images/jpeg',sys.getsizeof(large_io),None)
            images.large.save('large.jpg',large_file)
            images.save()
            large_url =request.build_absolute_uri(images.large.url)

            ################################# c. Grayscale################################################

            grayscale = Image.open(urlopen(input_iamge_url))
            gray_image = ImageOps.grayscale(grayscale)
            gray_image_io=BytesIO()
            gray_image.save(gray_image_io,format='JPEG')
            gray_image_file = InMemoryUploadedFile(gray_image_io,None,'grayimage.jpg','images/None/jpeg',sys.getsizeof(gray_image_io),None)
            images.grayscale.save('grayimage.jpg',gray_image_file)
            images.save()
            gray_image_url =request.build_absolute_uri(images.grayscale.url)

            gray_image.show()
            return Response({
                "input":input_iamge_url,
                "thumbnail":thumbnail_url,
                "medium":medium_url,
                "large":large_url,
                "grayimage":gray_image_url
            })