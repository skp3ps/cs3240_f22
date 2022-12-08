from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import requests, logging
from .models import Course, Book
from chat.models import Room
from django.contrib.auth.models import User
from .forms import BookForm
from .filters import BookFilter
from django.views.generic import ListView
from django.db.models import Q
from friendship.models import Friend, FriendshipRequest
import random, string


# Create your views here.

logger = logging.getLogger()

class BookListView(ListView):
    model = Book
    template_name = 'website/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def profile(request):
    requests = Friend.objects.unrejected_requests(user=request.user)
    all_friends = Friend.objects.friends(request.user)
    outgoing = Friend.objects.sent_requests(user=request.user)
    context = {'user': request.user, 'requests':requests, 'all_friends':all_friends, 'outgoing':outgoing}
    return render(request, 'website/profile.html', context)


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(pk=pk)
    if pk == request.user.pk:
        return redirect('profile')
    are_we_friends = Friend.objects.are_friends(request.user, other_user)
    sent = False
    for req in Friend.objects.sent_requests(user=request.user):
        if req.to_user == profile:
            sent = True
            break
    received = False
    for req in Friend.objects.sent_requests(user=other_user):
        if req.to_user == request.user:
            received = True
            break
    context = {'profile': profile, 'are_we_friends':are_we_friends, 'sent':sent, 'received':received}
    return render(request, 'website/profile_detail.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book, 'user': request.user}
    return render(request, 'website/book_detail.html', context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {'course':course, 'start_time': course.meetings_start_time[:5].replace('.', ':'), 'end_time': course.meetings_end_time[:5].replace('.', ':')}
    return render(request, 'website/course_detail.html', context)


# add book modified from https://openclassrooms.com/en/courses/6967196-create-a-web-application-with-django/7349525-create-model-objects-with-a-modelform
@login_required
def add_book(request, pk):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            try:
                book.course = Course.objects.get(pk=pk)
                book.save()
            except Course.DoesNotExist:
                logger.error('course pk from choose course does not exist')
            return redirect('profile')

    else:
        form = BookForm()

    return render(request,
                  'website/add_book.html',
                  {'form': form})


# edit book modified from https://openclassrooms.com/en/courses/6967196-create-a-web-application-with-django/7349667-update-a-model-object-with-a-modelform
@login_required
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = BookForm(instance=book)
    return render(request,
                  'website/add_book.html',
                  {'form': form})


@login_required
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        # redirect to the book list
        return redirect('profile')
    return render(request,
                  'website/delete_book.html',
                  {'book': book})

@login_required
def send_friend_request(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(id=pk)
    sent = False
    for req in Friend.objects.sent_requests(user=request.user):
        if req.to_user == profile:
            sent = True
    received = False
    for req in Friend.objects.sent_requests(user=other_user):
        if req.to_user == request.user:
            received = True
    if not sent:
        Friend.objects.add_friend(request.user, other_user)
    sent = True
    are_we_friends = False
    context = {'profile': profile, 'are_we_friends': are_we_friends, 'sent':sent, 'received':received}
    return render(request, 'website/profile_detail.html', context)

@login_required
def accept_friend_request(request, pk):
    other_user = User.objects.get(id=pk)
    if not (Friend.objects.are_friends(request.user, other_user)):
        friend_request = FriendshipRequest.objects.get(from_user=other_user, to_user=request.user)
        friend_request.accept()
    return redirect('profile')

@login_required
def accept_friend_request1(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(id=pk)
    if not (Friend.objects.are_friends(request.user, other_user)):
        friend_request = FriendshipRequest.objects.get(from_user=other_user, to_user=request.user)
        friend_request.accept()
    are_we_friends = True
    sent = False
    received = False
    context = {'profile': profile, 'are_we_friends': are_we_friends, 'sent': sent, 'received':received}
    return render(request, 'website/profile_detail.html', context)

@login_required
def remove_friend(request, pk):
    other_user = User.objects.get(id=pk)
    Friend.objects.remove_friend(other_user, request.user)
    return redirect('profile')

@login_required
def remove_friend1(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(id=pk)
    Friend.objects.remove_friend(other_user, request.user)
    are_we_friends = False
    sent = False
    received = False
    context = {'profile': profile, 'are_we_friends': are_we_friends, 'sent': sent, 'received': received}
    return render(request, 'website/profile_detail.html', context)

@login_required
def remove_request(request, pk):
    other_user = User.objects.get(id=pk)
    friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
    friend_request.accept()
    Friend.objects.remove_friend(request.user, other_user)
    return redirect('profile')

@login_required
def remove_request1(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(id=pk)
    first = True
    for req in Friend.objects.sent_requests(user=request.user):
        if req.to_user == profile:
            first = False
    if first:
        friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
        friend_request.accept()
        Friend.objects.remove_friend(request.user, other_user)
    are_we_friends = False
    sent = False
    received = False
    context = {'profile': profile, 'are_we_friends': are_we_friends, 'sent': sent, 'received': received}
    return render(request, 'website/profile_detail.html', context)

@login_required
def reject_request(request, pk):
    other_user = User.objects.get(id=pk)
    friend_request = FriendshipRequest.objects.get(from_user=other_user, to_user=request.user)
    friend_request.accept()
    Friend.objects.remove_friend(request.user, other_user)
    return redirect('profile')

@login_required
def reject_request1(request, pk):
    profile = get_object_or_404(User, pk=pk)
    other_user = User.objects.get(id=pk)
    first = False
    for req in Friend.objects.sent_requests(user=other_user):
        if req.to_user == request.user:
            first = True
            break
    if first:
        friend_request = FriendshipRequest.objects.get(from_user=other_user, to_user=request.user)
        friend_request.accept()
        Friend.objects.remove_friend(request.user, other_user)
    are_we_friends = False
    sent = False
    received = False
    print("deleted")
    print(first)
    context = {'profile': profile, 'are_we_friends': are_we_friends, 'sent': sent, 'received': received}
    return render(request, 'website/profile_detail.html', context)

@login_required
def favorite_book(request, pk):
    book = Book.objects.get(pk=pk)
    context = {'book': book, 'user': request.user}
    book.favorited_by.add(request.user)
    # redirect to the book list
    return render(request, 'website/book_detail.html', context)


@login_required
def remove_favorite(request, pk):
    book = Book.objects.get(pk=pk)
    book.favorited_by.remove(request.user)
    return redirect('profile')

@login_required
def remove_favorite1(request, pk):
    book = Book.objects.get(pk=pk)
    context = {'book': book, 'user': request.user}
    book.favorited_by.remove(request.user)
    return render(request, 'website/book_detail.html', context)


@login_required
def refresh_courses(request):
    DEPARTMENTS_URL = 'http://luthers-list.herokuapp.com/api/deptlist'
    r = requests.get(url=DEPARTMENTS_URL)
    departments = r.json()
    initial_count = Course.objects.count()
    first_run = Course.objects.count() < 500
    for department in departments:
        classes_url = 'http://luthers-list.herokuapp.com/api/dept/' + department['subject']
        r = requests.get(url=classes_url)
        courses = r.json()
        logging.info('department: ' + department['subject'])
        for entry in courses:
            try:
                course = Course.objects.get(semester_code=entry['semester_code'], subject=entry['subject'],
                                            catalog_number=entry['catalog_number'],
                                            course_section=entry['course_section'])
                if course.course_number != entry['course_number'] or course.instructor_name != entry['instructor'][
                    'name'] or course.instructor_email != entry['instructor']['email']:
                    logger.info(
                        'course update: ' + course.subject + course.catalog_number + '.' + course.course_section)
                    logger.info(str(course.course_number) + ' ' + str(entry['course_number']) + ' ' + str(
                        course.course_number == entry['course_number']))
                    logger.info(course.instructor_name + ' ' + entry['instructor']['name'] + ' ' + str(
                        course.instructor_name == entry['instructor']['name']))
                    logger.info(course.instructor_email + ' ' + entry['instructor']['email'] + ' ' + str(
                        course.instructor_email == entry['instructor']['email']))

                    course.course_number = entry['course_number']
                    course.instructor_name = entry['instructor']['name']
                    course.instructor_email = entry['instructor']['email']
                    course.save()
            except Course.DoesNotExist:
                if len(entry['meetings']) < 1:
                    continue
                course = Course(subject=entry['subject'],
                                semester_code=entry['semester_code'],
                                course_number=entry['course_number'],
                                course_section=entry['course_section'],
                                catalog_number=entry['catalog_number'],
                                instructor_name=entry['instructor']['name'],
                                instructor_email=entry['instructor']['email'],
                                description=entry['description'],
                                units=entry['units'],
                                component=entry['component'],
                                class_capacity=entry['class_capacity'],
                                wait_list=entry['wait_list'],
                                wait_cap=entry['wait_cap'],
                                enrollment_total=entry['enrollment_total'],
                                enrollment_available=entry['enrollment_available'],
                                meetings_days=entry['meetings'][0]['days'],
                                meetings_start_time=entry['meetings'][0]['start_time'],
                                meetings_end_time=entry['meetings'][0]['end_time'], 
                                facility_description=entry['meetings'][0]['facility_description'], 
                                )
                if not first_run:
                    logger.info('new course: ' + course.subject + course.catalog_number + '.' + course.course_section)
                course.save()
    logger.info('initial count: ' + str(initial_count) + '; final count: ' + str(Course.objects.count()))
    return redirect('/')


@login_required
def choose_course(request):
    if request.method == 'GET':
        args = {}
        entered = False
        for key, value in request.GET.items():
            if value and key == 'subject':
                args[key] = value.upper().strip()
                entered = True
            if value and key == 'semester_code':
                args[key] = value.strip()
                entered = True
            if value and key == 'course_number':
                args[key] = value.strip()
                entered = True
            if value and key == 'course_section':
                args[key] = value.strip()
                entered = True
            if value and key == 'catalog_number':
                args[key] = value.strip()
                entered = True
            if value and key == 'instructor_name':
                v = value.split()
                entered = True
                if len(v) >= 2:
                    value = v[0].capitalize() + " " + v[1].capitalize()
                else:
                    value = value.capitalize()
                args['instructor_name__contains'] = value
            if value and key == 'instructor_email':
                args[key] = value.lower().strip()
                entered = True
        courses = Course.objects.filter(**args)
        if len(courses) == 0:
            context = {'error_message': 'No courses match your selections.'}
        elif not entered:
            context = {'error_message': 'Please enter search criteria to filter available courses.'}
        elif len(courses) > 100:
            context = {'error_message': 'Too many courses match your selections. Please enter additional search criteria to see available courses.'}
        else:
            context = {'courses': courses}

        return render(request, 'website/choose_course.html', context)
    elif request.method == 'POST':
        return redirect('add_book', request.POST['course'])


@login_required
def chat(request, pk):
    user2 = get_object_or_404(User, pk=pk)
    room = Room.objects.filter(participants=request.user).filter(participants=user2).first()
    if room is None:
        names = [request.user.username, user2.username]
        names.sort()
        room = Room(name=names[0] + ' and ' + names[1] + ' chatroom',
                    description='A private chat between ' + names[0] + ' and ' + names[1] + '.',
                    slug=''.join(random.choice(string.ascii_lowercase) for i in range(20))
                    )
        room.save()
        room.participants.add(request.user, user2)
    return redirect('room_detail', slug=room.slug)


def search(request):
    context = {}
    if request.POST.get('key'):
        key = request.POST.get('key')
        logger.info('search term: ' + key)
        two = False
        if len(key.split()) == 2:
            subj = key.split()[0]
            num = key.split()[1]
            two = True
        context['books'] = Book.objects.filter( Q(title=key) |
                                                Q(title__icontains=key) |
                                                Q(isbn=key) |
                                                Q(isbn__icontains=key))
        context['profiles'] = User.objects.filter(Q(username=key) |
                                                    Q(username__contains=key))
        if two:
            context['courses'] = Course.objects.filter(Q(instructor_name=key) | 
                                                    Q(instructor_email=key) |
                                                    Q(subject=subj.upper(), catalog_number=int(num)))
            logger.info(context['courses'])
        else:
            context['courses'] = Course.objects.filter(Q(instructor_name=key) | 
                                                    Q(instructor_email=key) |
                                                    Q(subject=key.strip().upper()))
    else:
        context['nosearch'] = True

    return render(request, 'website/search.html', context)
