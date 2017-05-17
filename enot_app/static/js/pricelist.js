



var cDir = Vue.extend({
    props: ['ttl', 'countries'],
    data: function(){
        return {
        };
    },
    template: '<div class="direction">\
                <h1>{{ttl}}</h1>\
                    <div class="country" v-for="(value, key, index) in countries">\
                          <h2 style="color:#f6931f">\
                            {{value.rus_name}}\
                            </h2>\
                          <div class="place" v-for="p in value.places">\
                              <div v-if="p.price<35000">\
                              <div class="place__name"> <a href="#"> <strong>{{p.name}}</strong></a> </div>\
                              <div class="place__price"><a href="#">{{p.price}}</a></div>\
                              <div class="clearfix"></div>\
                              </div>\
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
    mounted: function(){
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
                <c-dir ttl="Европа" :countries="bids.europe"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir ttl="Азия" :countries="bids[\'asia\'][\'countries\']"></c-dir>\
                <c-dir ttl="Австралия и Океания" :countries="bids[\'australia-and-oceania\'][\'countries\']"></c-dir>\
            </div>\
            <div class="col-lg-4">\
                <c-dir ttl="Северная Америка" :countries="bids[\'north-america\'][\'countries\']"></c-dir>\
                <c-dir ttl="Южная Америка" :countries="bids[\'south-america\'][\'countries\']"></c-dir>\
                <c-dir ttl="Африка" :countries="bids[\'africa\'][\'countries\']"></c-dir>\
            </div>\
        </div>'
});


Vue.component('slider', {
  props: ['range', 'initvalue', 'min', 'max'],
  template: '#slider-template',
  data: function(){
    return {
      value: this.initvalue
    }
  },
  mounted: function () {
    var vm = this;
    console.log(this.$el);
    $(this.$el).find('.wrapped-slider')
      .slider({
          range: "min",
          value: this.initvalue,
          min: 5000,
          max: 60000
      })
      .on('slidestop', function(event, ui){
        vm.$parent.$emit('slide', ui.value);
      })
      .on('slide', function(event, ui){
        vm.value = Math.floor(ui.value/5000)*5000;
      })
  },
  watch: {
    value: function (value) {
      $(this.$el).val(value).trigger('change');
    },
    options: function (options) {
      $(this.$el).select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})

var vm = new Vue({
  el: '#cpanel',
  template: '#cpanel-template',
  data: {
  },
  created: function(){
    this.$on('slide', function(value){
      console.log(value);
    });
  }
});