.. _tastypie:

********
Tastypie
********
Tastypie претставува webservice framework за Django. Истата овозможува креирање 
на `REST-style интерфејс <http://en.wikipedia.org/wiki/Representational_state_transfer>`_. 
Целата комуникација помеѓу клиентската и серверската апликација е токму преку tastypie.
Како што спомнав претходно tastypie овозможува REST-style архитектура, 
а REST-style архитектурата користи ресурси што значи и tastypie се заснова на 
креирање на ресурси кои што се всушност python класи со субкласа 
``tastypie.resources.Resource``.
Убава практика е кодот за овие ресурси да се чува во претходно креиран пакет 
со име api. 
Исто така за секоја апликација потребно е да се регистрира соодветно ``api`` и 
неговите ``urls`` да се додадат во ``django urls``.
При тоа секој нов ресурс потребно е да се регистрира во претходно креираното ``api``.

Најчесто за секој креиран модел потребно е да се креира соодветен ресурс, 
конкретно за секој модел што има потреба за интеракција со клиентската страна 
потребно е да се креира соодветен негов ресурс. Така за Person моделот што го 
креиравме на почеток ресурсот би изгледал вака::

   class RelationPersonResource(Resource):
       class Meta:
           queryset = Person.objects.filter()
           resource_name = 'relation_person'
           fields = ['id', 'first_name', 'last_name']
           authentication = SessionAuthentication() 
           authorization = Authorization()

Всушност секој ресурс е python класа која што како субкласа ја содржи 
``tastypie.resources.Resource`` или класа која што во себе ја содржи оваа.

Во Meta класата се дефинираат основните параметри на ресурсот од кој модел 
да ги зема податоците(за кој модел се однесува), со кое име клиентот 
да пристапи до истата, кои полиња може да ги гледа клиентот аутентикација итн. 
Сите овие полиња детално се објаснети во самата 
`документација <http://django-tastypie.readthedocs.org/en/latest/tutorial.html>`_ 
на Tastypie и која што мора да ја разгледате за да  може да продолжите во 
следната фаза од проектов.


Креирање на Ресурси во SocialNet
--------------------------------

Во SocialNet апликацијата потребно е да се креира за секој модел соодветен 
ресурс со кој што истиот ќе биде претставен на клиентот. 
Така за моделот Person иницијалниот ресурс изгледа вака::

   class PersonResource(BaseModelResource):

       class Meta:
           queryset = Person.objects.all()
           resource_name = 'persons'
           excludes = ('password', 'is_staff', 'is_superuser',
                       'last_login', 'date_joined')
           always_return_data = True
           list_allowed_methods = ('get', 'post')
           detail_allowed_methods = ('get', 'post', 'patch', 'delete')
           authentication = SessionAuthentication()
           authorization = Authorization()
   
           filtering = {
                        'username': ('exact', ),
                        }
                        
Овој ресурс како и сите останати во проектов наследува од ``BaseModelResource`` 
која што во себе содржи дополнување на одредени методи од tastypie за да може 
динамички да ги повикуваме методите кои што ги имаме имплементирано претхоно 
во моделите. Нема детално да се задржуваме сега на оваа класа едноставно ќе 
ја употребуваме како таква.

Податоците за Person ресурсот се земаат од соодветниот Person модел, до истиот 
можеме да пристапиме преку неговото име ``persons``, полиња кои што не сакаме да се 
прикажуваат на клиентска страна се: ``password, is_staf, is_superuser, last_login, date_joined.`` 
Методи кои што се дозволени во овој ресурс се: ``post, get`` како list methods  
и ``get, post, patch, delete`` како detail methods. 
Дефинирани се соодветна аутентикација и ауторизација за ресурсот и дозволено е 
филтрирање според username.

За повикување на секој од модел методите потребно е секој од нив да биде 
дефиниран во ``Meta`` класата на ресурсот, заедно со неговата валидациона форма 
и параметрите кои што истиот ги прима. За повикување на методите за едитирање 
на корисник потребно е да се направи следнава дефиниција::

        inline_forms = {'UPDATE_PERSON': UpdatePersonForm,
                        'RESET_PASSWD': ResetPasswordForm,
                        }
        update_methods = {'UPDATE_PERSON': 'update_person',
                          'RESET_PASSWD': 'reset_password',
                          }
        update_fields = {'UPDATE_PERSON': ('first_name', 'last_name',
                                           'username', 'email', 'description',
                                           'phone', 'birthday', 'gender'),
                         'RESET_PASSWD': ('old_password', 'new_password'),
                         }

