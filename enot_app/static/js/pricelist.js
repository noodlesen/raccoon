/*$( function() {
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
);*/



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
                            <div v-if="p.price<15000">\
                            <div class="place__name"> <a href="#"> <strong>{{p.name}}</strong> ({{p.pcount}}) </a> </div>\
                            <div class="place__price"><a href="#">{{p.price}}</a></div>\
                            <div class="place__stops"><a href="#">1C</a></div>\
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


Vue.component('select2', {
  props: ['options', 'value'],
  template: '#select2-template',
  mounted: function () {
    var vm = this
    $(this.$el)
      // init select2
      .select2({ data: this.options })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', this.value)
      })
  },
  watch: {
    value: function (value) {
      // update value
      $(this.$el).val(value).trigger('change');
    },
    options: function (options) {
      // update options
      $(this.$el).select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})

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
      // init select2
      /*.select2({ data: this.options })
      .val(this.value)
      .trigger('change')*/
      .slider({
          range: "min",
          value: this.initvalue,
          min: 5000,
          max: 100000
      })
      .on('slidestop', function(event, ui){
        vm.$parent.$emit('slide', ui.value);
      })
      .on('slide', function(event, ui){
        vm.value = ui.value;
      })
      // emit event on change.
   /*   .on('change', function () {
        vm.$emit('input', this.value)
      })*/
  },
  watch: {
    value: function (value) {
      // update value
      $(this.$el).val(value).trigger('change');
    },
    options: function (options) {
      // update options
      $(this.$el).select2({ data: options })
    }/*,
    slide: function(value){
      console.log('ddd')
    }*/
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})

var vm = new Vue({
  el: '#cpanel',
  template: '#cpanel-template',
  data: {
/*    selected: 2,
    options: [
      { id: 1, text: 'Hello' },
      { id: 2, text: 'World' }
    ]*/
  },
  created: function(){
    this.$on('slide', function(value){
      console.log(value);
    });
  }
});