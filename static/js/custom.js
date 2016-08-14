
function initMap(){
	var input = document.getElementById('autocomplete');
    var autocomplete = new google.maps.places.Autocomplete(input);

    var map;
	map = new google.maps.Map(document.getElementById('map'), {
		center: {
			lat: -34.397,
			lng: 150.644
		},
		zoom: 8
	});
}



$(document).ready(function() {
    $body = $("body");
    $("#modal-display").click(function() {
        $body.addClass("loading");
    });
});
