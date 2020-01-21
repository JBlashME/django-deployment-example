from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# we are doing a lot of imports because we are using alot of djangos built in stuff. THis is all for login page
from django.urls import reverse
from django.contrib.auth.decorators import login_required   # if you ever want to a view that con only be seen while logged in you can decorate it with this login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    # This function is for people to log into their account
    if request.method == 'POST': #if the user submits something
        #we then get the user name and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # now we authenticate  the inputs  THIS IS A  BUILT IN DJANGO FUNCTION
        # you pass in what you want to authenticate EI is the input password = to the stored password in the data base.
        user = authenticate(username=username, password = password)

        if user:
            # we are checking if hte user is active. IF its a bot or something we would set the user to not active
            if user.is_active:
                #if all those things are true we pass in the request and then the authenticated object user
                login(request,user)
                #this return will redirect them to the home page
                return HttpResponseRedirect(reverse('index'))

            else: # so if their account is not active
                return HttpResponse("ACCOUNT IS NOT ACTIVE") #this will redicrect to a page and say this.
        else:
            print("Someone tried to log in and failed!")
            # so some one tried to log in incorrectly and this will return what the typed in and failed.
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html', {})

@login_required #this requires the user to be logged in
def special(request):
    return HttpResponse("you are logged in, Nice!")

#this @login_required decorates the entire view of user_logout so that the user needs to be logged in in order to log out
@login_required
def user_logout(request):
    #this function is for a user to log out
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# CTHis is all for registration
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    # WE CHECK TO SEE IF THE USER IS REGISTERED we just assume they are not so we write it to false.
    registered = False


    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)
        # in the above if we check to see if the form = post, if so we grab the information from the two forms

        # in this if statement we check to see if both forms are valid.
        if user_form.is_valid() and profile_form.is_valid():
            # if so we grab everything from the base user form and save it
            user = user_form.save()
            user.set_password(user.password) # this goes into settings.py and sets it as a hash
            user.save() # save to the data base
            # THen we grab everything from the and make sure there is a picture in it before we actually save it.
            profile = profile_form.save(commit = False)  # this commit = False does not save it to the data base yet it might overwrite the user
            profile.user = user   # this then sets it equal to the user from models

            #now we check to see if they uploaded a profile picture.
            if'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            # if there was an erroe we will print out the errors
            print(user_form.errors, profile_form.errors)
    else:
        #there was no request yet so we just set the form
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
# then we return the render
    return render(request, 'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})
