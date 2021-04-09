from django.shortcuts import get_object_or_404, render, redirect
from .models import Review, User, Ticket, UserFollows
from .forms import RegisterForm,LoginForm, CreateTicketForm, FollowUser, CreateReviewForm,UpdateTicketForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import CharField, Value, Q
from itertools import chain


@csrf_exempt
def index(request):
  
    if request.method == "POST":
        
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username = username, password = password)
        if username is not None or password is not None:
            if user is not None:
                login(request, user)
                return redirect("dashbord")
            else:
                messages.error(request, 'Identifiants incorrects')
                return redirect("dashbord")
    else: 
        form = LoginForm()
        return render(request, 'user/login.html',{'form': form} )
    
@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None) 
            password = form.cleaned_data.get('password', None)
            user = User()
            user.username = username
            user.password= make_password(password)
            user.save()
            
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request,'user/register.html', {'form': form})

@csrf_exempt      
def dashbord(request):
    
    if request.user.is_authenticated:
        liste = [ item.followed_user.id for item in UserFollows.objects.filter(user = request.user)]
        review_by_user = [ item.id for item in Ticket.objects.filter(user = request.user)]
        reviews =  Review.objects.filter(Q(user_id__in = liste) | Q(user_id= request.user) |Q(ticket_id__in= review_by_user) )
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets =  Ticket.objects.filter(Q (user_id= request.user.id) | Q(user_id__in = liste))
        tickets= tickets.annotate(content_type=Value('TICKET', CharField()))
        id_tickets = [ item.ticket_id for item in Review.objects.all()]
        all_tickets =Ticket.objects.all()
        # combine and sort the two types of posts
        posts = sorted(
            chain(tickets, reviews), 
            key=lambda post: post.time_created, 
            reverse=True
        )
        
        return render(request,'dashbord/dashbord.html', {'posts': posts, 'tickets':tickets, 'id_tickets':id_tickets, 'all_tickets':all_tickets  })
    else: 
       
        return redirect('index')
      
@csrf_exempt
def createTicket(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            form = CreateTicketForm(request.POST,request.FILES)
            if form.is_valid(): 
                ticket = form.save(commit=False)
                ticket.user_id = request.user.id
                ticket.save()   
                return redirect('dashbord')
        else:
            form = CreateTicketForm()
        return render(request,'dashbord/newticket.html', {'form': form})
    else:
        return redirect('index')
    
@csrf_exempt
def subscription(request):
    users = [ item.username for item in User.objects.all()]
    if request.user.is_authenticated:
        
        if request.method == "POST":
            form = FollowUser(request.POST)
            if form.is_valid(): 
                user = form.cleaned_data.get('follow', None)
                if user not in users:
                    return redirect('subscription')
                pk = User.objects.get(username=user).pk
                follow = UserFollows()
                follow.user_id = request.user.id
                follow.followed_user_id = pk
                follow.save()
                return redirect('subscription')

        else:
            form = FollowUser()
            user = UserFollows.objects.filter(user_id=request.user.id)
            follower = UserFollows.objects.filter(followed_user_id=request.user.id)
            return render(request,'subscription/subscription.html', {'form': form, 'user' :user, 'follower': follower})
    else:
        return redirect('index')

@csrf_exempt
def unsubscription(request, id):
    if request.user.is_authenticated:
        UserFollows.objects.filter(user_id=request.user.id, followed_user_id=id ).delete()
        return redirect('subscription')
    else:
        return redirect('index')

@csrf_exempt
def createReview(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateTicketForm(request.POST, request.FILES)
            review = CreateReviewForm(request.POST)
            if form.is_valid(): 
                ticket = form.save(commit=False)
                review = review.save(commit=False)
                ticket.user_id = request.user.id
                review.user_id = request.user.id
                review.ticket_id = ticket.id
                review.rating = request.POST.get('rating')
                ticket.save()
                review.ticket_id = ticket.id
                review.save()
                return redirect('dashbord') 
        else: 
            form = CreateTicketForm()
            review= CreateReviewForm()
            return render(request,'dashbord/newreview.html', {'form': form, 'review':review})   

        return redirect('index')
    
@csrf_exempt
def answerTicket(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            # ticket = CreateTicketForm(request.POST)
            form = CreateReviewForm(request.POST)
            
            if form.is_valid(): 
                url = request.META.get("HTTP_REFERER")
                url = url.split("/")[5].replace("?", "")
                review = form.save(commit=False)
                review.user_id = request.user.id
                review.ticket_id = url
                review.save()
                return redirect('dashbord') 

        else:
            tickets =  Ticket.objects.get(pk= id)
            review= CreateReviewForm()
            return render(request, 'dashbord/answerticket.html',{'review':review,'ticket':tickets, 'id':id})
    return redirect('index')

@csrf_exempt    
def post(request):
    if request.user.is_authenticated:    
        # review_by_user = [ item.id for item in Ticket.objects.filter(user = request.user)]
        ticket_answer = [ item.ticket_id for item in Review.objects.filter(user = request.user)]
        my_tickets =  Ticket.objects.filter( user_id= request.user.id) 
        my_tickets = my_tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews =  Review.objects.filter( user_id= request.user)  
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets =  Ticket.objects.filter(Q (user_id= request.user.id) | Q(id__in= ticket_answer))
        tickets= tickets.annotate(content_type=Value('REVIEW', CharField()))
        
        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, my_tickets), 
            key=lambda post: post.time_created, 
            reverse=True
        )
        
        return render(request,'post/post.html', {'posts': posts, 'tickets':tickets})
    return redirect('index')

@csrf_exempt
def editTicket(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Ticket, pk=id)
        ticket= UpdateTicketForm(request.POST or None,request.FILES or None, instance=post)
        if request.method == "POST":
            if ticket.is_valid(): 
                ticket.save()
                return redirect('post') 

        else:
            form = UpdateTicketForm( instance = post)
            return render(request, 'post/edit_ticket.html',{'form':form, 'post': post, 'id':id})
    return redirect('index')

@csrf_exempt
def editReview(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Review, pk=id)
        review= CreateReviewForm(request.POST or None,request.FILES or None, instance=post)
        ticket_answer = [ item.ticket_id for item in Review.objects.filter(user = request.user)]
        tickets =  Ticket.objects.filter(Q (user_id= request.user.id) | Q(id__in = ticket_answer))
        if request.method == "POST":
            if review.is_valid(): 
                review.save()
                return redirect('post') 

        else:
            form = CreateReviewForm( instance = post)
            return render(request, 'post/edit_review.html',{'form':form, 'post': post, 'tickets':tickets, 'id':id})
    return redirect('index')

@csrf_exempt
def deleteTicket(request, id):
    if request.user.is_authenticated:
        Ticket.objects.filter(id=id).delete()
        return redirect('post')
    return redirect('index')

@csrf_exempt
def deleteReview(request, id):
    if request.user.is_authenticated:
        Review.objects.filter(id=id).delete()
        return redirect('post')
    return redirect('index')
    
