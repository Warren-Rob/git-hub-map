var cityPoint;
var infoWindow = new google.maps.InfoWindow({content: '' });

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
    lat = cities[city].lat
    lng = cities[city].lon
    users = cities[city].users //array

    var populationOptions = {
      map: map,
      draggable: false,
      animation: google.maps.Animation.DROP,
      position: new google.maps.LatLng(lat, lng)
    };

    console.log(populationOptions)
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
  }
}

google.maps.event.addDomListener(window, 'load', initialize);
