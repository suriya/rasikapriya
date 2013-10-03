(function ($) {
  function centerMap(map, address) {
    if (address) {
      var geocoder = new google.maps.Geocoder();
      geocoder.geocode({ 'address': address }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          map.setCenter(results[0].geometry.location);
          map.setZoom(17);
          return new google.maps.Marker({
              map: map,
              position: results[0].geometry.location
          });
        } else {
          console.log("Geocode was not successful for the following reason: " + status);
        }
      });
    }
  }

  function initialize() {
    function initWidget(map_canvas) {
      function isMatchingClassName(s) {
        return s.match(/^places-autocomplete-corresponding-input-/);
      }
      var input_id = map_canvas.className.trim().split(' ').filter(isMatchingClassName)[0].replace(/^places-autocomplete-corresponding-input-/, '');
      var input = /** @type {HTMLInputElement} */(document.getElementById(input_id));
      var address = input.value;

      var mapOptions = {
        center: new google.maps.LatLng(13.08, 80.27),
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var map = new google.maps.Map(map_canvas, mapOptions);
      var centerMarker = centerMap(map, address);
      var autocomplete = new google.maps.places.Autocomplete(input);
      autocomplete.bindTo('bounds', map);

      var infowindow = new google.maps.InfoWindow();
      var marker = new google.maps.Marker({
        map: map
      });

      google.maps.event.addListener(autocomplete, 'place_changed', function() {
        if (centerMarker) {
          centerMarker.setVisible(false);
        }
        infowindow.close();
        marker.setVisible(false);
        input.className = input.className.replace(/places-autocomplete-notfound/, '');
        var place = autocomplete.getPlace();
        if (!place.geometry) {
          // Inform the user that the place was not found and return.
          input.className += ' places-autocomplete-notfound';
          return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
          map.fitBounds(place.geometry.viewport);
        } else {
          map.setCenter(place.geometry.location);
          map.setZoom(17);  // Why 17? Because it looks good.
        }
        marker.setIcon(/** @type {google.maps.Icon} */({
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(35, 35)
        }));
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        var address = '';
        if (place.address_components) {
          address = [
            (place.address_components[0] && place.address_components[0].short_name || ''),
            (place.address_components[1] && place.address_components[1].short_name || ''),
            (place.address_components[2] && place.address_components[2].short_name || '')
          ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map, marker);
      });
    }
    $('.places-autocomplete-map-canvas').each(function (i, div) {
      initWidget(div);
    });
  }
  $(document).ready(initialize);
})(
  ((typeof django !== "undefined" && django !== null) && (django.jQuery != null)) ?
    django.jQuery :
    (typeof jQuery !== "undefined" && jQuery !== null) ?
      jQuery :
      ($ != null) ?
        $ :
        void 0
);
