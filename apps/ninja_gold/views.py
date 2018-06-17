from django.shortcuts import render, redirect
import random, datetime

def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'activity' not in request.session:
        request.session['activity'] = []
    return render(request, "ninja_gold/index.html")

def process_money(request):
    # establish variables
    winnings = {'casino': random.randrange(-50, 51), 'farm': random.randrange(10, 21), 'cave': random.randrange(5, 11), 'house': random.randrange(2, 6)}
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    building = request.POST['building']
    action = []

    # build content to pass to template
    if building and building != 'casino':
        action = ["<p class='green'>Earned {} golds from the {}! ({})</p>".format(winnings[building], building, now)]
    elif (building == 'casino') and (winnings[building] >= 0):
       action = ["<p class='green'>Entered a casino and won {} golds! ({})</p>".format(winnings[building], now)]
    elif (building == 'casino') and (winnings[building] < 0):
        action = ["<p class='red'>Entered a casino and lost {} golds! ({})</p>".format(abs(winnings[building]), now)]

    context = {
        "building": building, 
        "winnings": winnings[building], 
        "now": now,
    }

    # keep score and activities list
    request.session['gold'] = request.session['gold'] + winnings[building]
    request.session['activity'] = request.session['activity'] + action

    return render(request, "ninja_gold/index.html", context)

def reset(request):
    del request.session['gold']
    del request.session['activity']
    return redirect("/")