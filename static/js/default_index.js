// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array.
    var enumerate = function(v) {
        var k=0;
        return v.map(function(e) {e._idx = k++;});
    };

    function get_listings_url() {
        return listings_url;
    }

    self.del_listing = function(listing_idx) {
        $.post(del_listing_url,
            { listing_id: self.vue.listings[listing_idx].id},
            function () {
                self.vue.listings.splice(listing_idx,1);
                enumerate(self.vue.listings);
            }
        )
    };

    self.get_listings = function () {
        $.getJSON(get_listings_url(),  $.param({q: self.vue.search_string}), function (data) {
            self.vue.listings = data.listings;
            self.vue.logged_in = data.logged_in;
            enumerate(self.vue.listings);
        });
        if (self.vue.poi != null) {
            for (i = 0; i < self.vue.listings.length;i++){
                self.get_distance(i);
            }
        }
    };

    self.get_distance = function(listing_idx) {
        var origin = self.vue.listings[listing_idx].housing_available;

        var destination = self.vue.poi;
        var service = new google.maps.DistanceMatrixService();

        service.getDistanceMatrix(
        {
            origins: [origin],
            destinations: [destination],
            travelMode: google.maps.TravelMode.DRIVING,
            avoidHighways: false,
            avoidTolls: false
        },
        callback
        );

        function callback(response, status) {
        if(status=="OK") {
            var orig = response.originAddresses[0];
            var dest = response.destinationAddresses[0];
            self.vue.listings[listing_idx].distance= response.rows[0].elements[0].distance.text;
            //self.vue.listings[listing_idx].whatever= response.rows[0].elements[0].duration.text;
        } else {
            alert("Error: " + status);
            }
        }
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: false,
            form_name: null,
            form_email: null,
            form_phone: null,
            form_housing: null,
            form_vtype: null,
            form_long: false,
            form_short: false,
            selected: null,
            auto_name: null,
            auto_email: null,
            auto_phone: null,
            listings: [],
            search_string: '',
            poi: null,
        },
        methods: {
            get_listings: self.get_listings,
            search_it: self.get_listings,
            del_listing: self.del_listing,
            get_distance: self.get_distance
        }

    });
    self.get_listings();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
