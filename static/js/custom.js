
function initMap(){
	var input = document.getElementById('autocomplete');
    var autocomplete = new google.maps.places.Autocomplete(input);

}

$(document).ready(function() {
    $body = $("body");
    $("#modal-display").click(function() {
        $body.addClass("loading");
    });
});
