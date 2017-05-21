from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import User, Category, Item
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json


# Create your views here.
def p_decorate(func):
    ''' decorator to check if there is a session or not.. if there is no session it loads login page else runs the request'''

    def func_wrapper(*args):

        if 'user_name' not in args[0].session and 'name' not in args[0].session:
            return render(args[0], 'item_catalog/login_signup.html')
        else:
            print("in else block")
            return func(*args)

    return func_wrapper


def home(request):
    '''
    This API is the landing page of the application
    '''
    dict = {}
    dict['items'] = getItems()
    dict['categories'] = getCategories()
    if 'user_name' in request.session and 'name' in request.session:
        dict['user_name'] = request.session['user_name']
        dict['name'] = request.session['name']


    return catalog_view(request, **dict)

def categoryitems(request, category):
    ''' returns items of a particular category'''
    category = category.strip().lower()
    if checkArguments(category):
        return render_message(request, "Please enter valid values for the post")
    dict = {}
    try:
        categoryid = Category.objects.get(name = category).category_id
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")
    if 'user_name' in request.session and 'name' in request.session:
        dict['user_name'] = request.session['user_name']
        dict['name'] = request.session['name']
    dict['categories'] = getCategories()
    dict['items'] = getItems(categoryid)
    dict['category'] = category
    return catalog_view(request, **dict)



def catalog_view(request, **kwargs):
    '''utility function for category items'''
    return render(request, 'item_catalog/application_success_page.html', kwargs)








def register(request):
    '''
    POST API which receives the request for registration.
    This API verifies that email and user name don't match with any other existing applicant,
    sets the user session details and redirects the user to login page .
    '''

    if request.POST:
        # Obtain form data from the request and store in session variables so they can be accessed across functions
        user_info = request.POST
        is_valid_user = True

        if User.objects.filter(email=user_info['email']).exists():
            is_valid_user = False
            error_message = "This email is already registered!"
            messages.add_message(request, messages.ERROR, error_message)
        if User.objects.filter(user_name=user_info['user_name']).exists():
            is_valid_user = False
            error_message = "This user name is already registered!"
            messages.add_message(request, messages.ERROR, error_message)

        if not is_valid_user:
            return render(request, 'item_catalog/login_signup.html')

        # If the user is valid, set the user session details
        request.session['name'] = user_info['name']
        request.session['email'] = user_info['email']
        request.session['user_name'] = user_info['user_name']
        email = user_info['email']
        pw_hash = make_password(user_info['password'], 'user_blog', hasher='default')
        print(pw_hash)
        name = user_info['name']
        user_name = user_info['user_name']
        user_blog = User(name=name, email=email, user_name=user_name, pw_hash=pw_hash)
        user_blog.save()
        error_message = "Successfully registered... Please Login to your account"
        messages.add_message(request, messages.SUCCESS, error_message)

        # Redirect the user to background check consent form
        return render(request, 'item_catalog/login_signup.html')


def logout(request):
    ''' deletes the session'''

    del request.session['name']
    del request.session['user_name']
    error_message = "Logout successful.."
    messages.add_message(request, messages.SUCCESS, error_message)
    return render(request, 'item_catalog/login_signup.html')

def signin(request):
    return render(request, 'item_catalog/login_signup.html')



def login(request):
    ''' handles the login request. If session already exists then renders the blow view request'''
    if request.POST:
        email = request.POST['email']
        password = make_password(request.POST['password'], 'user_blog', hasher='default')
        if (User.objects.filter(email=email, pw_hash=password).exists()):

            user_blog = User.objects.filter(email=email, pw_hash=password)[0]

            # Set the user's email in session
            request.session['user_name'] = user_blog.user_name
            request.session['name'] = user_blog.name
            categories = getCategories()
            items = getItems()
            return render(request, 'item_catalog/application_success_page.html',
                          {'name': request.session['name'], 'user_name': request.session['user_name'], 'categories': categories, 'items': items})
        else:
            messages.add_message(request, messages.ERROR, "Wrong email or password..")
            return render(request, 'item_catalog/login_signup.html')
    categories = getCategories()
    items = getItems()
    if 'user_name' in request.session and 'name' in request.session:
        return render(request, 'item_catalog/application_success_page.html',
                      {'name': request.session['name'], 'user_name': request.session['user_name'], 'categories': categories, 'items': items})
    else:

        return render(request, 'item_catalog/application_success_page.html',
                      {'categories': categories, 'items': items})





def render_message(request, error_message):
    ''' renders a view with  message'''

    messages.add_message(request, messages.ERROR, error_message)
    categories = getCategories()
    items = getItems()
    if 'user_name' in request.session and 'name' in request.session:
        return render(request, 'item_catalog/application_success_page.html',
                      {'name': request.session['name'], 'user_name': request.session['user_name'], 'categories': categories, 'items': items})
    else:
        return render(request, 'item_catalog/application_success_page.html',
                      {'categories': categories, 'items': items})




def getCategories():
    ''' returns list of all categories'''
    categories = [e.name for e in Category.objects.all().order_by('name')]
    return categories

def jsonprint(request):
    ''' returns json response'''

    report = getjsondata()
    return HttpResponse(json.dumps(report, indent=7), content_type="application/json")



def getjsondata():
    resultList = []
    categories = Category.objects.all()
    for category in categories:
        result ={}
        result['id'] = category.category_id
        result['name'] = category.name
        result['item'] = getItems(category.category_id)
        resultList.append(result)
    return resultList



