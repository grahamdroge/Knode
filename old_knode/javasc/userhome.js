
$('document').ready(function(){

	$('.topic-choice').each(function() {
		if($(this).children().is(':checked')) {
			$(this).addClass('topic-choice-click');


		} else {
			$(this).addClass('topic-choice');

		}

	});


		$('.topic-choice').click(function(){
			$(this).toggleClass('topic-choice-click');	
	});
		
		$('.topic-choice').click(function() {
				var checkbox = $(this).children();
				$(this).children().prop('checked',!checkbox.prop('checked'));
		});


	$('.link').click(function(){
		$(this).siblings('.link_num').toggle();
		$(this).siblings('.link_verbose').toggleClass('link_verbose_show');
	});


	// $('.topic-node').each(function(){
	// 	$(this).css('box-shadow', '0px 0px 18px #000');

	// 	// $(this).hide().fadeIn(1750);
	// });

	// $('.topic-node').hover(function(){
	// 	$(this).css('box-shadow', '0px 0px 18px #000');
	// }, function() {
	// 	$(this).css('box-shadow', '');
	// });

	$('#youtube-url').click(function(){
		$('#post_video_form_field').toggle();
		$('#post-form-title').toggle();
	});

	$('#image-file').click(function(){
		$('#id_post_image').click();
	});
	
	$('.navbar-brand').click(function(){
		$('.main-feed').animate({scrollTop: '0'},300);
	});

	$('.dropdown-submenu a.test').on("click",function(e){
	    $(this).next('ul').toggle();
	    e.stopPropagation();
	    e.preventDefault();
	  });
	

	$('.comment_btn').click(function(){
		$(this).parent().next('.comments').toggle();
		$(this).parent().next('.comments').children('div').animate({scrollTop: 500},100);
		
	});

	$('.choice').click(function(){
		var choice = $(this).text();
		var el = $(this);
		if((choice == 'Recommended') | (choice == 'Near Me')) {
			$('.post-gear').fadeOut(200);
			$('.type').animate({width: '44%'},1000);
			el.parent().parent().siblings('a').text(choice);
		} else {
			
			$('.type').animate({width: '26%'},800,function(){
				$('.post-gear').fadeIn(600);
			});
			
			$(this).parent().parent().siblings('a').text(choice);

		}

		$(this).parent().parent().parent().css('background-color','rgb(132,6,2)');
	});

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	$(function() {

	    // This function gets cookie with a given name
	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }
	    var csrftoken = getCookie('csrftoken');

	    /*
	    The functions below will create a header with csrftoken
	    */

	    function csrfSafeMethod(method) {
	        // these HTTP methods do not require CSRF protection
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }
	    function sameOrigin(url) {
	        // test that a given url is a same-origin URL
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }

	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	                // Send the token to same-origin, relative URLs only.
	                // Send the token only if the method warrants CSRF protection
	                // Using the CSRFToken value acquired earlier
	                xhr.setRequestHeader("X-CSRFToken", csrftoken);
	            }
	        }
	    });

	});


});





