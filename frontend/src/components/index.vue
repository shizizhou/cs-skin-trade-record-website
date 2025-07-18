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

export default {
    name: 'IndexPage',
    data() {
        return {
            username: '',
            trades: [],
            total_trades: 0,
            total_income: 0,
            total_purchase_price: 0,
            total_sell_price: 0,
            errorMsg: ''
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