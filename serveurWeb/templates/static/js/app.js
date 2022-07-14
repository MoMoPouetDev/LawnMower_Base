$( window ).on( "load", function() {
    setInterval(function() { 
        fetch('/ble')
            .then(function (response) {
                return response.json();
            }).then(function (msg) {
                    
                    console.log(msg);
                    if( msg.connection ) {
                        if(!alert('Disconnection Detected')) {
                            window.location.reload();
                        }
                    }
                    else {
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
                        var elementBatterie = document.getElementById("pourcentage");
                        elementBatterie.innerHTML = msg.batterie;
                        batterie(msg.batterie);
                        angleFromNorth(msg.angle);
                    }
          }); 
    }, 500);  
});

function batterie(batterieLevel) {
    let full = document.getElementById("full");
    let half = document.getElementById("half");
    let empty = document.getElementById("empty");
    let charge = document.getElementById("charge");
    
    if (batterieLevel >= 75) {
        full.style.display = "block";
        half.style.display = "none";
        empty.style.display = "none";
        charge.style.display = "none";
    }
    else if ((batterieLevel >= 25) && (batterieLevel < 75)) {
        full.style.display = "none";
        half.style.display = "block";
        empty.style.display = "none";
        charge.style.display = "none";
    }   
    else {
        full.style.display = "none";
        half.style.display = "none";
        empty.style.display = "block";
        charge.style.display = "none";
    }   

}

function angleFromNorth(angle) {
    $('#mower').css('transform','rotate(' + angle + 'deg)');
}

function sendStart() {
    fetch('/start', {
        method: 'POST',
        body: JSON.stringify({
            command: "start"
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            console.log(json);
        });    
}

function sendStop() {
    fetch('/stop', {
        method: 'POST',
        body: JSON.stringify({
            command: "stop"
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            console.log(json);
        });
}

function initMap() {
  var baseCoordinates = {lat: 49.231761, lng: 1.246831};
  var workingCoordinates = [
    baseCoordinates
  ];
  console.log(workingCoordinates);
  const map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 49.231649, lng: 1.246940},
    zoom: 21,
    scrollwheel: false,
    navigationControl: true,
    mapTypeControl: false,
    scaleControl: true,
    draggable: false,
    disableDefaultUI: true,
    mapTypeId: 'satellite'
  });
  const image = '/serveurWeb/templates/static/images/maker.png';
  const marker = new google.maps.Marker({
    position: baseCoordinates,
    map: map,
    icon: image,
    title: 'Station'
  });
  const workingPath = new google.maps.Polyline({
    path: workingCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });
  workingPath.setMap(map);
}