def getItems(*args) :
    ''' get all the items if no parameter is passed. if category id is passed then get item details'''
    if len(args) == 0:
        items = Item.objects.all().order_by('created_at')
    if len(args) == 1:
        items = Item.objects.filter(category_id__category_id = args[0])

    resultList = []
    for item in items:
        result ={}
        result['title'] = item.title
        if len(args) == 0:
            result['category'] = item.category_id.name
        result['item_id'] = item.item_id
        result['title'] = item.title
        result['description'] = item.description
        if len(args) == 0:
            result['user_name'] = item.user_name.user_name
        resultList.append(result)
    print(resultList)

    return resultList


def edititem(request):
    ''' edit the item'''
    title = (request.POST['title']).strip().lower()
    oldtitle = (request.POST['oldtitle']).strip().lower()

    description = (request.POST['description']).strip()
    category = (request.POST['category']).strip()

    if checkArguments(title, description,category):
        return render_message(request, "Please enter valid values for the post")
    try:
        category_row = Category.objects.get(name = category)
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occurred")
    try:
        user_row = User.objects.get(user_name = request.session['user_name'])
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occurred")
    try:
        obj = Item.objects.get(title = oldtitle,category_id = category_row, user_name = user_row )
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occurred")

    obj.title = title
    obj.description = description
    try:
        obj.save()
    except ValueError:
        return render_message(request, "not valid ")

    return render_message(request,"Item updated successfully")



def additem(request):
    ''' add the item'''
    title = (request.POST['title']).strip().lower()
    description = (request.POST['description']).strip()
    category = (request.POST['category']).strip()

    if checkArguments(title, description,category):
        return render_message(request, "Please enter valid values for the post")
    try:
        category_row = Category.objects.get(name = category)
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")
    try:
        user_row = User.objects.get(user_name = request.session['user_name'])
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")





    obj = Item(title= title, category_id = category_row, description= description, user_name = user_row )
    try:
        obj.save()
    except ValueError:
        return render_message(request, "not valid ")





    return render_message(request,"Item saved successfully")


def deleteitem(request, category, item):
    ''' deletes confirmation page '''
    category = category.strip().lower()
    item = item.strip().lower()
    if checkArguments(category, item):
        return render_message(request, "Please enter valid values for the post")
    categories = getCategories()
    if category not in categories:
        return render_message(request, "Incorrect category entered")


    try:
        obj = Item.objects.get(title= item, category_id__name = category)
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")
    item ={}
    item['category'] = category
    item['title'] = obj.title
    return render(request,'item_catalog/delete_item.html', {'item': item})



def deleteitemconfirm(request, category, item):
    ''' deletes the item'''
    category = category.strip().lower()
    item = item.strip().lower()
    if checkArguments(category, item):
        return render_message(request, "Please enter valid values for the post")
    categories = getCategories()
    if category not in categories:
        return render_message(request, "Incorrect category entered")


    try:
        obj = Item.objects.get(title= item, category_id__name = category)
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")


    obj.delete()

    return render_message(request,"successfully deleted item")


def viewitem(request, category, item, function):
    category = category.strip().lower()
    item = item.strip().lower()
    if checkArguments(category, item):
        return render_message(request, "Please enter valid values for the post")
    categories = getCategories()
    if category not in categories:
        return render_message(request, "Incorrect category entered")


    try:
        obj = Item.objects.get(title= item, category_id__name = category)
    except ObjectDoesNotExist:
        return render_message(request, "sorry.. some error occured")
    item = {}
    item['title'] = obj.title
    item['description'] = obj.description
    item['category'] = category
    if function == 'view':
        item['function'] = 'view'
    if function == 'edit':
        item['function'] = 'edit'

    dict = {}
    print(request.session['user_name'])
    if 'user_name' in request.session and 'name' in request.session:
        dict['user_name'] = request.session['user_name']
        dict['name'] = request.session['name']
    dict['item'] = item

    return render(request,'item_catalog/view_item.html',dict)

def fbconnect(request):
    ''' handles fbconnect '''

    access_token = request.POST['access']

    #access_token = "EAAJ84HH6Mw4BAASJf6AaCi1YhT5ZBgewM4xanZBV4uyuZCOT5sgeK7qeZATySWiSv4IdKoFmDAPutQp6WPCxx2oPN6PQZCYbKeZC7AxYQcdP8e4XnMT2ZBuNM2aJFjZCyAnuLUS352AN9uALJZAMzofXYs36VxFMZCr2cGy4Sc0lTtNq9uLn6hAudnF9b10doADbcZD"
    print ("access token received %s " % access_token)
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    print("--------------\n")
    print(url)
    print("--------------\n")
    result = json.load(urllib2.urlopen(url))



    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.9/me"
    # strip expire tag from access token
    token = result['access_token']
    print(token)
    url ='https://graph.facebook.com/v2.9/me?fields=id%2Cname%2Cemail&access_token=' + token


    result = json.load(urllib2.urlopen(url))

    request.session['name'] = result["name"]
    request.session['user_name'] = result["email"]
    return JsonResponse({'success': 1})







def checkArguments(*args):
    ''' checks if arguments are none or empty.. '''
    check = False

    for i in args:
        if i is None or not i:
            check = True
    return check














