var cityPoint;

function initialize() {
  console.log(cities);
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(37.09024, -95.712891),
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'),
                                mapOptions);

  for (var city in cities) {
    console.log(city)
    var populationOptions = {
      map: map,
      draggable: false,
      animation: google.maps.Animation.DROP,
      position: new google.maps.LatLng(cities[city].lat, cities[city].lon)
    };

    console.log(populationOptions)
    cityPoint = new google.maps.Marker(populationOptions);

    function addInfoWindow(marker, message) {
      var info = message;

      var infoWindow = new google.maps.InfoWindow({
        content: message
      });

      google.maps.event.addListener(marker, 'click', function() {
        infoWindow.open(map, marker);
      });
    }

    addInfoWindow(cityPoint, "debug");
  }
}

google.maps.event.addDomListener(window, 'load', initialize);
