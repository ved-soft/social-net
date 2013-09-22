.. _backbone:



***********
Backbone.js
***********

Backbone.js
Backbone e javascript библиотека со RESTful JSON интерфејс и е базирана на 
MVP (Model, View, Presenter) дизајн. Backbone e позната како полесна 
библиотека, која е зависна само од javascript и Underscore.js. 
Дизајнирана е за изработка на single-page веб апликации.


Model
-----

Модел во Backbone.js преставува срцето на една Javascript апликација. 
Тој ги содржи податоците со потребната логика за нив, како конверзија, 
валидација, привилегии и слично.

Пример за Backbone модел.::

	Person = Backbone.Model.extend({
        initialize: function(){
            alert("Welcome to this world");
        }
    });
    
    var person = new Person;

Функцијата initialize() се повикува секогаш при креирање на инстанца од тој модел. 
Исто важи и за collection и view. 
Откако ќе креираме инстанца од некој модел за да сетираме параметри на тој модел користиме:
::   

   Person = Backbone.Model.extend({
        initialize: function(){
            alert("Welcome to this world");
        }
    });
    
    var person = new Person({ name: "Thomas", age: 67});
    // or we can set afterwards, these operations are equivelent
    var person = new Person();
    person.set({ name: "Thomas", age: 67});


Значи за сетирање на атрибути на модел користиме model.set(). Сега кога моделот има 
сетирано параметри можеме да ги земеме користејќи model.get().
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	Person = Backbone.Model.extend({
        initialize: function(){
            alert("Welcome to this world");
        }
    });
    
    var person = new Person({ name: "Thomas", age: 67, child: 'Ryan'});
    
    var age = person.get("age"); // 67
    var name = person.get("name"); // "Thomas"
    var child = person.get("child"); // 'Ryan'

На моделите некогаш имаме потреба да имаме default вредности. Начинот на дефинирање 
на default вредности е следен:
::::::::::::::::::::::::::::::

	Person = Backbone.Model.extend({
        defaults: {
            name: 'Fetus',
            age: 0,
            child: ''
        },
        initialize: function(){
            alert("Welcome to this world");
        }
    });
    
    var person = new Person({ name: "Thomas", age: 67, child: 'Ryan'});
    
    var age = person.get("age"); // 67
    var name = person.get("name"); // "Thomas"
    var child = person.get("child"); // 'Ryan'

Моделите исто така можат да содржат методи во нив. По default сите методи во еден 
модел се public.
::::::::::::::::

	Person = Backbone.Model.extend({
        defaults: {
            name: 'Fetus',
            age: 0,
            child: ''
        },
        initialize: function(){
            alert("Welcome to this world");
        },
        adopt: function( newChildsName ){
            this.set({ child: newChildsName });
        }
    });
    
    var person = new Person({ name: "Thomas", age: 67, child: 'Ryan'});
    person.adopt('John Resig');
    var child = person.get("child"); // 'John Resig'

Сите атрибути на моделот може да имаат функции кои чекаат на промени на атрибутот. 
Тие функции се повикуваат секогаш на промена на избраниот параметар. 
Во следниот пример, при промена на name атрибутот на person моделот ќе го алертува новото име.::

   Person = Backbone.Model.extend({
        defaults: {
            name: 'Fetus',
            age: 0
        },
        initialize: function(){
            alert("Welcome to this world");
            this.on("change:name", function(model){
                var name = model.get("name"); // 'Stewie Griffin'
                alert("Changed my name to " + name );
            });
        }
    });
    
    var person = new Person({ name: "Thomas", age: 67});
    person.set({name: 'Stewie Griffin'}); // This triggers a change and will alert()

Доколку сакаме да имаме listener кои ќе слуша на промени на сите атрибути, 
едноставно користиме: this.on("change", function(model){});

Collection
----------

Backbone collections преставуваат низа од модели. 
На пример може да се користи во ситуации како::

	Model: Student, Collection: ClassStudents
	Model: Todo Item, Collection: Todo List
	Model: Animal, Collection: Zoo

