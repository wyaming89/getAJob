var vm=new Vue({
    el: '#app',
    data: {
        asidecomp: 'aside',
        items: [
            {name: '行业', key:'industry'},
            { name: '城市', key: 'city'},
            { name: '公司', key: 'company'},

        ],
        
    },
    
    mounted() {
        var echt1 = echarts.init(document.getElementById('part1'));
        var echt2 = echarts.init(document.getElementById('part2'));
        var echt3 = echarts.init(document.getElementById('part3'));
        var echt4 = echarts.init(document.getElementById('part4')); 
        $.get('/data', function (data) {
            echt1.setOption(data.res[1]);
            echt2.setOption(data.res[0]);
            echt3.setOption(data.res[2]);
            echt4.setOption(data.res[3]);
        })
        
    }, 
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        getindu (event) {
            $.get('/datas/'+event, function (data) {
                var echt = echarts.getInstanceByDom(document.getElementById('part1'))
                /* echt.setOption(data.res[0]); */
                console.log(data)
            }) 
            
        },
    },
    
    
})









