var map, cityData, heatmap;

function initialize() {
  console.log(cities);
  var citylist = [];
  var mapOptions = {
    zoom: 3,
    center: new google.maps.LatLng(25.9923503, -31.9631969),
    mapTypeId: google.maps.MapTypeId.ROADMAP
    // disableDefaultUI: false,
  };

  map = new google.maps.Map(document.getElementById('map-canvas'), 
                            mapOptions);

  heatmap = new HeatmapOverlay(map, {
    "radius": 20,
    "visible": true,
    "opacity": 75
  });

  for (var city in cities) {
    lat = cities[city].lat;
    lng = cities[city].lon;
    users = cities[city].users; // array

    var numUsers = users.length;

    citylist.push({
      lat: lat,
      lng: lng,
      count: numUsers
    });
  }

  cityData = {
    max: 400,
    data: citylist
  };

  google.maps.event.addListenerOnce(map, "idle", function() {
    heatmap.setDataSet(cityData);
  });

  heatmap.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initialize);
