

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


var subscribeForm = new Vue({
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
});

var bidFeed = new Vue({
    el: '#bid-feed',
    data: {
        shownBids:[],
        allBids: []
    },
    ready: function(){
        var currentdate = new Date();
        var sc = currentdate.getSeconds();
        var self = this;
        getResults('/bid-feed', 'json', {}, function(res){
            if (res.success){
                self.allBids = res.bids;
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



            }
        });
    },
    methods: {
        sortBids: function(){
            function compareRating(a,b){
                if (a.rating>b.rating){
                    return -1;
                } else if (a.rating<b.rating){
                    return 1;
                } else {
                    return 0;
                }
            }
            this.shownBids.sort(compareRating);
        }
    }
});