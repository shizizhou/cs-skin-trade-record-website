<template>
  <div class="container">
    <div>
      <h1>亏损交易列表</h1>
      <div class="center">
        <router-link to="/">返回主页</router-link>
      </div>
      <h2>总亏损</h2>
      <p class="center">{{ total_loss }}</p>

      <table>
        <thead>
          <tr>
            <th>名称</th>
            <th>Float</th>
            <th>买入价</th>
            <th>卖出价</th>
            <th>毛利润</th>
            <th>净利润</th>
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
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LossPage',
  data() {
    return {
      trades: [],
      total_income: 0
    }
  },
  async mounted() {
    try {
      const res = await axios.get('/api/loss', {
        withCredentials: true
      })
      console.log(res.data)
      this.trades = res.data.trades
      this.total_loss = res.data.total_loss
    } catch (err) {
      if (err.response && err.response.status === 401) {
        this.$router.push('/login')
      } else {
        alert('加载亏损交易失败')
      }
    }
  }
}
</script>

<style scoped>
.center {
  text-align: center;
}
table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  margin-top: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
th, td {
  padding: 0.75rem;
  border: 1px solid #ddd;
}
th {
  background-color: #f5f5f5;
}
.container {
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  padding: 1rem;
}
tr:nth-child(even) {
  background-color: #fafafa;
}
</style>