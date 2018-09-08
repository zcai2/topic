from django.shortcuts import render
from django.http import Http404 , JsonResponse
import ast , json
from pprint import pprint


from bookDisplayer.models import TocBookTopic , BookTopicInfo , TocTopic , TocFreq , BookInfo , DescriptBookTopic , DescriptTopic , ClassInfo , ModelInfo,JobCon,JobDes, JobInfo

## basic returns
def index(request):
    model_field = ModelInfo.objects.using('database').all()[0]

    return  render(request,'bookDisplayer/index.html' , {
        'model_field' : model_field,
        })

def about(request):
    return render(request,'bookDisplayer/about.html')


## Visuals Currently : circle packer and tree_node
def circle_packer(request):
    temp = request.GET.get('dept_search') 

    if temp is None or temp == "All":
        temp = "All"

    depart = temp
    dept_course = ClassInfo.objects.using('database').all()
    dept_list = []
    for course in dept_course:
        dept = course.dept_course.split(" ")[0]

        if dept not in dept_list:
            dept_list.append(dept)
    dept_list.sort()
    dept_list.insert(0,"All Courses")
    return render(request , 'bookDisplayer/circle-packer.html', {
        'dept_list' : dept_list,
        'department' : temp,
        })

def tree_node(request):
    temp = request.GET.get('dept_search') 

    if temp is None or temp == "All":
        temp = "All"

    depart = temp
    dept_course = ClassInfo.objects.using('database').all()
    dept_list = []
    for course in dept_course:
        dept = course.dept_course.split(" ")[0]

        if dept not in dept_list:
            dept_list.append(dept)
    dept_list.sort()
    dept_list.insert(0,"All Courses")
    return render(request , 'bookDisplayer/tree-node.html', {
        'dept_list' : dept_list,
        'department' : temp,
        })

## loads json for the visuals
def load_json(request , department):

    dept_selection = department

    json_dict = {
     "name": department,
     "children": 
        [
     ]
    }

    if dept_selection != "All":
        course_list = ClassInfo.objects.using('database').filter(dept_course__regex=r"^"+dept_selection+" ")    
    else:
        course_list = ClassInfo.objects.using('database').all()


    for course in course_list:
        book_list = ast.literal_eval(course.associated_books)
        json_dict['children'].append(
            {
                'name' : course.dept_course,
                'children' : [],
            }
            )
            
        for book in book_list:
            title = book[0]
            isbn = book[1]
            course_index = 0
            for idx , entry in enumerate(json_dict['children']):
                
                if entry['name'] == course.dept_course:
                    course_index = idx
                    break


            json_dict['children'][course_index]['children'].append(
                {
                    'name':title,
                    'isbn':isbn,
                    'children':[]
                })

            topic_list = TocBookTopic.objects.using('database').filter(isbn = isbn)

            for topic in topic_list:
                distrib = ast.literal_eval(topic.topic_distribution)
                distrib = int(round(distrib * 100)) * 100
                book_index = 0
                for idx , entry in enumerate(json_dict['children'][course_index]['children']):
                
                    if entry['isbn'] == isbn:
                        book_index = idx
                        break

                json_dict['children'][course_index]['children'][book_index]['children'].append(
                {
                    'name':topic.topic_words,
                    'size':distrib,
                    'group':topic.topic_id,
                })

    return JsonResponse(json_dict, safe = False)

def load_json_treenode(request , department):

    dept_selection = department

    json_dict = {
     "nodes": []
    }

    return JsonResponse(json_dict, safe = False)

## About pages, features a searchbar
def toc_about(request):
    results=None
    topics = TocBookTopic.objects.using('database').order_by("-topic_distribution")
    book_topic_info = BookTopicInfo.objects.using('database').all()
    if request.GET.get('title_search') or request.GET.get('isbn_search') or request.GET.get('distr_search') or request.GET.get('words_search'):
        title_search = request.GET.get('title_search')
        isbn_search = request.GET.get('isbn_search')
        distr_search = request.GET.get('distr_search')
        words_search = request.GET.get('words_search')

        results = BookInfo.objects.using('database').filter(title__contains=title_search , 
            isbn__contains = isbn_search,
         )

    return render(request,'bookDisplayer/toc-about.html', {
        'results' : results,
        'toc_books' : topics,
        'book_topic_info':book_topic_info,
        })

