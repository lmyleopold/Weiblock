<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <link rel="icon"
          href="https://i0.hdslb.com/bfs/face/362805e8573cb396abada203596e80aab983f406.jpg@160w_160h_1c_1s.webp">

    <style>
        {{css|safe}}

    </style>

</head>
<body>
<!--<h1 class="heading">微博舆情监测与分析</h1>-->
<!--<a href="pie/" class="input">展示饼图统计</a>-->
<!--<div>-->

<!--    <h2 class="pie_text">情感分析统计饼图</h2>-->
<!--    <img src="https://s1.ax1x.com/2022/04/09/LiGrGT.png" alt="LiGrGT.png" class="pie"/>-->
<!--</div>-->
<!--<div class="pleftbox2top" style="width: 500px;height: 400px">-->
<!--    <h2 class="tith2">情感分析图</h2>-->
<!--    <div id="pleftbox2top" class="pleftbox2topcont"></div>-->
<!--</div>-->
<!-- Navbar -->
<nav id="navbar">
    <ul class="navbar-items flexbox-col">
        <li class="navbar-logo flexbox-left">
            <a class="navbar-item-inner flexbox">
                <svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 1438.88 1819.54">
                    <polygon points="925.79 318.48 830.56 0 183.51 1384.12 510.41 1178.46 925.79 318.48"/>
                    <polygon
                            points="1438.88 1663.28 1126.35 948.08 111.98 1586.26 0 1819.54 1020.91 1250.57 1123.78 1471.02 783.64 1663.28 1438.88 1663.28"/>
                </svg>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="search-outline">
                    </ion-icon>
                </div>
                <span class="link-text">中国地图</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left" href="">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="home-outline"></ion-icon>
                </div>
                <span class="link-text">Home</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="folder-open-outline"></ion-icon>
                </div>
                <span class="link-text">Projects</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="pie-chart-outline"></ion-icon>
                </div>
                <span class="link-text">Dashboard</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="people-outline"></ion-icon>
                </div>
                <span class="link-text">Team</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="chatbubbles-outline"></ion-icon>
                </div>
                <span class="link-text">Support</span>
            </a>
        </li>
        <li class="navbar-item flexbox-left">
            <a class="navbar-item-inner flexbox-left">
                <div class="navbar-item-inner-icon-wrapper flexbox">
                    <ion-icon name="settings-outline"></ion-icon>
                </div>
                <span class="link-text">Settings</span>
            </a>
        </li>
    </ul>
</nav>

<!-- Main -->
<main id="main" class="flexbox-col">
    <h2>微博舆情检测与分析</h2>
</main>
<div id="chinamap" style="height: 700px">
</div>
<!--<div id="area" style="height: 500px">-->
<!--</div>-->
<div id="pointmap" style="height: 500px">
</div>

