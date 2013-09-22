.. _marionette:



*************
Marionette.js
*************


Backbone.Marionette е композитна библиотека за Backbone.js што ја олеснува и симплифицира 
конструкцијата на големи javascript апликации. 
Предноста на користењето на Marionette во Backbone апикациите е тоа што овој плагин ни ја олеснува 
работата со views. 

Views
-----

Marionette.View го наследува Backbone.View. Ги имаме следните типови на views во Marionette:

* Marionette.View: Base View type што другите Marionette views го наследуваат (Не се користи директно).
* Marionette.ItemView: View што рендерира само една инстанца.
* Marionette.CollectionView: View коешто итерира врз collection, и рендерира по една ItemView инстанца за секој модел.
* Marionette.CompositeView: Содржи model и collection. Рендерира Collection view и item view.
* Marionette.Layout: View коешто рендерира layout и креира региони и регион менаџер што ги менаџира полињата во него.


Marionette.View
---------------

Marionette има основен Marionette.View тип на View од кој наследуваат сите други Views. 
Овој основен view ги содржи сите заеднички својства и функционалности што ги користат сите други views.
Овој тип не е наменет да се користи директно. Тој постои како основен view за да можат 
другите views да го наследат.

Прикачување на евенти во Marionette.View препорачливо е да се прави со listenTo.::

	MyView = Backbone.Marionette.ItemView.extend({
	  initialize: function(){
	    this.listenTo(this.model, "change:foo", this.modelChanged);
	    this.listenTo(this.collection, "add", this.modelAdded);
	  },
	
	  modelChanged: function(model, value){
	  },
	
	  modelAdded: function(model){
	  }
	});

При затворање на view се повикуваат onBeforeClose, onClose методите, се бришат сите евенти 
сетирани на DOM елементите, се брише this.el од DOM. 
Доколку имплементирате onClose метод во вашата дефиниција на view-то, таа ќе биде повикана 
при затворање на view-to. За разлика од onClose, onBeforeClose методот се повикува веднаш пред 
бришењето на view-то. Доколку оваа функција ни врати false, при повик на close() view-то нема 
да биде затворено.::
	
	Backbone.Marionette.ItemView.extend({
	  onClose: function(){
	    // custom cleanup or closing code, here
	  }
	});
	
	MyView = Marionette.View.extend({
	
	  onBeforeClose: function(){
	    // prevent the view from being closed
	    return false;
	  }
	
	});
	
	var v = new MyView();
	
	v.close(); // view will remain open


Marionette.ItemView
-------------------

ItemView е view кое прикажува еден item. Toj item може да биде Backbone.Model или може да 
биде Backbone.Collection којашто ќе се третира како една ставка. 
Класата ItemView наследува директно од Marionette.View. 
Има render метод во неа кој се користи за рендерирање на темплејти наменети за тоа view.
За оваа акција да биде извршена, треба да му сетираме template атрибут на ItemView-то. Тој 
треба да биде jQuery селектор.::

	MyView = Backbone.Marionette.ItemView.extend({
	  template: "#some-template"
	});

	new MyView().render();


За рендерирање на Backbone.Collection најдобро е да користиме CollectionView или CompositeView, но 
ако ни е потребно да изрендерираме една обична листа каде што не ни е потребна никаква интеракција 
можеме да искористиме и ItemView.
:::::::::::::::::::::::::::::::::

	<script id="some-template" type="text/html">
	  <ul>
	    <% _.each(items, function(item){ %>
	    <li> <%= item.someAttribute %> </li>
	    <% }); %>
	  </ul>
	</script>
	
	var MyItemsView = Marionette.ItemView.extend({
	  template: "#some-template"
	});
	
	var view = new MyItemsView({
	  collection: someCollection
	});

Ова е пример како тоа можеме да прикажеме Backbone.Collection со ItemView.
Евенти што се тригерираат при рендерирање на еден ItemView се "before:render"/onBeforeRender 
и "render" / onRender. onBeforeRender се извршува пред да биде почнато рендерирањето на темплејтот.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	
	Backbone.Marionette.ItemView.extend({
	  onBeforeRender: function(){
	    // set up final bits just before rendering the view's `el`
	  }
	});

A додека onRender се извршува откако темплејтот ќе биде рендериран.::

	Backbone.Marionette.ItemView.extend({
	  onRender: function(){
	    // manipulate the `el` here. it's already
	    // been rendered, and is full of the view's
	    // HTML, ready to go.
	  }
	});

