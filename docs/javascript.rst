.. _javascript:


******
Javascript
******

Javascript е скриптен јазик којшто може да биде вметнат во HTML страна. 
Овој програмски јазик се користи за регирање на 
евенти (пример: клик на копче, клик на слика, вчитување на страна ... ), 
за промена на содржината во HTML, за промена на CSS стилови, 
валидација на input полиња и се извршува во сите модерни Browser- и.


Променливи
----------
Променливите се користат за чување на вредност која можеме да ја употребиме 
подоцна во кодот. Променливите може да чуваат секаков тип на вредност: текст, 
бројки, листа, објект, дури и код (во форма на функција). 
Променливите се декларираат со ``var``.
::
   
	var myName = “Oliver”;
	var a = 1, b = “primer”;

Кога употребуваме некоја вредност повеќепати, тогаш потребно е да се искористи променлива.

Во javascript постојат 5 примитивни типови на променливи: ``string(text)``, ``boolean(true/false)``, 
``numbers``, ``undefined``, ``null``. Другото се се третира како објект.


Функции
----------------------
Функциите овозможуваат помали програмски блокови да бидат поделени во една целина.
::
 
   	var zbir = function(a, b) { 
		return a+b;
	}
	
Или:: 
	
	function zbir(a, b) {
		return a+b;
	}

 
Објекти
--------------------

Како и во повеќето други програмски јазици, исто и во javascript се користат 
објекти.
::

	var person = {
		first_name: “John”,
		last_name: “Doe”
	};

Објектот на примерот се состои од две променливи ``first_name`` и ``last_name``. 
До нив се пристапува со точка, t.e. ``person.first_name`` или ``person.last_name``.


Object methods
--------------

Методи во објектите се параметри во објектот кои нивните вредности се функции.::
   
	var person = {
		first_name: “John”,
		last_name: “Doe”,
		get_person: functin() {
			alert(this.first_name, this.last_name);
		}
	};
   
За да пристапиме до методот get_person само додаваме на објектот ``person.get_person()``;
Значењето на зборот this. Во секој метод, во секоја функција постои овој збор – ``this``; 
Се однесува на објектот во кој функцијата е повикана. Тоа значи дека кога го 
повикуваме ``person.get_person()``, можеме да го користиме зборот this во функцијата ``get_person()``, 
за да пристапиме до објектот person, директно од методот ``get_person()``.


 
Arrays
------
Низите се тип на објекти кој се чуваат во листи од вредности. 
Добро е да се чуваат како сет од слични вредности со ист тип, на пример strings. 
 
Пример за array:
::
   
	var myArray = [ 'a', 'b', 'c' ];
 
Пристап до некој член во низата: ``myArray[0]``.


Loops (for циклус)
------------------

Како и во секој програмски јазик и во јаваскрипт постои ја има употребата на for циклус.
Со употреба на for циклус можеме да направиме итерација врз една низа. 
Пример: 
::
  
	var myArray = [ 'a', 'b', 'c' ];
	var i;
	var len = myArray.length;
	 
	for (i = 0; i < len; i = i + 1) {
		console.log( 'item at index ' + i + ' is ' + myArray[ i ] );
	}
  
Променливата ``i`` ја користиме како индекс, стартува од ``0`` и се инкрементира за еден 
се додека не ја достигне должината на низата.


if/else
-------

Исто така како и во повеќето програмски јазици, така и во javascript постои if/else. 
Се користи да се провери вистинитоста. Во javascript повеќето објекти се вистинити, 
т.е. True. Единствено следните 5 се false: undefined, null, NaN, 0, “”. 
Кога сакаме да тестираме дали некоја вредност е false, тогаш користиме ! Оператор.

Примери
::
   
	var a = '';
	 
	if ( !a ) {
	  // Овој код ќе се изврши ако 'a' е false;
	  console.log( 'a was falsy' );
	}
	
	var notANumber = 'four' - 'five';
	 
	if ( !notANumber ) {
	  // this code will run
	  console.log( '!notANumber was truthy' );
	}


Логички оператори
-----------------

Логички оператори кои се користат во javascript се: И(&&) и ИЛИ(||) операторите.
Примери
::
   
	var foo = 1;
	var bar = 0;
	var baz = 2;
	 
	foo || bar;     // returns 1, which is truthy
	bar || foo;     // returns 1, which is truthy
	 
	foo && bar;     // returns 0, which is falsy
	foo && baz;     // returns 2, which is truthy

   
