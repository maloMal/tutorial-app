$(document).ready(function(){



	//like button

	$('#likes').click(function(){
		var cat_id;
		cat_id = $(this).attr("data-catid");

		$.get('/like_category/', {category_id : cat_id}, function(){
			$('#like-count').html(data);
			$('#likes').hide();


	})

});