def descript_about(request):
    results=None
    topics = DescriptBookTopic.objects.using('database').order_by("-topic_distribution")
    book_topic_info = BookTopicInfo.objects.using('database').all()
    if request.GET.get('title_search') or request.GET.get('isbn_search') or request.GET.get('distr_search') or request.GET.get('words_search'):
        title_search = request.GET.get('title_search')
        isbn_search = request.GET.get('isbn_search')
        distr_search = request.GET.get('distr_search')
        words_search = request.GET.get('words_search')

        results = BookInfo.objects.using('database').filter(title__contains=title_search , 
            isbn__contains = isbn_search,
         )

    return render(request,'bookDisplayer/descript-about.html', {
        'results' : results,
        'toc_books' : topics,
        'book_topic_info':book_topic_info,
        })

def classes_about(request):
    classes = ClassInfo.objects.using('database').all()
    descript_books = DescriptBookTopic.objects.using('database').order_by("-topic_distribution")
    toc_books = TocBookTopic.objects.using('database').order_by('-topic_distribution')
    book_topic_info = BookTopicInfo.objects.using('database').all()
    results = None
    if request.GET.get('tag_search') and request.GET.get('num_search'):
        tag_search = request.GET.get('tag_search').upper()
        num_search = request.GET.get('num_search')
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^"+tag_search+" " + num_search+ "$" ).order_by("dept_course")

    elif request.GET.get('tag_search'):
        tag_search = request.GET.get('tag_search').upper()
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^"+tag_search+" ").order_by("dept_course")

    elif request.GET.get('num_search'):
        num_search = request.GET.get('num_search')
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^[a-zA-Z]* " + num_search +"$").order_by("dept_course")

    return render(request, 'bookDisplayer/classes-about.html' , {
        'classes' : classes,
        'descript_books' : descript_books,
        'toc_books' : toc_books,
        'book_topic_info':book_topic_info,
        'results' : results,
        })

def job_search(request):
    classes = ClassInfo.objects.using('database').all()
    jobs_con = JobCon.objects.using('database').all().order_by("-Similarity")
    jobs_des = JobDes.objects.using('database').all().order_by("-Similarity")
    all_jobs = JobInfo.objects.using('database').all()
    results = None
    if request.GET.get('tag_search') and request.GET.get('num_search'):
        tag_search = request.GET.get('tag_search').upper()
        num_search = request.GET.get('num_search')
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^"+tag_search+" " + num_search+ "$" )

    elif request.GET.get('tag_search'):
        tag_search = request.GET.get('tag_search').upper()
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^"+tag_search+" ")

    elif request.GET.get('num_search'):
        num_search = request.GET.get('num_search')
        results = ClassInfo.objects.using('database').filter(dept_course__regex=r"^[a-zA-Z]* " + num_search +"$")

    return render(request, 'bookDisplayer/job-search.html' , {
                  'classes' : classes,
                  'jobs_con' : jobs_con,
                  'jobs_des' : jobs_des,
                  'alljobs': all_jobs,
                  'results' : results,
                  })
    


def job_about(request):
    classes = ClassInfo.objects.using('database').all()
    jobs = JobCon.objects.using('database').all().order_by("-Similarity")
    all_jobs = JobInfo.objects.using('database').all()

    return render(request, 'bookDisplayer/job-about.html' , {
                  'classes' : classes,
                  'jobs' : jobs,
                  'alljobs': all_jobs,
                  })
    



## Massive page loading, basically an index
def classes(request):
    classes = ClassInfo.objects.using('database').all()
    descript_books = DescriptBookTopic.objects.using('database').order_by("-topic_distribution")
    toc_books = TocBookTopic.objects.using('database').order_by('-topic_distribution')
    return render(request, 'bookDisplayer/classes.html' , {
        'classes' : classes,
        'descript_books' : descript_books,
        'toc_books' : toc_books,
        })

# By books
def descript_books(request):
    books = BookTopicInfo.objects.using('database').order_by("-id")
    topics = DescriptBookTopic.objects.using('database').order_by("-topic_distribution")
    books_info = BookInfo.objects.using('database').all()
    return  render(request,'bookDisplayer/descript_books.html' , {
            'books' : books,
            'topics' : topics,
            'books_info' : books_info,
        })

# by topics
def descript_topics(request):
    books = DescriptBookTopic.objects.using('database').exclude(id = -1).order_by("-topic_distribution")
    topics = DescriptTopic.objects.using('database').order_by("-book_count")
    return  render(request,'bookDisplayer/descript_topics.html' , {
            'books' : books,
            'topics' : topics,
        })