За секој метод потребно е да имаме соодветен клуч за едитирање така за промена 
на лозинка соодветниот клуч е ``RESET_PASSWD``, во делот ``inline_forms`` ја 
дефинираме формата која што одговара на соодветниот клуч во нашиот случај тоа 
е формата за промена на лозинка, во вториот дел го дефинираме името на методот 
што одговара на овој  клуч во нашиот случај ``reset_password`` и во последниот 
``dict`` ги дефинираме полињата кои што ги прима како влезни аргументи методот 
``old_password, new_password``.
Со ова ние всушност ја дефиниравме комуникацијата помеѓу клиентот и соодветниот 
модел на серверската страна за промена на лозинка. На ист начин се дефинираат 
сите останати методи за едитирање.
Методите за бришење се дефинираат на сосема ист начин со тоа што имињата на овие 
параметри се: ``delete_forms, delete_methods, delete_fields``. Пример за оваа 
дефиницја следи во продолжение::

        delete_form = {'REMOVE_PERSON': BaseDeleteForm}
        delete_method = {'REMOVE_PERSON': 'remove_person'}
        delete_fields = {'REMOVE_PERSON': ()}
        
Во конкретнио случај методот за креирање на нов корисник е специфичен 
бидејќи мора да се дозволи POSТ до ресурсот од страна на коирсник кој што 
сеуште не е логиран во системот. Поради тоа овој метод потребно е да има 
специјална имплементација. ::

   def prepend_urls(self):
           return [
               url(r"^(?P<persons>%s)/create_account%s$" \
                           % (self._meta.resource_name, trailing_slash()),
                           self.wrap_view('create_account'),
                           name="social_net_api"),
           ]

   def create_account(self, request, **kwargs):
           self.method_check(request, allowed=['post'])
           self.throttle_check(request)
   
           body = request.raw_post_data
           deserialized = self.deserialize(request, body,
                   format=request.META.get('CONTENT_TYPE', 'application/json'))
           deserialized = \
                       self.alter_deserialized_detail_data(request, deserialized)
   
           form = CreateNewPersonForm(deserialized)
   
           if not form.is_valid():
               raise ValidationError(form.errors)
   
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           email = form.cleaned_data['email']
           description = form.cleaned_data['description']
           phone = form.cleaned_data['phone']
           birthday = form.cleaned_data['birthday']
           gender = form.cleaned_data['gender']
   
           person = Person.create_person(first_name, last_name, username,
                                         password, email, gender, description,
                                         phone, birthday)
   
            return self.create_response(request, dict(id=person.pk),
                                       response_class=HttpCreated)

И во овој метод се прави валидација на податоците преку претходно креираната форма, 
повикување на модел методот за креирање нов корисник и враќање ``response`` кон 
клиентот со потребните информации за новокреираниот корисник.

Во сите останати ресурси дефинирањето за креирање на нов објект од конкретен 
модел е на ист начин, преку дефинирање на параметри во Meta класата за истиот, 
во продолжение следува пример за креирање на нова релација помеќу два контакти ::
   
        validation = \
                    CleanedDataFormValidation(form_class=CreateNewRelationForm)
        create_method = 'add_relation'
        create_fields = ('second_contact_id', 'relation')
        

Формата за валидација ја дефинираме преку tastypie  класата ``CleanedDataFormValidation``, 
и ги дефинираме соодветниот метод за креирање на објект и параметри кои што ги 
прима истиот.
Во најголем број на случаеви еден модел може да има само еден метод за креирање 
на нов објек од истиот, поради тоа во овој случај нема потреба за дефинирање на 
клуч за креирање на објектот.

Доколку клиентот има потреба од некој дополнителни информации за објектот кои што 
не се содржани во самиот модел за истиот, истите можат да се дефинираат во 
dehydrate методот. За ова може повеќе да најдете 
`тука <http://django-tastypie.readthedocs.org/en/v0.10.0/resources.html#dehydrate>`_

Следува соодветен пример од Person ресурсот на SocialNet апликацијата::
   
   def dehydrate(self, bundle):
        # Remove password field from the data that will be send to client.
        bundle.data.pop('password', None)

        rel_counts = bundle.obj.relations_count()

        # If full view is requested must be returned
        # all friends, requested_friends and friend_requests for the contact
        if bundle.request.META['REQUEST_METHOD'] == 'GET' and \
                    bundle.request.GET.get('view_type', None) == 'OWN_VIEW':

            bundle.data['requested_friends_num'] = \
                                            rel_counts['requested_friends_num']
            bundle.data['friend_requests_num'] = \
                                            rel_counts['friend_requests_num']

        bundle.data['friends_num'] = rel_counts['friends_num']
        bundle.data['messages_num'] = bundle.obj.activities.count()
        bundle.data['comments_num'] = bundle.obj.comments.count()

        return bundle
 