Организација на UI елементите во Marionette View се прави така што можеме да сетираме ui атрибут, 
кадешто со jQuery селектори ќе ги дефинираме сите UI елементи што ни се потребни за користење 
во тој view. Потоа во другите методи на view-то можеме да ги повикаме со this.ui.elementName.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	Backbone.Marionette.ItemView.extend({
	  tagName: "tr",
	
	  ui: {
	    checkbox: "input[type=checkbox]"
	  },
	
	  onRender: function() {
	    if (this.model.get('selected')) {
	      this.ui.checkbox.addClass('checked');
	    }
	  }
	});

Исто така во Marionette View постојат евенти што се поврзани директно со моделите или колекциите, 
како на пример modelEvents, collectionEvents::

	Marionette.ItemView.extend({
	  modelEvents: {
	    "change": "modelChanged"
	  },
	
	  collectionEvents: {
	    "add": "modelAdded"
	  }
	});

Од овој пример може да видиме дека при промена на некој модел, ќе се изврши modelChanged методот, 
додека во вториот случај modelAdded ќе се изврши при секое додавање на model во collection-от на тоа view.


Marionette.CollectionView
-------------------------
CollectionView е таков тип на view, којшто ќе помине низ целата низа од модели во collection 
и ќе ги рендерира сите користејќи специфициран itemView, потоа el елементите од сите itemViews 
ќе ги прикачи на неговиот el елемент. За да сетираме itemView во нашиот collection view треба 
да користиме Backbone view дефиниран објект, а не негова инстанца. Може да биде било кој 
Backbone.View или Marionette.ItemView
:::::::::::::::::::::::::::::::::::::
	
	MyItemView = Backbone.Marionette.ItemView.extend({});
	
	Backbone.Marionette.CollectionView.extend({
	  itemView: MyItemView
	});

Во многу случаеви ќе мора да префрлите некој податок од collection view до секоја инстанца 
од itemView. За да го направите тоа треба да дефинирате itemViewOptions во вашиот CollectionView 
и тоа ќе биде префрлено во вашиот itemView како дел од опциите.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	ItemView = Backbone.Marionette.ItemView({
	  initialize: function(options){
	    console.log(options.foo); // => "bar"
	  }
	});

	CollectionView = Backbone.Marionette.CollectionView({
	  itemView: ItemView,
	
	  itemViewOptions: {
	    foo: "bar"
	  } 
	});

Исто така itemViewOptions може да ја сетирате и како функција, доколку имате потреба да пресметате 
нешто. Функцијата мора да враќа објект кадешто атрибутите од објектот ќе бидат копирани во 
инстанцата на itemView како опции.
::::::::::::::::::::::::::::::::::

	CollectionView = Backbone.Marionette.CollectionView({
	  itemViewOptions: function(model, index) {
	    // do some calculations based on the model
	    return {
	      foo: "bar",
	      itemIndex: index
	    }   
	  }  
	});

Кога колекцијата не содржи ниту еден објект т.е. таа е празна, можете да специфицирате emptyView 
атрибут на вашиот CollectionView.
:::::::::::::::::::::::::::::::::

	NoItemsView = Backbone.Marionette.ItemView.extend({
	  template: "#show-no-items-message-template"
	});
	
	Backbone.Marionette.CollectionView.extend({
	  // ...
	
	  emptyView: NoItemsView
	});

Доколку Collection-от на ова view е празен, тогаш ќе се изрендерира NoItemsView.

Исто како и во ItemView и тука се извршуваат евентите при рендерирање onBeforeRender и onRender, како 
и евентите при close на view, onClose и onBeforeClose. Други евенти што постојат во CollectionView 
се евентите при додавање и бришење на itemView. Имаме onBeforeItemAdded, метод што се извршува секогаш 
пред додавање на ItemView, onAfterItemAdded, метод што се извршува секогаш после додавање на ItemView 
и onItemRemoved, метод што се извршува секогаш кога некој ItemView ќе биде избришан од CollectionView.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	Backbone.Marionette.CollectionView.extend({
	  onBeforeItemAdded: function(itemView){
	    // work with the itemView instance, here
	  },
	 onAfterItemAdded: function(itemView){
	    // work with the itemView instance, here
	  },
	onItemRemoved: function(itemView){
	    // work with the itemView instance, here
	  }
	});

При извршување на евентите "add", "remove" и "reset" на дефинираниот Collection, во CollectionView-то 
ќе се извршат следните акции. За "add" CollectionView-то ќе го изрендерира само новиот додаден модел. 
При "remove" на item од CollectionView-то ќе се затвори само тоа ItemView што е избришано. При "reset" 
на Collection, CollectionView-то ќе се изрендерира повторно, т.е. ќе го повика методот render.
CollectionView-то само по себе ги прилепува itemView-ата на својот el елемент со jQuery функцијата append. 
Но доколку имаме потреба да ги прикачиме на друг елемент, тогаш можеме да ја употребиме функцијата 
appendHtml која прима три параметри collectionView, itemView, index.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	Backbone.Marionette.CollectionView.extend({
	
	    // The default implementation:
	  appendHtml: function(collectionView, itemView, index){
	    collectionView.$el.append(itemView.el);
	  }
	
	});


