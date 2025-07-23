<template>
    <div class="container">
        <h1>CS 交易管理系统</h1>
        <p>欢迎，{{ username }}！</p>

        <nav>
            <router-link to="/profit">查看盈利交易</router-link>
            <router-link to="/loss">查看亏损交易</router-link>
            <router-link to="/search">搜索交易记录</router-link>
            <router-link to="/add_trade">添加交易</router-link>
            <router-link to="/import_csv">导入交易记录</router-link>
            <a href="http://localhost:10000/export">导出交易记录</a>
            <a href="#" @click.prevent="logout">登出</a>
        </nav>

        <h2>交易总览</h2>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 2rem;">
            <div style="width: 510px;">
                <VueUiXy :config="config1" :dataset="dataset1" />
            </div>
            <div style="width: 400px;">
                <VueUiDonut :config="config2" :dataset="dataset2" />
            </div>
        </div>
        <h2></h2>
        <table>
            <thead>
                <tr>
                    <th>总交易数</th>
                    <th>总买入价</th>
                    <th>总卖出价</th>
                    <th>总收益</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{ total_trades }}</td>
                    <td>{{ total_purchase_price }}</td>
                    <td>{{ total_sell_price }}</td>
                    <td>{{ total_income }}</td>
                </tr>
            </tbody>
        </table>

        <h2>交易列表</h2>
        <table>
            <thead>
                <tr>
                    <th>名称</th>
                    <th>Float</th>
                    <th>买入价</th>
                    <th>卖出价</th>
                    <th>毛利润</th>
                    <th>净利润</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="trade in trades" :key="trade.id">
                    <td>{{ trade.name }}</td>
                    <td>{{ trade.float_value }}</td>
                    <td>{{ trade.purchase_price }}</td>
                    <td>{{ trade.sell_price }}</td>
                    <td>{{ trade.gross_income }}</td>
                    <td>{{ trade.net_income }}</td>
                    <td>
                        <form @submit.prevent="deleteTrade(trade)" @keydown.enter.prevent>
                            <button>删除</button>
                        </form>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { VueUiXy } from "vue-data-ui";
import { VueUiDonut } from 'vue-data-ui'
import "vue-data-ui/style.css";


