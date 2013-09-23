var cityCircle;

function initialize() {
    console.log(cities)
    var mapOptions = {
	zoom: 4,
	center: new google.maps.LatLng(37.09024, -95.712891),
	mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    var map = new google.maps.Map(document.getElementById('map-canvas'),
				  mapOptions);

    for (var city in cities) {
	// Construct the circle for each value in citymap. We scale population by 20.
	console.log(city)
	var populationOptions = {
	    strokeColor: '#1783FF',
	    strokeOpacity: 0.8,
	    strokeWeight: 2,
	    fillColor: '#73B4FF',
	    fillOpacity: 0.35,
	    map: map,
	    center: new google.maps.LatLng(cities[city].lat, cities[city].lon),
	    radius: cities[city].count * 10000
	};
	console.log(populationOptions)
	cityCircle = new google.maps.Circle(populationOptions);
    }
}


google.maps.event.addDomListener(window, 'load', initialize);

