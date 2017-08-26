(function($){

	function getOffset( el ) {
		var _x = 0;
		var _y = 0;
		while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
			_x += el.offsetLeft - el.scrollLeft;
			_y += el.offsetTop - el.scrollTop;
			el = el.offsetParent;
		}
		return { top: _y, left: _x };
	}
	
	$(function(){
		$('#example1 .htContainer:first-child .ht_master:first table.htCore:first > tbody > tr:first-child > td:nth-child(n+5)').each(function(index){

			var offset = getOffset(this).left + $(window).scrollLeft();
			$('body').prepend('<div class="scroll_fixed_top hide" style="position:absolute;z-index:1000; left: '+offset+'px;">'
				+$(this).text()
				+'</div>'
			);
		});
		var titles = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
		$('#example1 .htContainer:first-child .ht_master:first table.htCore:first > tbody > tr > td[rowspan="14"]').each(function(index){
			var offset = getOffset(this).top + $(window).scrollTop();
			$('body').prepend('<div id="scroll_fixed_left_'+index+'" class="scroll_fixed_left hide" style="position:absolute;z-index:1000;margin-top:-1px; top:'+offset+'px; ">'
				+titles[index]+'</div>'
			);
		});

		
		//var top = $('.scroll_fixed_top').eq(0).offset().top - parseFloat($('.scroll_fixed_top').eq(0).css('margin-top').replace(/auto/, 0));
		
		var $captions_left = $(".scroll_fixed_left");
			$captions_left.each(function(){
				$(this).data('left_init', 0);//$(this).offset().left);
			});
		var $captions_top = $(".scroll_fixed_top");
			$captions_top.each(function(){
				$(this).data('top_init', 0);
			});

		$(window).scroll(function(event) {
		
			var x = $(this).scrollLeft();
			var y = $(this).scrollTop();

			// whether that's below the form
			if (y >= 100) {
				// if so, ad the fixed class
				if ($captions_top.eq(0).hasClass('hide')) {
					$captions_top.removeClass('hide');
				}				
			} else {
				// otherwise remove it
				if (!$captions_top.eq(0).hasClass('hide')) {
					$captions_top.addClass('hide');
				}
			}
			
			if (x >= 140) {
				// if so, ad the fixed class
				if ($captions_left.eq(0).hasClass('hide')) {
					$captions_left.removeClass('hide');
				}
				
			} else {
				if (!$captions_left.eq(0).hasClass('hide')) {
					$captions_left.addClass('hide');
				}
			}					

			$captions_left.each(function(){
				$(this).offset({
					left: x + $(this).data('left_init')
				});
			});
			$captions_top.each(function(){
				$(this).offset({
					top: y + $(this).data('top_init')
				});
			});
		});
	});

})(jQuery);