export default {
    name: 'IndexPage',
    components: {
        VueUiXy,
        VueUiDonut
    },
    data() {
        return {
            username: '',
            trades: [],
            total_trades: 0,
            total_income: 0,
            total_purchase_price: 0,
            total_sell_price: 0,
            errorMsg: '',
            config1: {
                theme: '',
                responsive: false,
                responsiveProportionalSizing: true,
                customPalette: [],
                useCssAnimation: true,
                downsample: {
                    threshold: 500
                },
                chart: {
                    fontFamily: 'inherit',
                    backgroundColor: '#FFFFFFff',
                    color: '#1A1A1Aff',
                    height: 600,
                    width: 1000,
                    annotations: [
                        {
                            show: false,
                            yAxis: {
                                yTop: null,
                                yBottom: null,
                                label: {
                                    text: '',
                                    textAnchor: 'start',
                                    position: 'start',
                                    offsetX: 0,
                                    offsetY: 0,
                                    padding: {
                                        top: 5,
                                        right: 10,
                                        bottom: 5,
                                        left: 10
                                    },
                                    border: {
                                        stroke: '#FFFFFF',
                                        strokeWidth: 1,
                                        rx: 0,
                                        ry: 0
                                    },
                                    fontSize: 14,
                                    color: '#2D353C',
                                    backgroundColor: '#e1e5e8'
                                },
                                line: {
                                    stroke: '#2D353C',
                                    strokeWidth: 1,
                                    strokeDasharray: 0
                                },
                                area: {
                                    fill: '#e1e5e8',
                                    opacity: 30
                                }
                            }
                        }
                    ],
                    zoom: {
                        show: true,
                        color: '#CCCCCCff',
                        highlightColor: '#4A4A4A',
                        fontSize: 14,
                        useResetSlot: false,
                        startIndex: null,
                        endIndex: null,
                        enableRangeHandles: true,
                        enableSelectionDrag: true,
                        minimap: {
                            show: true,
                            smooth: false,
                            selectedColor: '#1F77B4',
                            selectedColorOpacity: 0.2,
                            lineColor: '#1A1A1A',
                            selectionRadius: 2,
                            indicatorColor: '#1A1A1A',
                            verticalHandles: false
                        }
                    },
                    padding: {
                        top: 36,
                        right: 24,
                        bottom: 48,
                        left: 48
                    },
                    highlighter: {
                        color: '#1A1A1Aff',
                        opacity: 5,
                        useLine: false,
                        lineDasharray: 2,
                        lineWidth: 1
                    },
                    highlightArea: {
                        show: false,
                        from: 0,
                        to: 0,
                        color: '#CCCCCCff',
                        opacity: 20,
                        caption: {
                            text: 'Caption',
                            fontSize: 20,
                            color: '#1A1A1Aff',
                            bold: false,
                            offsetY: 0,
                            width: 'auto',
                            padding: 3,
                            textAlign: 'center'
                        }
                    },
                    timeTag: {
                        show: false,
                        backgroundColor: '#e1e5e8ff',
                        color: '#1A1A1Aff',
                        fontSize: 12,
                        circleMarker: {
                            radius: 3,
                            color: '#1A1A1Aff'
                        }
                    },
                    grid: {
                        stroke: '#e1e5e8ff',
                        showVerticalLines: false,
                        showHorizontalLines: false,
                        position: 'middle',
                        frame: {
                            show: false,
                            stroke: '#E1E5E8ff',
                            strokeWidth: 2,
                            strokeLinecap: 'round',
                            strokeLinejoin: 'round',
                            strokeDasharray: 0
                        },
                        labels: {
                            show: true,
                            color: '#1A1A1Aff',
                            fontSize: 16,
                            axis: {
                                yLabel: '',
                                yLabelOffsetX: 0,
                                xLabel: '',
                                xLabelOffsetY: 14,
                                fontSize: 12
                            },
                            zeroLine: {
                                show: true
                            },
                            xAxis: {
                                showBaseline: true,
                                showCrosshairs: true,
                                crosshairsAlwaysAtZero: false,
                                crosshairSize: 6
                            },
                            yAxis: {
                                position: 'left',
                                showBaseline: true,
                                showCrosshairs: true,
                                crosshairSize: 6,
                                commonScaleSteps: 10,
                                useIndividualScale: false,
                                useNiceScale: true,
                                stacked: false,
                                gap: 12,
                                labelWidth: 40,
                                formatter: null,
                                scaleMin: null,
                                scaleMax: null,
                                groupColor: '#1A1A1A',
                                scaleLabelOffsetX: 0,
                                scaleValueOffsetX: 0
                            },
                            xAxisLabels: {
                                color: '#1A1A1Aff',
                                show: true,
                                values: [],
                                datetimeFormatter: {
                                    enable: false,
                                    locale: 'en',
                                    useUTC: false,
                                    januaryAsYear: false,
                                    options: {
                                        year: 'yyyy',
                                        month: 'MMM \'yy',
                                        day: 'dd MMM',
                                        hour: 'HH:mm',
                                        minute: 'HH:mm:ss',
                                        second: 'HH:mm:ss'
                                    }
                                },
                                fontSize: 18,
                                showOnlyFirstAndLast: false,
                                showOnlyAtModulo: false,
                                modulo: 12,
                                yOffset: 8,
                                rotation: 0
                            }
                        }
                    },
                    comments: {
                        show: true,
                        showInTooltip: true,
                        width: 200,
                        offsetX: 0,
                        offsetY: 0
                    },
                    labels: {
                        fontSize: 16,
                        prefix: '',
                        suffix: ''
                    },
                    legend: {
                        color: '#1A1A1Aff',
                        show: true,
                        fontSize: 16
                    },
                    title: {
                        text: '交易盈利统计',
                        color: '#1A1A1Aff',
                        fontSize: 20,
                        bold: true,
                        textAlign: 'center',
                        paddingLeft: 0,
                        paddingRight: 0,
                        subtitle: {
                            color: '#CCCCCCff',
                            text: '',
                            fontSize: 16,
                            bold: false
                        },
                        show: true
                    },
                    tooltip: {
                        show: true,
                        color: '#1A1A1Aff',
                        backgroundColor: '#FFFFFFff',
                        fontSize: 14,
                        customFormat: null,
                        borderRadius: 4,
                        borderColor: '#e1e5e8',
                        borderWidth: 1,
                        backgroundOpacity: 30,
                        position: 'center',
                        offsetY: 24,
                        showTimeLabel: true,
                        showValue: true,
                        showPercentage: false,
                        roundingValue: 0,
                        roundingPercentage: 0
                    },
                    userOptions: {
                        show: true,
                        showOnChartHover: false,
                        keepStateOnChartLeave: true,
                        position: 'right',
                        buttons: {
                            tooltip: true,
                            pdf: true,
                            csv: true,
                            img: true,
                            table: true,
                            labels: true,
                            fullscreen: true,
                            sort: false,
                            stack: true,
                            animation: false,
                            annotator: true
                        },
                        callbacks: {
                            animation: null,
                            annotator: null,
                            csv: null,
                            fullscreen: null,
                            img: null,
                            labels: null,
                            pdf: null,
                            sort: null,
                            stack: null,
                            table: null,
                            tooltip: null
                        },
                        buttonTitles: {
                            open: 'Open options',
                            close: 'Close options',
                            tooltip: 'Toggle tooltip',
                            pdf: 'Download PDF',
                            csv: 'Download CSV',
                            img: 'Download PNG',
                            table: 'Toggle table',
                            labels: 'Toggle labels',
                            fullscreen: 'Toggle fullscreen',
                            stack: 'Toggle stack mode',
                            annotator: 'Toggle annotator'
                        },
                        print: {
                            allowTaint: false,
                            backgroundColor: '#FFFFFFff',
                            useCORS: false,
                            onclone: null,
                            scale: 2,
                            logging: false
                        }
                    }
                },
                bar: {
                    borderRadius: 2,
                    useGradient: true,
                    periodGap: 0.1,
                    border: {
                        useSerieColor: false,
                        strokeWidth: 1,
                        stroke: '#FFFFFFff'
                    },
                    labels: {
                        show: true,
                        offsetY: -8,
                        rounding: 0,
                        color: '#1A1A1Aff',
                        formatter: null
                    },
                    serieName: {
                        show: false,
                        offsetY: -6,
                        useAbbreviation: true,
                        abbreviationSize: 3,
                        useSerieColor: true,
                        color: '#1A1A1Aff',
                        bold: false
                    }
                },
                line: {
                    radius: 6,
                    useGradient: false,
                    strokeWidth: 2,
                    cutNullValues: false,
                    dot: {
                        hideAboveMaxSerieLength: 62,
                        useSerieColor: false,
                        fill: '#FFFFFF',
                        strokeWidth: 2
                    },
                    labels: {
                        show: true,
                        offsetY: -16,
                        rounding: 0,
                        color: '#1A1A1Aff',
                        formatter: null
                    },
                    area: {
                        useGradient: true,
                        opacity: 20
                    },
                    tag: {
                        followValue: true,
                        formatter: null,
                        fontSize: 14
                    }
                },
                plot: {
                    radius: 6,
                    useGradient: true,
                    dot: {
                        useSerieColor: true,
                        fill: '#FFFFFF',
                        strokeWidth: 0.5
                    },
                    labels: {
                        show: true,
                        offsetY: -8,
                        rounding: 0,
                        color: '#1A1A1Aff',
                        formatter: null
                    },
                    tag: {
                        followValue: true,
                        formatter: null,
                        fontSize: 14
                    }
                },
                table: {
                    responsiveBreakpoint: 400,
                    rounding: 0,
                    sparkline: true,
                    showSum: true,
                    columnNames: {
                        period: 'Period',
                        total: 'Total'
                    },
                    th: {
                        backgroundColor: '#FAFAFAff',
                        color: '#1A1A1Aff',
                        outline: ''
                    },
                    td: {
                        backgroundColor: '#FAFAFAff',
                        color: '#1A1A1Aff',
                        outline: ''
                    }
                },
                showTable: false
            },
            dataset1: [
                {
                    name: 'total income',
                    series: [
                        1,
                        9,
                        7,
                        2,
                        199,
                        16,
                        17,
                        30,
                        16,
                        23
                    ],
                    color: '#1f77b4',
                    type: 'line',
                    shape: 'circle',
                    useArea: false,
                    useProgression: false,
                    dataLabels: true,
                    smooth: true,
                    dashed: false,
                    useTag: 'none',
                }
            ],
            config2: {
                type: 'classic',
                responsive: false,
                theme: '',
                customPalette: [],
                useCssAnimation: true,
                serieToggleAnimation: {
                    show: true,
                    durationMs: 500
                },
                startAnimation: {
                    show: true,
                    durationMs: 1000,
                    staggerMs: 50
                },
                useBlurOnHover: true,
                userOptions: {
                    show: true,
                    showOnChartHover: false,
                    keepStateOnChartLeave: true,
                    position: 'right',
                    buttons: {
                        tooltip: true,
                        pdf: true,
                        csv: true,
                        img: true,
                        table: true,
                        labels: true,
                        fullscreen: true,
                        sort: false,
                        stack: false,
                        animation: false,
                        annotator: true
                    },
                    callbacks: {
                        animation: null,
                        annotator: null,
                        csv: null,
                        fullscreen: null,
                        img: null,
                        labels: null,
                        pdf: null,
                        sort: null,
                        stack: null,
                        table: null,
                        tooltip: null
                    },
                    buttonTitles: {
                        open: 'Open options',
                        close: 'Close options',
                        tooltip: 'Toggle tooltip',
                        pdf: 'Download PDF',
                        csv: 'Download CSV',
                        img: 'Download PNG',
                        table: 'Toggle table',
                        labels: 'Toggle labels',
                        fullscreen: 'Toggle fullscreen',
                        annotator: 'Toggle annotator'
                    },
                    print: {
                        allowTaint: false,
                        backgroundColor: '#FFFFFFff',
                        useCORS: false,
                        onclone: null,
                        scale: 2,
                        logging: false
                    }
                },
                translations: {
                    total: 'Total',
                    average: 'Average'
                },
                table: {
                    show: false,
                    responsiveBreakpoint: 400,
                    th: {
                        backgroundColor: '#FFFFFFff',
                        color: '#1A1A1Aff',
                        outline: 'none'
                    },
                    td: {
                        backgroundColor: '#FFFFFFff',
                        color: '#1A1A1Aff',
                        outline: 'none',
                        roundingValue: 0,
                        roundingPercentage: 0
                    },
                    columnNames: {
                        series: 'type',
                        value: 'Value',
                        percentage: 'Percentage'
                    }
                },
                style: {
                    fontFamily: 'inherit',
                    chart: {
                        useGradient: true,
                        gradientIntensity: 40,
                        backgroundColor: '#FFFFFFff',
                        color: '#1A1A1Aff',
                        padding: {
                            top: 0,
                            right: 0,
                            bottom: 0,
                            left: 0
                        },
                        width: 512,
                        height: 360,
                        layout: {
                            curvedMarkers: true,
                            labels: {
                                dataLabels: {
                                    show: true,
                                    useLabelSlots: false,
                                    hideUnderValue: 3,
                                    prefix: '',
                                    suffix: ''
                                },
                                value: {
                                    rounding: 0,
                                    show: true,
                                    formatter: null
                                },
                                percentage: {
                                    color: '#1A1A1Aff',
                                    bold: true,
                                    fontSize: 18,
                                    rounding: 0,
                                    formatter: null
                                },
                                name: {
                                    color: '#1A1A1Aff',
                                    bold: false,
                                    fontSize: 14
                                },
                                hollow: {
                                    show: true,
                                    total: {
                                        show: true,
                                        bold: false,
                                        fontSize: 18,
                                        color: '#AAAAAAff',
                                        text: 'Total',
                                        offsetY: 0,
                                        value: {
                                            color: '#1A1A1Aff',
                                            fontSize: 18,
                                            bold: true,
                                            suffix: '',
                                            prefix: '',
                                            offsetY: 0,
                                            rounding: 0,
                                            formatter: null
                                        }
                                    },
                                    average: {
                                        show: true,
                                        bold: false,
                                        fontSize: 18,
                                        color: '#AAAAAAff',
                                        text: 'Average',
                                        offsetY: 0,
                                        value: {
                                            color: '#1A1A1Aff',
                                            fontSize: 18,
                                            bold: true,
                                            suffix: '',
                                            prefix: '',
                                            offsetY: 0,
                                            rounding: 0,
                                            formatter: null
                                        }
                                    }
                                }
                            },
                            donut: {
                                strokeWidth: 64,
                                borderWidth: 1,
                                useShadow: false,
                                shadowColor: '#1A1A1A',
                                emptyFill: '#E1E5E8'
                            }
                        },
                        comments: {
                            show: true,
                            showInTooltip: true,
                            width: 100,
                            offsetY: 0,
                            offsetX: 0
                        },
                        legend: {
                            show: true,
                            bold: false,
                            backgroundColor: '#FFFFFFff',
                            color: '#1A1A1Aff',
                            fontSize: 16,
                            roundingValue: 0,
                            roundingPercentage: 0
                        },
                        tooltip: {
                            show: true,
                            color: '#1A1A1Aff',
                            backgroundColor: '#FFFFFFff',
                            fontSize: 14,
                            customFormat: null,
                            borderRadius: 4,
                            borderColor: '#e1e5e8',
                            borderWidth: 1,
                            backgroundOpacity: 30,
                            position: 'center',
                            offsetY: 24,
                            showValue: true,
                            showPercentage: true,
                            roundingValue: 0,
                            roundingPercentage: 0
                        },
                        title: {
                            text: '交易类型分布',
                            color: '#1A1A1Aff',
                            fontSize: 20,
                            bold: true,
                            textAlign: 'center',
                            paddingLeft: 0,
                            paddingRight: 0,
                            subtitle: {
                                color: '#A1A1A1ff',
                                text: '',
                                fontSize: 16,
                                bold: false
                            }
                        }
                    }
                }
            },

            dataset2: [
                {
                    name: 'knife',
                    values: [
                        100
                    ],
                    color: '#1f77b4'
                },
                {
                    name: 'glove',
                    values: [
                        50
                    ],
                    color: '#aec7e8'
                },
                {
                    name: 'gun',
                    values: [
                        25
                    ],
                    color: '#ff7f0e'
                },
                {
                    name: 'other',
                    values: [
                        22
                    ],
                    color: '#42d392'
                }
            ]
        }
    },
    async mounted() {
        try {
            const me = await axios.get('/api/me')
            this.username = me.data.username
            const res = await axios.get('/api/')
            this.trades = res.data.trades
            this.total_trades = res.data.total_trades
            this.total_income = res.data.total_income
            this.total_purchase_price = res.data.total_purchase_price
            this.total_sell_price = res.data.total_sell_price
            this.total_income_list = res.data.total_income_list
            this.total_trade_type = res.data.total_trade_type
            this.dataset1 = [
                {
                    name: 'total income',
                    series: this.total_income_list,
                    color: '#1f77b4',
                    type: 'line',
                    shape: 'circle',
                    useArea: false,
                    useProgression: false,
                    dataLabels: false,
                    smooth: true,
                    dashed: false,
                    useTag: 'none'
                }
            ]
            const convertedSeries = this.total_income_list.map((y, i) => ({
                x: i + 1,
                y: y
            }))

            this.config1.chart.grid.labels.xAxisLabels.values = convertedSeries.map((point, i) =>
                i % 20 === 0 ? point.x : ''
            )

            this.dataset2 = [
                {
                    name: 'knife',
                    values: [
                        this.total_trade_type[0]
                    ],
                    color: '#1f77b4'
                },
                {
                    name: 'glove',
                    values: [
                        this.total_trade_type[1]
                    ],
                    color: '#aec7e8'
                },
                {
                    name: 'gun',
                    values: [
                        this.total_trade_type[2]
                    ],
                    color: '#ff7f0e'
                },
                {
                    name: 'other',
                    values: [
                        this.total_trade_type[3]
                    ],
                    color: '#42d392'
                }
            ]
        } catch (error) {
            if (error.response && error.response.status === 401) {
                this.$router.push('/login')
            } else {
                this.errorMsg = '加载交易数据失败'
            }
        }
    },
    methods: {
        async logout() {
            try {
                await axios.post('http://localhost:10000/logout', {}, { withCredentials: true })
                this.$router.push('/login')
            } catch (err) {
                alert('登出失败')
            }
        },
        async deleteTrade(trade) {
            if (!confirm('确定删除这条交易吗？')) return
            try {
                await axios.post('http://localhost:10000/delete_trade', {
                    name: trade.name,
                    purchase_price: trade.purchase_price,
                    sell_price: trade.sell_price
                }, {
                    withCredentials: true  // 🔥 必须有
                })
                // 删除后刷新页面或移除该项
                this.trades = this.trades.filter(t =>
                    !(t.name === trade.name &&
                        t.purchase_price === trade.purchase_price &&
                        t.sell_price === trade.sell_price)
                )

            } catch (err) {
                alert('删除失败')
            }
        }
    }
}
</script>