Marionette.CompositeView
------------------------

CompositeView наследува од CollectionView и го надополнува за да може да се искористи за посебни 
случаеви кога треба да се прикаже некој објект кој самиот во себе има и листа. Најдобар пример 
што можеме да го наведеме за користење на овој тип на view е TreeView.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	
	CompositeView = Backbone.Marionette.CompositeView.extend({
	  template: "#leaf-branch-template"
	});
	
	new CompositeView({
	  model: someModel,
	  collection: someCollection
	});

CompositeView има атрибут itemViewContainer којшто се користи за да сетираме елемент кадешто 
itemView-ата од Collection-от ќе се прикачуваат. Ќе дадеме пример за употреба на еден CompositeView. 
За почеток потребни ни се два темплејти, еден за itemView-ата, а другиот за самиот CompositeView.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	<script id="row-template" type="text/html">
	  <td><%= someData %></td>
	  <td><%= moreData %></td>
	  <td><%= stuff %></td>
	</script>
	
	<script id="table-template" type="text/html">
	  <table>
	    <thead>
	      <tr>
	        <th>Some Column</th>
	        <th>Another Column</th>
	        <th>Still More</th>
	      </tr>
	    </thead>
	
	    <!-- want to insert collection items, here -->
	    <tbody></tbody>
	
	    <tfoot>
	      <tr>
	        <td colspan="3">some footer information</td>
	      </tr>
	    </tfoot>
	  </table>
	</script>

Потоа ги креираме view-ата и сетираме itemViewContainer.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	
	RowView = Backbone.Marionette.ItemView.extend({
	  tagName: "tr",
	  template: "#row-template"
	});
	
	TableView = Backbone.Marionette.CompositeView.extend({
	  itemView: RowView,
	
	  // specify a jQuery selector to put the itemView instances in to
	  itemViewContainer: "tbody",
	
	  template: "#table-template"
	});

Истиот елемент можеме да го сетираме и во функцијата appendHtml.


Marionette.Layout
-----------------

Layout е хибрид од ItemView и колекција од региони. Layout-ите се идеални за рендерирање на 
layout-и за апликации со повеќе региони. Во следниот пример ќе покажеме како се употребува layout 
во една Marionette апликација.
:: 

	<script id="layout-template" type="text/template">
	  <section>
	    <navigation id="menu">...</navigation>
	    <article id="content">...</article>
	  </section>
	</script>
::
	
	AppLayout = Backbone.Marionette.Layout.extend({
	  template: "#layout-template",
	
	  regions: {
	    menu: "#menu",
	    content: "#content"
	  }
	});
	
	var layout = new AppLayout();
	layout.render();

Откако ќе се изрендерира layout-от имаме целосен пристап до неговите региони.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	layout.menu.show(new MenuView());
	
	layout.content.show(new MainContentView());

Регионите можат да бидат додадени и избришани по потреба. Методи за додавање и бришење на 
региони се addRegion, addRegions, removeRegion.

addRegion
:::::::::

	var layout = new MyLayout();
	
	// ...
	
	layout.addRegion("foo", "#foo");
	layout.foo.show(new someView());

addRegions
::::::::::

	var layout = new MyLayout();
	
	// ...
	
	layout.addRegions({
	  foo: "#foo",
	  bar: "#bar"
	});

removeRegions
:::::::::::::

	var layout = new MyLayout();
	
	// ...
	
	layout.removeRegion("foo");
	
	
Application
-----------

Backbone.Marionette.Application објектот е центар на вашата композитна апликација. 
Тој организира, иницијализира и координира различни парчиња во вашата апликација. Исто така 
обезбедува појдовна точка за повикување. Апликацијата е наменета да се инстанцира директно, но 
доколку сакате можете да и додадете екстра функционалност.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	MyApp = new Backbone.Marionette.Application();

Вашата апликација треба според дефинираните рутери да ја прикажува содржината од поставените региони, да 
ја менува содржината на регионите и друго. За да ја завршиме цела таа работа нас ни е потребно да го 
сетираме addInitializer на апликацијата.
::::::::::::::::::::::::::::::::::::::::

	MyApp.addInitializer(function(options){
	  // do useful stuff here
	  var myView = new MyView({
	    model: options.someModel
	  });
	  MyApp.mainRegion.show(myView);
	});
	
	MyApp.addInitializer(function(options){
	  new MyAppRouter();
	  Backbone.history.start();
	});

