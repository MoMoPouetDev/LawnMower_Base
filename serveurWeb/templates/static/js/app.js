var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'message', function( msg ) {
  console.log( msg )
  var elementStatus = document.getElementById("status");
  elementStatus.innerHTML = msg.status;
  var elementError = document.getElementById("error");
  elementError.innerHTML = msg.error;
  var elementLatitude = document.getElementById("latitude");
  elementLatitude.innerHTML = msg.latitude;
  var elementLongitude = document.getElementById("longitude");
  elementLongitude.innerHTML = msg.longitude;
  var elementHeures = document.getElementById("heures");
  elementHeures.innerHTML = msg.heures;
  var elementMinutes = document.getElementById("minutes");
  elementMinutes.innerHTML = msg.minutes;
  var elementJours = document.getElementById("jours");
  elementJours.innerHTML = msg.jours;
  var elementMois = document.getElementById("mois");
  elementMois.innerHTML = msg.mois;
  var elementAnnee = document.getElementById("annee");
  elementAnnee.innerHTML = msg.annee;
})

function sendStart() {
  socket.emit('command', {
    command : 'Start'
  })
}

function sendStop() {
  socket.emit('command', {
    command : 'Stop'
  })
}

function initMap() {
  var baseCoordinates = {lat: 49.231761, lng: 1.246831};
  var workingCoordinates = [
    baseCoordinates
  ];
  console.log(workingCoordinates);
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 49.231649, lng: 1.246940},
    zoom: 21,
    scrollwheel: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false,
    draggable: false,
    disableDefaultUI: true,
    mapTypeId: 'satellite'
  });
  var marker = new google.maps.Marker({
    position: baseCoordinates,
    map: map,
    title: 'Station'
  });
  var workingPath = new google.maps.Polyline({
    path: workingCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });
  workingPath.setMap(map);
}