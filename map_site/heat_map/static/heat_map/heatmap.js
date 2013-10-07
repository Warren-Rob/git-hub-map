var map, cityPoint, cityData, heatmap;
var markers = [];
var infoWindow = new google.maps.InfoWindow({content: '' });

function initialize() {
    console.log(cities);
    var citylist = [];
    var mapOptions = {
	zoom: 3,
	center: new google.maps.LatLng(25.9923503, -31.9631969),
	mapTypeId: google.maps.MapTypeId.ROADMAP
	//	disableDefaultUI: false,
    };

    
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);

    heatmap = new HeatmapOverlay(map, {
	"radius":8,
	"visible":true,
	"opacity":60
    });
    
    for (var city in cities) {
	lat = cities[city].lat;
	lng = cities[city].lon;
	users = cities[city].users; //array
	var numUsers = 0;
	for(var u in users){
	    numUsers += 1;	    
	}
	citylist.push({
	    lat: lat,
	    lng: lng,
	    count: numUsers
	}
		     );
	var populationOptions = {
	    map: null,
	    draggable: false,
	    animation: google.maps.Animation.DROP,
	    position: new google.maps.LatLng(lat, lng)
	};

	cityPoint = new google.maps.Marker(populationOptions);

	function addInfoWindow(marker, message) {
	    var info = message;

	    google.maps.event.addListener(marker, 'click', function() {
		infoWindow.setContent(message);
		infoWindow.open(map, marker);
	    });
	}

	str = "<b>Users from " + city + ":</b> </br>";
	for (var u in users) { str += "> " + users[u].login + "</br>"; }

	addInfoWindow(cityPoint, str);
	markers.push(cityPoint);
    }

    cityData = {
	max: 400,
	data: citylist
	};

    google.maps.event.addListener(map, "idle", function(){
	if (map.zoom <= 6 && heatmap.data == null){
	    heatmap.setDataSet(cityData);
	}
	if(map.zoom <= 6){
	    console.log("setting data");
	    heatmap.setMap(map);
	} else {
	    hideHeatmap();
	}	
    });

    google.maps.event.addListenerOnce(map, 'tilesloaded', function(){
	if (map.zoom <= 7 && heatmap.data == null){
	    heatmap.setDataSet(cityData);
	}
	if(map.zoom <= 7){
	    console.log("setting data");
	    heatmap.setMap(map);
	} else {
	    hideHeatmap();
	}
    });
    google.maps.event.addListener( map, 'zoom_changed', function(){
	console.info(map.center);
	if(map.zoom ==  8) {
//	    hideHeatmap();
	    showMarkers();
	}
	if(map.zoom == 7){
	    hideMarkers();
//	    showHeatmap();
	}
	
    });

    console.log(citylist);

    
    
    //    heatmap.setMap(map);
    
    
}

function associateMarkers(map){
    console.info("Toggle Markers");
    for(var i = 0; i < markers.length; i++){

	markers[i].setMap(map);
    }
}

function showMarkers() {
    associateMarkers(map);
}

function hideMarkers() {
    associateMarkers(null);
}

function showHeatmap() {
    heatmap.setDataSet(cityData);
    heatmap.map = map;
    
    heatmap.visible = true;
    
}

function hideHeatmap() {
   // heatmap.setDataSet(null);
    //heatmap.map = null;
    heatmap.visible = false;
    
}

google.maps.event.addDomListener(window, 'load', initialize);