Резервирани зборови
-------------------

Следната листа од зборови преставува листа од резервирани зборови во javascript::

	abstract boolean break byte case catch char class const continue debugger
	default delete do double else enum export extends false final finally float
	for function goto if implements import in instanceof int interface long
	native new null package private protected public return short static super
	switch synchronized this throw throws transient true try typeof var
	volatile void while with
	

јQuery
------

jQuery е javascript библиотека којашто се користи за лесно да се манипулира со 
HTML страна откако ќе биде прикажана од browser-от. Исто така овозможува многу 
алатки кои помагаат на корисникот во интеракција со страната, како и алатки кои 
креираат анимации на страната и алатки кои ви дозволуваат директна комуникација 
со серверот без превчитување на страната.

Што преставува знакот ``$``?
jQuery библиотеката преставува функција којашто ни дозволува да селектираме 
HTML елементи со помош на CSS селектори.
::

	var listItems = jQuery( 'li' ); 

или::
	
	var listItems = $( 'li' );

``$`` преставува кратенка за ``jQuery``.

За да бидеме сигурни дека е безбедно да користиме ``jQuery`` на нашата HTML страна, 
треба да се осигураме дека страната (DOM three) е целосно вчитана и е спремна за 
манипулација од страна на ``jQuery`` кодот. Тоа можеме да го исполниме со тоа што 
целиот код ќе го сместиме во ``$(document).ready();``.
::

	$( document ).ready(function() {
	  console.log( 'ready!' );
	});


jQuery селектори
-----------------

Ако имате претходно познавање на CSS тогаш употребата на селектори во jQuery ќе ви биде 
многу едноставна. Имено CSS селекторите се сместуваат во $();

Пример::

	$( '#header' ); // select the element with an ID of 'header'
	$( 'li' );      // select all list items on the page
	$( 'ul li' );   // select list items that are in unordered lists
	$( '.person' ); // select all elements with a class of 'person'

Други начини за да се креираат jQuery објекти. ::

	// create a jQuery object from a DOM element
	$( document.body.children[0] );
	 
	// create a jQuery object from a list of DOM elements
	$( [ window, document ] );
	 
	// make a selection in the context of a DOM element
	var firstBodyChild = document.body.children[0];
	$( 'li', firstBodyChild );
	 
	// make a selection within a previous selection
	var paragraph = $( 'p' );
	$( 'a', paragraph );

За да провериме дали нашата селекција е успешна, т.е. дали селекторот пронашол таг 
во HTML-от на страната можеме да искористиме
::

	if ( $( '#nonexistent' ) ) {
	  // Wrong! This code will always run!
	}
	 
	if ( $( '#nonexistent' ).length > 0 ) {
	  // Correct! This code will only run if there's an element in your page
	  // with an ID of 'nonexistent'
	}
	
	if ( $( '#nonexistent' ).length ) {
	  // This code will only run if there's a matching element
	}


Креирање на нови тагови (HTML елементи) со помош на jQuery:
-----------------------------------------------------------
Ако му додадете HTML на ``$()`` можете да креиратe елемент во меморијата. 
Тој елемент ќе биде креиран но нема да биде прикажан на страната се додека 
вие прилепите на некој постоечки елемент. 
::

	$( '<p>' ); // creates a new <p> element with no content
	$( '<p>Hello!</p>' ); // creates a new <p> element with content
	$( '<p class="greet">Hello!</p>' ); // creates a new <p> with content and class

Исто така можете да креирате елемент со прикачување на информации за тоа како сакате 
да го креирате елементот. 
::

	$( '<p>', {
	  html: 'Hello!',
	  'class': 'greet'
	});	

Во овој туторијал на кратко спомнавме за javascript и за нејзината најупотребувана 
библиотека jQuery. За подетално да се запознаете со овој програмски јазик, неговите техники 
на работење како и користењето на библиотеката jQuery и нејзиниот плагин за кориснички интерфејс
може да ги погледнете на следните линкови:

	* `<http://www.w3schools.com/js/>`_
	* `<http://www.w3schools.com/jquery/>`_
	* `<http://jquery.com/>`_
	* `<http://jqueryui.com/>`_
	* `<http://jqfundamentals.com/chapter/jquery-basics>`_
	