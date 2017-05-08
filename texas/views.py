from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from . models import User
# from . gamehandler import GameHandler
from . gamehandler import NoLimitHeadsUpTexasHandler as GameHandler

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
    GameHandler.start('agentname', username)
    context = {'username': username}

    return render(request, 'texas/play_no_limit_texas.html', context)


def update(request):
    logging.debug('update()')
    username = request.session.get('username', default=None)
    msg = GameHandler.receive(username)
    logging.debug(msg)
    d = None
    if msg:
        GameHandler.update_gamestate(username, msg)
        d = GameHandler.gamestate_to_dict(username)

    return JsonResponse(d, safe=False)


def action(request):

    action = request.GET['action']
    username = request.session.get('username', default=None)

    if action == 'update':
        print('action=update')
        msg = GameHandler.receive_msg(username)
        logging.debug(msg)
            
        GameHandler.update_gamestate(username, msg)
        d = GameHandler.gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)

    elif action == 'next':
        print("action=%s" % action)
        msg = GameHandler.receive_msg(username)
        GameHandler.reset_gamestate(username)
        GameHandler.update_gamestate(username, msg)
        d = GameHandler.gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)
        
    else:
        amount = request.GET['amount']
        context = {'action': action, 'amount': amount}
        print("context:", context)
        GameHandler.send_response(username, context)

        msg = GameHandler.receive_msg(username)
        GameHandler.update_gamestate(username, msg)
        d = GameHandler.gamestate_to_dict(username)
        logging.debug(d)
        return JsonResponse(d, safe=False)
   

def test(request):
    return render(request, 'texas/no_limit_texas.html', {})