Врз основа на досега образложеното потребно е да бидат креирани ресурси за секој 
од останатите модели со соодветните дефиниции за нив.

Креирање на Unit tests со Tastypie
----------------------------------
Многу е важно да имаме интегрирани тестови за целата апликација вклучувајќи го 
и делот за интеракција помеѓу  клиентот и серверот. Tastypie има интегрирано 
свои класи надоградени на веќе постоечките од Django за полесно пишување на 
тестовите при употреба на овој сервис. 
Во tastypie `документацијата <http://django-tastypie.readthedocs.org/en/latest/testing.html>`_ 
има детално објаснување за овие класи.


Во претходниот пример даден за django unit tests можеме да забележиме дека 
всушност тест класата не наследува од ``TestCase`` туку од ``ResourceTestCase`` 
што претставува интегрирана класа од tastypie. 

Постојат неколку видови на requiest-и што може да направи клиентот до 
серверот и тоа: ``get, post, patch, put и delete``. 
Во продолжение за секој од нив ќе дадеме соодветен пример на тест.

При креирање на одреден ресурс, потребно е да видиме дали комуникацијата помеѓу 
овој ресурс и клиентот е воспоставена и ги враќа посакуваните објекти. 
Задачата на наредниот тест е токму таа ::

   def test_get_persons_from_resource(self):
        url = '/social_net/api/1/persons/?format=json'

        response = self.api_c.get(url, format='json',
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertHttpOK(response)

Во ``setUp`` методот дефинирамe инстанца од api_c клиентот кои што ги содржи методите 
за сите овие видови на requests до сервер-от.
За да направиме ``GET`` request до серверот потребно е да имаме дефинирано url 
на кое сакаме да пристапиме, односно url со кое пристапуваме до ресурсот, 
после тоа формат на податоците во нашиов случај ``json``, и како плус параметар 
специфицираме HTTP header  ``HTTP_X_REQUESTED_WITH`` кој што овозможува тестирање 
на ``django.http.HttpRequest.is_ajax()`` методи. Што значи конкретно во нашиот случај 
можеме и да го изоставиме. Во следниот момент проверуваме дали ресурсот од овој 
request е со статус 200 што значи дека истиот е успешен. Со ``response.content`` 
ја земеме датата која што ја враќа овој response.

Доколку сакаме да креираме нов корисник во системот потребно е да направиме 
``POST`` request до соодветниот ресурс на серверот. Тестот за креирање на нов 
корисник изгледа вака::

   def test_create_new_person(self):
        '''
            Create new person in the system  with full data.
        '''
        first_name = 'Test'
        last_name = 'Person'
        username = 'test.person'
        password = '12345'
        email = 'test@mail.com'
        description = 'Test description'
        phone = '+2165125498425'
        birthday = '1989-12-01'
        gender = 'MALE'

        url = '/social_net/api/1/persons/create_account/'
        response = self.api_c.post(url, format='json',
                                   data={'first_name': first_name,
                                        'last_name': last_name,
                                        'username': username,
                                        'password': password,
                                        'email': email,
                                        'description': description,
                                        'phone': phone,
                                        'birthday': birthday,
                                        'gender': gender
                                         },
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertHttpCreated(response)

        resp_data = self.deserialize(response)

        self.assertEqual(resp_data, {u'id': 2})

        person = Person.objects.get(pk=resp_data['id'])

        # Check db values
        self.assertEqual(person.first_name, first_name)
        self.assertEqual(person.last_name, last_name)
        self.assertEqual(person.username, username)
        self.assertEqual(person.email, email)
        self.assertEqual(person.birthday.strftime('%Y-%m-%d'), birthday)
        self.assertEqual(person.description, description)
        self.assertEqual(person.phone, phone)
        self.assertEqual(person.gender, MALE)

        self.assertTrue(person.check_password(password))

Во првиот дел од тестот ги дефинираме сите потребни параметри за креирање на нов 
корисник како посебни променливи, потоа url на кое што треба да биде испратен 
овој request, за симулирање на ``POST`` request го повикуваме методот ``post`` 
од ``api_client`` кој како параметри прима url, форматот на податоците, 
потоа потребните податоци за креирање на нов корисник и 
додатен header доколку е потребен.

Секој ``POST`` request во tastypie  доколку е успешен враќа resopnse со статус 
201, што значи дека нов објект е креиран во нашиов случај тоа е нов корисник. 
На крај потребно е да ги провериме податоците што ги враќа овој response дали 
се оние кои што ги очекуваме и се разбира проверка на сите параметри дали се 
зачувани во база со вистинската вредност.
Доколку постојат специфични услови за креирање на нов корисник сите тие мора да 
бидат истестирани со посебни тестови за да бидеме сигурни дека напишаниот код 
се однесува онака како што очекуваме.

Промена на одредени податоци во веќе креиран објект може да се направи со 
``PUT/PATCH`` request до сервер. ``PUT`` се користи најчесто за едитирање на цел 
објект додека ``PATCH``  се однесува за поединечно едитирање на одредени полиња 
во ресурсот. Пример за едитирање на одреден податок, во нашиов случај лозинка на 
корисник е даден во следниов пример::

   def test_reset_password(self):
        '''
            Reset person's password.
        '''
        person = Person.create_person(**self.person_data)

        old_password = '12345'
        new_password = 'qwerty'

        url = '/social_net/api/1/persons/{0}/'.format(person.pk)
        response = self.api_c.patch(url, format='json',
                                   data={'update_key': 'RESET_PASSWD',
                                         'old_password': old_password,
                                         'new_password': new_password,
                                         },
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertHttpAccepted(response)

        self.assertEqual(self.deserialize(response), [])

        person = Person.objects.get(pk=person.pk)

        self.assertTrue(person.check_password(new_password)) 
        
Во овој случај за да правиме промена на податоците, мора веќе да имаме постоечки објект, 
Доколку го немаме најпрвин е потребно истиот да го креираме. 
Понатаму следува дефинирање на потребните параметир што ги очекува серверот во 
нашиот случај старата и нова лозина и на крај url  на кое да биде испрате истиот. 
Методот за симулирање на овој request  е ``patch`` и истиот ги прима истите параметри 
како и ``POST`` request-от. На крај како одговор од овој request треба да очекуваме 
response со статус 202 или 204 во зависнот дали враќа параметри со него или не. 
Ја проверуваме содржината на response-от и на крај потврдуваме дека променетите податоци 
се запишани во база.

На крај ни останува уште ``DELETE`` request-от кој што се користи доколку сакаме 
да избришеме одреден објект. Пример за тест кои што симулира ``DELETE`` request 
кон сервер е даден во продолжение::

   def test_remove_person(self):
        '''
            Set is_active flag to False.
        '''
        person = Person.create_person(**self.person_data)

        self.assertEqual(Person.objects.filter(is_active=True).count(), 2)

        url = '/social_net/api/1/persons/{0}/?delete_key=REMOVE_PERSON'.\
                                                            format(person.pk)
        response = self.api_c.delete(url, format='json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertHttpAccepted(response)

        self.assertEqual(response.content, '')

        self.assertEqual(Person.objects.filter(is_active=True).count(), 1)

Во конкретниот случај корисникот не го бришеме трајно од база но истиот го деактивираме. 
За симулирање на овој request се повикува ``delete`` методот од api_client со 
соодветни параметри.
Response-от на овој request враќа статус код 204 за успешен request.
Сите претходни тестови очекувавме да бидат успешни, во продолжение еве пример и од 
тест кои што очекуваме да јави грешка. ::

   def test_reset_password_not_match_old(self):
        '''
            Try to reset password but does not match old one and
            server should raise an exceptioon.
        '''
        person = Person.create_person(**self.person_data)

        old_password = '123456'
        new_password = 'qwerty'

        url = '/social_net/api/1/persons/{0}/'.format(person.pk)
        response = self.api_c.patch(url, format='json',
                                   data={'update_key': 'RESET_PASSWD',
                                         'old_password': old_password,
                                         'new_password': new_password,
                                         },
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertHttpApplicationError(response)

        self.assertEqual(response.content,
                                '{"msg": "Old password does not match."}')

        person = Person.objects.get(pk=person.pk)

        self.assertTrue(person.check_password('12345'))

Во овој случај очекуваме response – от да јави грешка со статус 500, 
пораката која што ја содрши овој response може да ја добиеме преку 
``response.content`` и таа ја опишува причината за настанатата грешка. 
На крај правиме проверка на податоците во база дека не се променети.

Врз основа на овие примери и на претходно изнесеното за ``unit tests`` потребно 
е да се направи позитивни и негативни тестови за секој дел од 
``SocialNet`` пликацијата со тоа што ја задржуваме праксата на креирање 
првин тестови па после тоа имплементирање на методи.