Овие методи ќе се извршат кога ќе ја стартуваме апликацијата. 
Во својот животен циклус апликацијата повикува неколку евенти: "initialize:before" / onInitializeBefore кој 
се извршува пред да се иницијализира апликацијата, "initialize:after" / onInitializeAfter кој се извршува 
веднаш после иницијализација на апликацијата и "start" / onStart којшто се извршува после 
initialize и неговите евенти.
:::::::::::::::::::::::::::::
	
	MyApp.on("initialize:before", function(options){
	  options.moreData = "Yo dawg, I heard you like options so I put some options in your options!"
	});
	
	MyApp.on("initialize:after", function(options){
	  if (Backbone.history){
	    Backbone.history.start();
	  }
	});

Откако се во апликацијата е конфигурирано, апликацијата почнува со работа со повикување на 
MyApp.start(options). Оваа функција прима еден параметар со опции.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	var options = {
	  something: "some value",
	  another: "#some-selector"
	};
	
	MyApp.start(options);

Секоја апликација доаѓа со инстанца од Backbone.Wreqr.EventAggregator што се нарекува app.vent.
Таму можеме да ги додадеме сите глобални евенти којшто ќе ни бидат потребни низ целата апликација.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	MyApp = new Backbone.Marionette.Application();
	
	MyApp.vent.on("foo", function(){
	  alert("bar");
	});
	
	MyApp.vent.trigger("foo"); // => alert box "bar"


Router
------

Дефинирањето на рутите во Marionette е исто како и во Backbone. На секоја дефиниција за рута 
сетираме метод во рутерот. 
Пример:
:::::::
	
	MyRouter = Backbone.Marionette.AppRouter.extend({
	  // "someMethod" must exist at controller.someMethod
	  appRoutes: {
	    "some/route": "someMethod"
	  },
	
	  /* standard routes can be mixed with appRoutes/Controllers above */
	  routes : {
	    "some/otherRoute" : "someOtherMethod"
	  },
	  someOtherMethod : function(){
	    // do something here.
	  }
	
	});

Рутерите може да се користат само во controller објект. Тие може да се дефинираат во 
рутер-от или на контролерот може да сетираме рутер.
:::::::::::::::::::::::::::::::::::::::::::::::::::

	someController = {
	  someMethod: function(){ /*...*/ }
	};
	
	Backbone.Marionette.AppRouter.extend({
	  controller: someController
	});

::
	
	myObj = {
	  someMethod: function(){ /*...*/ }
	};
	
	new MyRouter({
	  controller: myObj
	});


Controller
----------
	
Овој објект се користи како контролер за модулите и рутерите, и како посредник за работа и координација 
на другите објекти, view-ата и многу повеќе. Marionette.Controller може да биде проширен (extended) 
како и сите други Backbone и Marionette објекти. Го поддржува стандардниот initialize метод. 
Еве еден пример како се користи Controller.
:::::::::::::::::::::::::::::::::::::::::::

	// define a controller
	var MyController = Marionette.Controller.extend({
	
	  initialize: function(options){
	    this.stuff = options.stuff;
	  },
	
	  doStuff: function(){
	    this.trigger("stuff:done", this.stuff);
	  }
	
	});
	
	// create an instance
	var c = new MyController({
	  stuff: "some stuff"
	});
	
	// use the built in EventBinder
	c.listenTo(c, "stuff:done", function(stuff){
	  console.log(stuff);
	});
	
	// do some stuff
	c.doStuff();

Исто како и сите view-а во Marionette и контролерот има метод close којшто се грижи да ги избрише 
сите евенти кои се директно закачени на инстанцата на контролерот.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

	// define a controller with an onClose method
	var MyController = Marionette.Controller.extend({
	
	  onClose: function(){
	    // put custom code here, to close this controller
	  }
	
	})
	
	// create a new controller instance
	var contr = new MyController();
	
	// add some event handlers
	contr.on("close", function(){ ... });
	contr.listenTo(something, "bar", function(){...});
	
	// close the controller: unbind all of the
	// event handlers, trigger the "close" event and 
	// call the onClose method
	controller.close();
	
Ова е само мал дел од тоа што го нуди овој плагин на Backbone, за да може да го совладате целиот матерјал 
следуваат неколку линкови кадешто подетално е објаснето за Marionette.
   
   * `<http://marionettejs.com/>`_
   * `<http://addyosmani.github.io/backbone-fundamentals/#marionettejs-backbone.marionette>`_
   * `<https://github.com/marionettejs/backbone.marionette>`_

Пред да се зафатите со работа, исто така убаво е да ја прочитате и следната книга којашто објаснува 
како да ги решавате проблемите во огромните javascript апликации.

   * `<http://addyosmani.com/resources/essentialjsdesignpatterns/book/>`_
