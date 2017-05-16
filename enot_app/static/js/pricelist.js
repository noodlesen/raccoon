$( function() {
    console.log('hello!')
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 37,
      min: 1,
      max: 700,
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.value );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range-min" ).slider( "value" ) );
  }
);



var cDir = Vue.extend({
    props: ['ttl', 'bids'],
    data: function(){
        return {
        };
    },
    template: ' <div class="direction">\
                    <h1>{{ttl}}</h1>\
                    <div class="country" v-for="b in bids">\
                        <h2>{{b.name}}</h2>\
                        <div class="place" v-for="p in b.places">\
                            <div class="place__name"> <a href="#"> <strong>{{p.name}}</strong> ({{p.pcount}}) </a> </div>\
                            <div class="place__price"><a href="#">{{p.price}}</a></div>\
                            <div class="place__stops"><a href="#">1C</a></div>\
                            <div class="clearfix"></div>\
                        </div>\
                    </div>\
                </div>'
});

Vue.component('c-dir', cDir);




var directions = new Vue({
    el: '#directions',
    data: {
        bids:{}
    },
    ready: function(){
        var self = this;
        getResults('/structured-feed', 'json', {}, function(res){
            if (res.success){
                console.log('success');
                self.bids = res.bids;
                console.log(JSON.stringify(self.bids));
            } else {
                console.log('error');
            }
        });
    },
    methods: {

    },
    template: '<div>\
            <div class="col-lg-4">\
                <c-dir ttl="Европа" :bids="bids[\'Европа\'][\'countries\']"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir ttl="Азия" :bids="bids[\'Азия\'][\'countries\']"></c-dir>\
                <c-dir ttl="Австралия и Океания" :bids="bids[\'Австралия и Океания\'][\'countries\']"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir ttl="Северная Америка" :bids="bids[\'Северная Америка\'][\'countries\']"></c-dir>\
                <c-dir ttl="Южная Америка" :bids="bids[\'Южная Америка\'][\'countries\']"></c-dir>\
                <c-dir ttl="Африка" :bids="bids[\'Африка\'][\'countries\']"></c-dir>\
            </div>\
        </div>'
});