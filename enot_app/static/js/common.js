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

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
        console.log(csrftoken);
    }
})

function getResults(route, resultType, formData, callback){
	$.ajax(route,{
		type: 'post',
		data: JSON.stringify(formData, null, '\t'),
		dataType: resultType,
		contentType: 'application/json;charset=UTF-8',
		success: function(result){
			callback(result);
		},
		error: function(result){
			console.log(result);
			alert('Something went wrong :( \nTry to reload this page (F5 or Ctrl+R)');
			//location.reload();
		}
	});
}




