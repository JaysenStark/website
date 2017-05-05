from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from . models import User
from . gamehandler import GameHandler

import logging
import random


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, 
    filename='./texas/log/view_log.txt', filemode='w')

def index(request):
    return render(request, 'texas/index.html')

def login(request):
    name = request.POST['username']
    passwd = request.POST['password']
    print(name, passwd)

    res = User.objects.filter(username=name, password=passwd)
    context = {}

    if res:
        context = {'username': name}
        request.session['username'] = name
        return render(request, 'texas/choose.html', context)
    else:
        context['message'] = 'login failed!'
        return render(request, 'texas/index.html', context)

def logout(request):
    name = request.session['username']
    print('%s is about ot logout' % name)
    del request.session['username']
    return render(request, 'texas/index.html')

        
def start(request):
    username = request.session.get('username', default=None)
    GameHandler.start(username)
    context = {'username': username}

    return render(request, 'texas/play_no_limit_texas.html', context)

def update(request):
    logging.debug('update()')
    username = request.session.get('username', default=None)
    msg = GameHandler.advanced_receive(username)
    logging.debug(msg)
    d = None
    if msg:
        GameHandler.advanced_update_gamestate(username, msg)
        d = GameHandler.advanced_gamestate_to_dict(username)
        logging.debug('d')
        logging.debug(d)

    return JsonResponse(d, safe=False)


def action(request):

    action = request.GET['action']
    username = request.session.get('username', default=None)

    if action == 'update':
        print('action=update')
        msg = GameHandler.advanced_receive(username)
        logging.debug(msg)
            
        GameHandler.advanced_update_gamestate(username, msg)
        d = GameHandler.advanced_gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)

    elif action == 'next':
        print("action=%s" % action)
        msg = GameHandler.advanced_receive(username)
        GameHandler.advanced_reset_gamestate(username)
        GameHandler.advanced_update_gamestate(username, msg)
        d = GameHandler.advanced_gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)
        
    else:
        amount = request.GET['amount']
        context = {'action': action, 'amount': amount}
        print("context:", context)
        GameHandler.advanced_send_action(username, context)

        msg = GameHandler.advanced_receive(username)
        GameHandler.advanced_update_gamestate(username, msg)
        d = GameHandler.advanced_gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)
        
def test(request):
    return render(request, 'texas/no_limit_texas.html', {})