# by books
def toc_books(request):
    books = BookTopicInfo.objects.using('database').order_by("-toc_topic_count")
    topics = TocBookTopic.objects.using('database').order_by("-topic_distribution")
    books_info = BookInfo.objects.using('database').all()
    return  render(request,'bookDisplayer/toc_books.html' , {
            'books' : books,
            'topics' : topics,
            'books_info' : books_info,
        })

# by topics
def toc_topics(request):
    books = TocBookTopic.objects.using('database').exclude(id = -1).order_by("-topic_distribution")
    topics = TocTopic.objects.using('database').order_by("-book_count")
    return  render(request,'bookDisplayer/toc_topics.html' , {
            'books' : books,
            'topics' : topics,
        })

# by frequency
def toc_freq(request):
    books = BookTopicInfo.objects.using('database').order_by("id")
    books_info = BookInfo.objects.using('database').order_by("id")
    freqs = TocFreq.objects.using('database').order_by("id")
    books_info = BookInfo.objects.using('database').all()
    for TocFreqIdentity in freqs:
        TocFreqIdentity.frequency = ast.literal_eval(TocFreqIdentity.frequency)

    return render(request, 'bookDisplayer/toc_freq.html' , { 
        'books' : books,
        'freqs' : freqs,
        'books_info' : books_info
        })


## Detail pages







def class_detail(request, class_id):
    class_info = ClassInfo.objects.using('database').filter(id = class_id)[0]
    books = BookInfo.objects.using('database').filter(dept_course__contains = class_info.dept_course)
    topics_toc = []
    topics_descript = []

    for book in books:
        toc = TocBookTopic.objects.using('database').filter(isbn = book.isbn)
        descript = DescriptBookTopic.objects.using('database').filter(isbn = book.isbn)
        topics_toc.extend(toc)
        topics_descript.extend(descript)

    return render(request , 'bookDisplayer/class_detail.html', {
        'class' : class_info,
        'books' : books,
        'topics_toc': topics_toc,
        'topics_descript' : topics_descript,
        })


def book_detail(request , book_id):
    book = BookTopicInfo.objects.using('database').filter(id = book_id)[0]
    toc_topics = TocBookTopic.objects.using('database').filter(id = book_id)
    descript_topics = DescriptBookTopic.objects.using('database').filter(id = book_id)

    return render(request , 'bookDisplayer/book_detail.html' , {
        'book' : book,
        'toc_topics' : toc_topics,
        'descript_topics' : descript_topics,
        })

def toc_topic_detail(request , topic_id):
    topics = TocBookTopic.objects.using('database').all().filter(topic_id = topic_id)
    topic_words = topics[0].topic_words
    courses = ClassInfo.objects.using('database').all()
    all_classes = []
    for topic in topics:
        isbn = topic.isbn
        classes = courses.filter(associated_books__contains = isbn)
        for c in classes:
            all_classes.append(c)
    class_count = len(all_classes)
    return render(request , 'bookDisplayer/toc_topic_detail.html', {
        'topics' : topics,
        'topic_words' : topic_words,
        'classes' : all_classes,
        'class_count' : class_count,
        })

def descript_topic_detail(request, topic_id):
    topics = DescriptBookTopic.objects.using('database').all().filter(topic_id = topic_id)
    topic_words = topics[0].topic_words
    courses = ClassInfo.objects.using('database').all()
    all_classes = []
    for topic in topics:
        isbn = topic.isbn
        classes = courses.filter(associated_books__contains = isbn)
        for c in classes:
            all_classes.append(c)
    class_count = len(all_classes)
    return render(request , 'bookDisplayer/descript_topic_detail.html', {
        'topics' : topics,
        'topic_words' : topic_words,
        'classes' : all_classes,
        'class_count' : class_count,
        })

def job_detail(request , job_id):
    job = JobInfo.objects.using('database').all().filter(id = job_id)
    

    return render(request , 'bookDisplayer/job_detail.html' , {
        'job' : job,
        
        })




## Dumb search
def search(request , course):
    courses = ClassInfo.objects.using('database').order_by("id")
    descript_books = DescriptBookTopic.objects.using('database').order_by("-topic_distribution")
    toc_books = TocBookTopic.objects.using('database').order_by('-topic_distribution')  
    return render(request , 'bookDisplayer/search.html',{
        'course' : course,
        'courses' : courses,
        'descript_books' : descript_books,
        'toc_books' : toc_books,

        })