Пример за model/collection::

   var Song = Backbone.Model.extend({
     initialize: function(){
     	console.log("Music is the answer");
   	}
   });
   
   var Album = Backbone.Collection.extend({
   	model: Song
   });
   
   var song1 = new Song({ name: "How Bizarre", artist: "OMC" });
   var song2 = new Song({ name: "Sexual Healing", artist: "Marvin Gaye" });
   var song3 = new Song({ name: "Talk It Over In Bed", artist: "OMC" });
   
   var myAlbum = new Album([ song1, song2, song3]);
   console.log( myAlbum.models ); // [song1, song2, song3]


View
----

Кодот за view-то наликува исто како на моделот. Се користи за прикажување на одреден дел на страната. 
За рендерирање на темплејти се користи Underscore.js темплејт. 
За манипулација на DOM се користи jQuery. Пример за едно view:
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	SearchView = Backbone.View.extend({
        initialize: function(){
            alert("Alerts suck.");
        }
    });

    // The initialize function is always called when instantiating a Backbone View.
    // Consider it the constructor of the class.
    var search_view = new SearchView();

Параметарот el референцира до DOM објектот креиран во browser-от. Секој Backbone View 
има еден el параметар, кој ако не е дефиниран, по default backbone ќе креира празен div елемент.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	<div id="search_container"></div>

	<script type="text/javascript">
    	SearchView = Backbone.View.extend({
        	initialize: function(){
            	alert("Alerts suck.");
        	}
    	});
    	
    	var search_view = new SearchView({ el: $("#search_container") });
	</script>

Сите евенти што се повикуваат мора да бидат во овој елемент.
Вчитувањето на темплејти во Backbone е целосно зависно од Underscore.js. Во следниот пример 
ќе имплементираме render() функција која што ќе се повикува на иницијализација на view-то 
и ќе го прикачиме на el параметарот користејќи jQuery.
::::::::::::::::::::::::::::::::::::::::::::::::::::::
	
	<script type="text/template" id="search_template">
  		<label>Search</label>
  		<input type="text" id="search_input" />
  		<input type="button" id="search_button" value="Search" />
	</script>

	<div id="search_container"></div>

	<script type="text/javascript">
    	SearchView = Backbone.View.extend({
        	initialize: function(){
            	this.render();
        	},
	        render: function(){
	            // Compile the template using underscore
	            var template = _.template( $("#search_template").html(), {} );
	            // Load the compiled HTML into the Backbone "el"
	            this.$el.html( template );
        	}
    	});
    
    	var search_view = new SearchView({ el: $("#search_container") });
	</script>

Евенти во Backbone View можат да се прикачат само на el елементот и на сите негови child елементи. 
На следниот пример ќе прикажеме еден click евент на копче::
 
   <script type="text/template" id="search_template">
   	<label>Search</label>
   	<input type="text" id="search_input" />
   	<input type="button" id="search_button" value="Search" />
   </script>
   
   <div id="search_container"></div>
   
   <script type="text/javascript">
       SearchView = Backbone.View.extend({
           initialize: function(){
               this.render();
           },
           render: function(){
               var template = _.template( $("#search_template").html(), {} );
               this.$el.html( template );
           },
           events: {
               "click input[type=button]": "doSearch"
           },
           doSearch: function( event ){
               // Button clicked, you can access the element that was clicked with event.currentTarget
               alert( "Search for " + $("#search_input").val() );
           }
       });
   	
   	    var search_view = new SearchView({ el: $("#search_container") });
   	</script>

Router
------

Backbone router се користи за рутирање на Backbone апликацијата со користење на хаштагови. 
Рутерите интерпретираат се што содржи после хаштагот и повикува функција дефинирана за патека.
::	
	
	<script>
	    var AppRouter = Backbone.Router.extend({
	        routes: {
	            "*actions": "defaultRoute" // matches http://example.com/#anything-here
	        }
	    });
	    // Initiate the router
	    var app_router = new AppRouter;
	
	    app_router.on('route:defaultRoute', function(actions) {
	        alert(actions);
	    })
	
	    // Start Backbone history a necessary step for bookmarkable URL's
	    Backbone.history.start();
	
	</script>
	
	
Целосно отворено API за Backbone js, како и по опширна документација може да најдете на 
следните линкови:
	
	* `<http://backbonejs.org/>`_
	* `<http://backbonetutorials.com/>`_
	* `<https://github.com/jashkenas/backbone>`_
	* `<http://addyosmani.github.io/backbone-fundamentals/>`_
	
	
	
	
	