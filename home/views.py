from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
# Create your views here.


def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')
        
        if option == '1':
            game = Game.objects.filter(room_code = room_code).first()
            
            if game is None:
                messages.success(request , "Room code not found")
                return redirect('/')
            
            if game.is_over:
                messages.success(request , "Game is over")
                return redirect('/')
                        
            request.session['option']=option
            game.game_opponent = username
            game.save()
            return redirect('/play/' + room_code + '?username='+username) 
        else:
            request.session['option']=option
            game = Game(game_creator = username , room_code = room_code)
            game.save()       
            return redirect('/play/' + room_code + '?username='+username)     
            
    return render(request, 'home.html')


def play(request , room_code):
    username = request.GET.get('username')
    option =request.session['option']
    context = {'room_code' : room_code , 'username' : username ,'option': option}
    return render(request, 'play.html' , context)
