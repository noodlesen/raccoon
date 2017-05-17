var bus = new Vue({});

Vue.component('c-button',{
    props:['mark', 'wrap'],
    methods:{
        emitEvent:function(){
            bus.$emit('pb', {emitter:this.mark});
            console.log('!');
        }
    },
    created: function(){
        var self = this;
        
        bus.$on('changed', function(){
            console.log('CATCHED!');
        });
    },
    template:'<button class="c-button btn {{wrap}}" v-on:click="emitEvent"><slot></slot></button>'
});


var vm = new Vue({
    el:'#el',
    data:{
        pressed1: 'No',
        pressed2: 'No'
    },
    template:'<div><c-button>PRESS1</c-button><span>{{pressed1}}</span><c-button>PRESS2</c-button><span>{{pressed2}}</span></div>',
    created: function(){
        var self = this;

        bus.$on('pb', function(value){
          self.pressed1 = 'YES!';
          bus.$emit('changed');
        });

        
  }
});

