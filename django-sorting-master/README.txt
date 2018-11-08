How to use django-sorting
----------------------------

``django-sorting`` allows for easy sorting, and sorting links generation 
without modifying your views.

There are really 4 steps to setting it up with your projects.

1. List this application in the ``INSTALLED_APPS`` portion of your settings
   file.  Your settings file might look something like::
   
       INSTALLED_APPS = (
           # ...
           'django_sorting',
       )

2. If it's not already added in your setup, add the request context processor.
   Note that context processors are set by default implicitly, so to set them
   explicitly, you need to copy and paste this code into your under
   the value TEMPLATE_CONTEXT_PROCESSORS::
   
        ("django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request")

3. Add this line at the top of your template to load the sorting tags:

       {% load sorting_tags %}


4. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it.

       {% autosort object_list %}
       or (which is more secure) {% autosort object_list accepted_fields %}
       or {% autosort object_list accepted_fields default_ordering %}

    for example

       {% autosort books 'created_at,author__last_name,author__first_name' 'author__last_name,author__first_name' %}

. Now, you want to display different headers with links to sort 
your objects_list:
   
    <tr>
       <th>{% anchor 'last_name,first_name' 'Name' 'authors-list' %}</th>
       <th>{% anchor 'creation_date' 'Creation' %}</th>
        ...
    </tr>

    The first argument is a field of the objects list, and the second 
    one(optional) is a title that would be displayed. The previous 
    snippet will be rendered like this:

    <tr>
        <th><a href="/path/to/your/view/?sort=last_name,first_name#authors-list" title="Name">Name</a></th>
        <th><a href="/path/to/your/view/?sort=creation_date" title="Name">Creation</a></th>
        ...
    </tr>


That's it!


