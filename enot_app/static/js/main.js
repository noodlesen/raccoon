

Vue.transition('fade', {
  css: false,
  enter: function (el, done) {
    // element is already inserted into the DOM
    // call done when animation finishes.
    $(el)
      .css('opacity', 0)
      .animate({ opacity: 1 }, 1000, done)
  },
  enterCancelled: function (el) {
    $(el).stop()
  },
  leave: function (el, done) {
    // same as enter
    $(el).animate({ opacity: 0 }, 1000, done)
  },
  leaveCancelled: function (el) {
    $(el).stop()
  }
})


Vue.transition('stagger', {
  stagger: function (index) {
    // increase delay by 50ms for each transitioned item,
    // but limit max delay to 300ms
    return Math.min(300, index * 50)
  }
})


/*var subscribeForm = new Vue({
    el: '#subscription',
    data: {
        email:'',
        sent: false,
        showBlock: true
    },
    methods: {
        saveEmail: function(){
            var self = this;
            getResults('/save-email','json',{email: this.email}, function(res){
                if (res.success){
                    self.sent = true;
                }
            });
        },
        hideBlock: function(){
            this.showBlock = false;
        }
    }
});*/

var cDir = Vue.extend({
    props: ['bids','ttl'],
    data: function(){
        return {
        };
    },
    template: ' <div class="direction">\
                    <h1>{{ttl}}</h1>\
                    <div class="country" v-for="b in bids">\
                        <h2>{{b.name}}</h2>\
                        <div class="place" v-for="p in b.places">\
                            <div class="place__name"> <a href="#"> {{p.name}} </a> </div>\
                            <div class="place__price"><a href="#">{{p.price}}</a></div>\
                            <div class="place__stops"><a href="#">1C</a></div>\
                            <div class="place__more"><a href="#">23+</a></div>\
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
/*        var currentdate = new Date();
        var sc = currentdate.getSeconds();*/
        var self = this;

        getResults('/structured-feed', 'json', {}, function(res){
            if (res.success){
/*                self.allBids = res.bids;
                var i=0;

                setTimeout(function cycle(){
                    i++;
                    if (self.allBids.length>0){
                        var ri = Math.floor(Math.random() * self.allBids.length);
                        self.shownBids.push(self.allBids.splice(ri,1)[0]);
                        self.sortBids();
                    } else {
                    }
                    setTimeout(cycle, i*100+Math.floor((Math.sin(i+sc)+1)*750));
                },1500);

*/              console.log('success');
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
                <c-dir :ttl="Европа" :bids="bids[\'Европа\'][\'countries\']"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir :ttl="Азия" :bids="bids[\'Азия\'][\'countries\']"></c-dir>\
                <c-dir :ttl="Австралия и Океания" :bids="bids[\'Австралия и Океания\'][\'countries\']"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir :ttl="Северная Америка" :bids="bids[\'Северная Америка\'][\'countries\']"></c-dir>\
                <c-dir :ttl="Южная Америка" :bids="bids[\'Южная Америка\'][\'countries\']"></c-dir>\
                <c-dir :ttl="Африка" :bids="bids[\'Африка\'][\'countries\']"></c-dir>\
            </div>\
        </div>'
});