from django.shortcuts import render, HttpResponse, redirect
from apps.first_app.models import *
from django.contrib import messages
import re
import hashlib

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# top table will be people who i clicked add friend.
# possible if statement that if
# bottom table will be friends table .exclude my name && .

def index(request):
    return render(request, 'first_app/index.html')

def delete(request, user_i):
    Friend.objects.get(id=user_i).delete()
    return redirect('/friends')

def viewfriend(request, user_i):
    context = {
        'user' : Friend.objects.get(id=user_i)
    }
    return render(request, 'first_app/viewfriend.html', context)

def user(request, user_i):

    context = {
        'user' : User.objects.get(id=user_i),
    }
    return render(request, 'first_app/user.html', context)

def add(request, user_i):
    print('-------------------going through add------------------')
    friend_to_add = User.objects.get(id=user_i)

    current_user = User.objects.get(id=request.session['user_id'])
    request.session['friend_name'] = friend_to_add.name
    request.session['friend_alias'] = friend_to_add.alias
    request.session['friend_email'] = friend_to_add.email
    print(friend_to_add.name)
    print(friend_to_add.alias)
    print(friend_to_add.email)

    Friend.objects.create(name = str(request.session['friend_name']), alias = str(request.session['friend_alias']), email=str(request.session['friend_email']), friend= current_user)


    # print(Friend.objects.all().values())

    # friend_to_add.friend_id = Friend.objects.create()

    return redirect('/friends')

def friends(request):
    print('*************GOING THROUGH FRIENDS')
    print(request.session['user_id'])
    print(User.objects.all().values())
    print('********************************')
    # print(Friend.objects.all().values())
    # print(request.session['alias'])
    print(Friend.objects.filter(friend_id= request.session['user_id']))

    context = {
        # this will be the query for the top table. where friend_id needs to equal the request session user id.
        'now_friends' : Friend.objects.filter(friend_id= request.session['user_id']),
        'not_yet_friends' : User.objects.exclude(email=request.session['email']),
    }
    return render(request, 'first_app/friends.html', context)

def register(request):
    print("***********going through REGISTER**********")

    if len(request.POST['reg_name']) < 3:
        print('Needs more than 3 characters for name')
        return redirect('/')
    elif len(request.POST['reg_alias']) < 3:
        print('Needs more than 3 characters for alias')
        return redirect('/')
    elif not EMAIL_REGEX.match(request.POST['reg_email']):
        print('Incorrect Email format')
        return redirect('/')

    elif User.objects.filter(email=str(request.POST['reg_email'])):
        print('This email already exists!!!')
        return redirect('/')
    elif len(request.POST['reg_password']) < 9:
        print('Password must be longer than 8 characters')
        return redirect('/')
    elif (request.POST['reg_password']) != (request.POST['reg_confirm_password']):
        print('Passwords did not match')
        return redirect('/')
    else:
        User.objects.create(name = request.POST['reg_name'], alias = request.POST['reg_alias'], email = request.POST['reg_email'], password = hashlib.md5(request.POST['reg_password'].encode('utf-8')).hexdigest(), dob = request.POST['reg_dateofbirth']),

        # Friend.objects.create(name = request.POST['reg_name'], alias = request.POST['reg_alias'], email = request.POST['reg_email'], password = hashlib.md5(request.POST['reg_password'].encode('utf-8')).hexdigest(), dob = request.POST['reg_dateofbirth'])

        alias_id = User.objects.filter(alias=request.POST["reg_alias"])[0]
        request.session['user_id'] = alias_id.id
        request.session['email'] = request.POST['reg_email']

        request.session['name'] = alias_id.name
        # this works right now
        print('__________The user_id logged in is: ', request.session['user_id'])
        print(User.objects.all().values())
        print('********************************')
        print(Friend.objects.all().values())

        return redirect('/friends')

def login(request):
    print("******going through LOGIN***********")
    # print(users.objects.filter(email__contains=request.POST['email']))


    if User.objects.filter(email = request.POST['login_email']):
        # print(User.objects.filter(alias=request.POST["login_alias"]))

        print(hashlib.md5(request.POST['login_password'].encode('utf-8')).hexdigest())

        alias_id = User.objects.filter(email=request.POST["login_email"])[0]
        password_id = User.objects.filter(password=hashlib.md5(request.POST['login_password'].encode('utf-8')).hexdigest())[0]



        print("_________The password_id is: ", password_id.id)

        if password_id.id == alias_id.id:
            request.session['user_id'] = alias_id.id
            request.session['email'] = request.POST['login_email']
            request.session['name'] = alias_id.name

            print('__________The user_id logged in is: ', request.session['user_id'])
            print(User.objects.all().values())
            print('********************************')
            print(Friend.objects.all().values())



            return redirect('/friends')
        else:
            return redirect('/')
    else:
        print('************************There is a problem with you login validation')

        return redirect('/')

def logout(request):
    print(User.objects.all().values())
    request.session.clear()
    return redirect('/')