<script src="https://cdn.staticfile.org/echarts/4.3.0/echarts.min.js"></script>
<!--<script>-->
<!--    let headers = JSON.parse('{{header|safe}}');-->
<!--    let nums = JSON.parse('{{num|safe}}');-->
<!--    console.log(nums)-->
<!--    let myChart = echarts.init(document.getElementById('pleftbox2top'));-->
<!--    option = {-->
<!--        tooltip: {//提示框组件-->
<!--            trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。-->
<!--            axisPointer: {-->
<!--                // 坐标轴指示器，坐标轴触发有效-->
<!--                // type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'-->
<!--            },-->
<!--            formatter: '{a} <br/>{b} : {c} <br/>百分比 : {d}%' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）-->
<!--        },-->
<!--        color: ['#d2d17c', '#00b7ee', '#5578cf', '#5ebbeb', '#d16ad8', '#f8e19a', '#00b7ee', '#81dabe', '#5fc5ce'],-->
<!--        backgroundColor: 'rgba(1,202,217,.2)',-->
<!--        // grid: {-->
<!--        //     left: 20,-->
<!--        //     right: 20,-->
<!--        //     top: 0,-->
<!--        //     bottom: 20-->
<!--        // },-->
<!--        legend: {-->
<!--            top: 10,-->
<!--            textStyle: {-->
<!--                fontSize: 23,-->
<!--                // color: 'rgba(255,255,255,.7)'-->
<!--            },-->
<!--            data: headers-->
<!--        },-->
<!--        series: [-->
<!--            {-->
<!--                name: '统计人数',-->
<!--                type: 'pie',-->
<!--                // radius: '55%',-->
<!--                // center: ['50%', '55%'],-->
<!--                data: nums,-->
<!--                textStyle: {-->
<!--                    fontSize: 23-->
<!--                }-->
<!--                // itemStyle: {-->
<!--                //     emphasis: {-->
<!--                //         shadowBlur: 10,-->
<!--                //         shadowOffsetX: 0,-->
<!--                //         shadowColor: 'rgba(0, 0, 0, 0.5)'-->
<!--                //     }-->
<!--                // }-->
<!--            }-->
<!--        ]-->
<!--    };-->
<!--    myChart.setOption(option);-->
<!--</script>-->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts-gl/dist/echarts-gl.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts-stat/dist/ecStat.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts/dist/extension/dataTool.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts/map/js/china.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts/map/js/world.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts/dist/extension/bmap.min.js"></script>
<script>
    let point = echarts.init(document.getElementById('pointmap'));
    const data = [
        {
            name: "0",
            fixed: true,
            x: point.getWidth() / 2,
            y: point.getHeight() / 2,
            symbolSize: 20,
            id: '-1'
        }
    ];
    const edges = [];
    option = {
        tooltip: {//提示框组件
            trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
            axisPointer: {
                // 坐标轴指示器，坐标轴触发有效
                // type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: '{c}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
        },
        series: [
            {
                type: 'graph',
                layout: 'force',
                animation: false,
                data: data,
                force: {
                    // initLayout: 'circular'
                    // gravity: 0
                    repulsion: 100,
                    edgeLength: 5
                },
                edges: edges
            }
        ]
    };
    point.setOption(option);
    // point.on('click', function (params) {
    //         {
    //             console.log(params);
    //         }
    //     });
    let points = JSON.parse('{{points|safe}}');
    for (let i = 0; i < points.length; i++) {
        data.push({
            name: i + 1,
            id: i
        });
        var source = points[i][0];
        var target = points[i][1];
        if (source !== target) {
            edges.push({
                source: source,
                target: target
            });
        }
    }
    let tooltip = {//提示框组件
        trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
        axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            // type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
        },
        formatter: '{b}{c}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    }
    point.setOption({

        series: [
            {
                // label: i,
                // focusNodeAdjacency: true,//加上后静止
                roam: true,
                data: data,
                edges: edges,
                tooltip: tooltip,
                itemStyle: {
                    normal: {
                        color: '#1890FF',
                        label: {
                            color: '#000', //字的颜色
                            borderColor: '#A618FF',  //拐点边框颜色
                            // show: true  //设置这个就会把值显示在图表上
                        },
                        lineStyle: {
                            color: '#A618FF',
                            width: 3
                        }
                    }
                },

            }
        ]
    })


    // setInterval(function () {
    //     data.push({
    //         id: data.length + ''
    //     });
    //     var source = Math.round((data.length - 1) * Math.random());
    //     var target = Math.round((data.length - 1) * Math.random());
    //     if (source !== target) {
    //         edges.push({
    //             source: source,
    //             target: target
    //         });
    //     }
    //     point.setOption({
    //         tooltip: {//提示框组件
    //             trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
    //             axisPointer: {
    //                 // 坐标轴指示器，坐标轴触发有效
    //                 type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
    //             },
    //             formatter: '{b}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    //         },
    //         series: [
    //             {
    //                 roam: true,
    //                 data: data,
    //                 edges: edges
    //             }
    //         ]
    //     });
    //     // console.log('nodes: ' + data.length);
    //     // console.log('links: ' + data.length);
    // }, 200);

</script>
<script>
    let mapchart = echarts.init(document.getElementById('chinamap'));
    var geoCoordMap = {
        "海门": [121.15, 31.89],
        "鄂尔多斯": [109.781327, 39.608266],
        "招远": [120.38, 37.35],
        "舟山": [122.207216, 29.985295],
        "齐齐哈尔": [123.97, 47.33],
        "盐城": [120.13, 33.38],
        "赤峰": [118.87, 42.28],
        "青岛": [120.33, 36.07],
        "乳山": [121.52, 36.89],
        "金昌": [102.188043, 38.520089],
        "泉州": [118.58, 24.93],
        "莱西": [120.53, 36.86],
        "日照": [119.46, 35.42],
        "胶南": [119.97, 35.88],
        "南通": [121.05, 32.08],
        "拉萨": [91.11, 29.97],
        "云浮": [112.02, 22.93],
        "梅州": [116.1, 24.55],
        "文登": [122.05, 37.2],
        "上海": [121.48, 31.22],
        "攀枝花": [101.718637, 26.582347],
        "威海": [122.1, 37.5],
        "承德": [117.93, 40.97],
        "厦门": [118.1, 24.46],
        "汕尾": [115.375279, 22.786211],
        "潮州": [116.63, 23.68],
        "丹东": [124.37, 40.13],
        "太仓": [121.1, 31.45],
        "曲靖": [103.79, 25.51],
        "烟台": [121.39, 37.52],
        "福州": [119.3, 26.08],
        "瓦房店": [121.979603, 39.627114],
        "即墨": [120.45, 36.38],
        "抚顺": [123.97, 41.97],
        "玉溪": [102.52, 24.35],
        "张家口": [114.87, 40.82],
        "阳泉": [113.57, 37.85],
        "莱州": [119.942327, 37.177017],
        "湖州": [120.1, 30.86],
        "汕头": [116.69, 23.39],
        "昆山": [120.95, 31.39],
        "宁波": [121.56, 29.86],
        "湛江": [110.359377, 21.270708],
        "揭阳": [116.35, 23.55],
        "荣成": [122.41, 37.16],
        "连云港": [119.16, 34.59],
        "葫芦岛": [120.836932, 40.711052],
        "常熟": [120.74, 31.64],
        "东莞": [113.75, 23.04],
        "河源": [114.68, 23.73],
        "淮安": [119.15, 33.5],
        "泰州": [119.9, 32.49],
        "南宁": [108.33, 22.84],
        "营口": [122.18, 40.65],
        "惠州": [114.4, 23.09],
        "江阴": [120.26, 31.91],
        "蓬莱": [120.75, 37.8],
        "韶关": [113.62, 24.84],
        "嘉峪关": [98.289152, 39.77313],
        "广州": [113.23, 23.16],
        "延安": [109.47, 36.6],
        "太原": [112.53, 37.87],
        "清远": [113.01, 23.7],
        "中山": [113.38, 22.52],
        "昆明": [102.73, 25.04],
        "寿光": [118.73, 36.86],
        "盘锦": [122.070714, 41.119997],
        "长治": [113.08, 36.18],
        "深圳": [114.07, 22.62],
        "珠海": [113.52, 22.3],
        "宿迁": [118.3, 33.96],
        "咸阳": [108.72, 34.36],
        "铜川": [109.11, 35.09],
        "平度": [119.97, 36.77],
        "佛山": [113.11, 23.05],
        "海口": [110.35, 20.02],
        "江门": [113.06, 22.61],
        "章丘": [117.53, 36.72],
        "肇庆": [112.44, 23.05],
        "大连": [121.62, 38.92],
        "临汾": [111.5, 36.08],
        "吴江": [120.63, 31.16],
        "石嘴山": [106.39, 39.04],
        "沈阳": [123.38, 41.8],
        "苏州": [120.62, 31.32],
        "茂名": [110.88, 21.68],
        "嘉兴": [120.76, 30.77],
        "长春": [125.35, 43.88],
        "胶州": [120.03336, 36.264622],
        "银川": [106.27, 38.47],
        "张家港": [120.555821, 31.875428],
        "三门峡": [111.19, 34.76],
        "锦州": [121.15, 41.13],
        "南昌": [115.89, 28.68],
        "柳州": [109.4, 24.33],
        "三亚": [109.511909, 18.252847],
        "自贡": [104.778442, 29.33903],
        "吉林": [126.57, 43.87],
        "阳江": [111.95, 21.85],
        "泸州": [105.39, 28.91],
        "西宁": [101.74, 36.56],
        "宜宾": [104.56, 29.77],
        "呼和浩特": [111.65, 40.82],
        "成都": [104.06, 30.67],
        "大同": [113.3, 40.12],
        "镇江": [119.44, 32.2],
        "桂林": [110.28, 25.29],
        "张家界": [110.479191, 29.117096],
        "宜兴": [119.82, 31.36],
        "北海": [109.12, 21.49],
        "西安": [108.95, 34.27],
        "金坛": [119.56, 31.74],
        "东营": [118.49, 37.46],
        "牡丹江": [129.58, 44.6],
        "遵义": [106.9, 27.7],
        "绍兴": [120.58, 30.01],
        "扬州": [119.42, 32.39],
        "常州": [119.95, 31.79],
        "潍坊": [119.1, 36.62],
        "重庆": [106.54, 29.59],
        "台州": [121.420757, 28.656386],
        "南京": [118.78, 32.04],
        "滨州": [118.03, 37.36],
        "贵阳": [106.71, 26.57],
        "无锡": [120.29, 31.59],
        "本溪": [123.73, 41.3],
        "克拉玛依": [84.77, 45.59],
        "渭南": [109.5, 34.52],
        "马鞍山": [118.48, 31.56],
        "宝鸡": [107.15, 34.38],
        "焦作": [113.21, 35.24],
        "句容": [119.16, 31.95],
        "北京": [116.46, 39.92],
        "徐州": [117.2, 34.26],
        "衡水": [115.72, 37.72],
        "包头": [110, 40.58],
        "绵阳": [104.73, 31.48],
        "乌鲁木齐": [87.68, 43.77],
        "枣庄": [117.57, 34.86],
        "杭州": [120.19, 30.26],
        "淄博": [118.05, 36.78],
        "鞍山": [122.85, 41.12],
        "溧阳": [119.48, 31.43],
        "库尔勒": [86.06, 41.68],
        "安阳": [114.35, 36.1],
        "开封": [114.35, 34.79],
        "济南": [117, 36.65],
        "德阳": [104.37, 31.13],
        "温州": [120.65, 28.01],
        "九江": [115.97, 29.71],
        "邯郸": [114.47, 36.6],
        "临安": [119.72, 30.23],
        "兰州": [103.73, 36.03],
        "沧州": [116.83, 38.33],
        "临沂": [118.35, 35.05],
        "南充": [106.110698, 30.837793],
        "天津": [117.2, 39.13],
        "富阳": [119.95, 30.07],
        "泰安": [117.13, 36.18],
        "诸暨": [120.23, 29.71],
        "郑州": [113.65, 34.76],
        "哈尔滨": [126.63, 45.75],
        "聊城": [115.97, 36.45],
        "芜湖": [118.38, 31.33],
        "唐山": [118.02, 39.63],
        "平顶山": [113.29, 33.75],
        "邢台": [114.48, 37.05],
        "德州": [116.29, 37.45],
        "济宁": [116.59, 35.38],
        "荆州": [112.239741, 30.335165],
        "宜昌": [111.3, 30.7],
        "义乌": [120.06, 29.32],
        "丽水": [119.92, 28.45],
        "洛阳": [112.44, 34.7],
        "秦皇岛": [119.57, 39.95],
        "株洲": [113.16, 27.83],
        "石家庄": [114.48, 38.03],
        "莱芜": [117.67, 36.19],
        "常德": [111.69, 29.05],
        "保定": [115.48, 38.85],
        "湘潭": [112.91, 27.87],
        "金华": [119.64, 29.12],
        "岳阳": [113.09, 29.37],
        "长沙": [113, 28.21],
        "衢州": [118.88, 28.97],
        "廊坊": [116.7, 39.53],
        "菏泽": [115.480656, 35.23375],
        "合肥": [117.27, 31.86],
        "武汉": [114.31, 30.52],
        "大庆": [125.03, 46.58]
    };

    let option = {
        tooltip: {//提示框组件
            trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
            axisPointer: {
                // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: '{b}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
        },
        // visualMap: {           //地图图例
        //     show: true,
        //     left: 26,
        //     bottom: 40,
        //     showLabel: true,
        // pieces: [        //根据数据大小，各省显示不同颜色
        //     {
        //         gte: 100,
        //         label: ">= 1000",
        //         color: "#1f307b"
        //     },
        //     {
        //         gte: 500,
        //         lt: 999,
        //         label: "500 - 999",
        //         color: "#3c57ce"
        //     },
        //     {
        //         gte: 100,
        //         lt: 499,
        //         label: "100 - 499",
        //         color: "#6f83db"
        //     },
        //     {
        //         gte: 10,
        //         lt: 99,
        //         label: "10 - 99",
        //         color: "#9face7"
        //     },
        //     {
        //         lt: 10,
        //         label: '<10',
        //         color: "#bcc5ee"
        //     }
        // ],

        geo: {                 //中国地图设置
            map: "china",
            // scaleLimit: {
            //   min: 1,
            //   max: 2
            // },
            zoom: 1,
            // top: 120,
            label: {
                normal: {
                    show: true,
                    fontSize: "14",
                    color: "rgba(0,0,0,0.7)"
                }
            },
            itemStyle: {
                normal: {
                    borderColor: "rgba(129,73,73,0.2)"
                },
                emphasis: {
                    areaColor: "#f80000",
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    borderWidth: 0,
                }
            }
        },
        series: [
            {
                // nam  e: "突发事件",
                type: "map",
                geoIndex: 0,
                // data: geoCoordMap
            }
        ]
    };
    // mapchart.on('click', function (params) {
    //     if (params['name']==='西藏')
    //     let area = echarts.init(document.getElementById('area'));
    //     let option={
    //
    //     }
    // });
    mapchart.setOption(option);
</script>
</body>
</html>