<style scoped>
* {
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f2f5;
    color: #333;
    margin: 0;
    padding: 2rem;
    max-width: 1000px;
    margin-left: auto;
    margin-right: auto;
}

h1,
h2 {
    text-align: center;
}

nav {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

nav a,
nav router-link {
    display: inline-block;
    background-color: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.2s;
}

nav a:hover {
    background-color: #0056b3;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    table-layout: fixed;
    margin-bottom: 2rem;
}

th,
td {
    padding: 0.75rem;
    border: 1px solid #ddd;
    text-align: left;
}

th {
    background-color: #f5f5f5;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

button {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s;
}

button:hover {
    background-color: #c82333;
}

.container {
    max-width: 1000px;
    margin-left: auto;
    margin-right: auto;
    padding: 1rem;
}

.error {
    color: red;
    text-align: center;
    margin-top: 1rem;
}

@media (max-width: 768px) {

    table,
    thead,
    tbody,
    th,
    td,
    tr {
        display: block;
    }

    thead {
        display: none;
    }

    tr {
        margin-bottom: 1rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        overflow: hidden;
    }

    td {
        padding: 0.5rem;
        display: flex;
        justify-content: space-between;
    }

    td::before {
        content: attr(data-label);
        font-weight: bold;
        flex-basis: 50%;
    }
}
</style>