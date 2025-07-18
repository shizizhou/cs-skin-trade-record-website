<template>
  <div class="container">
    <h1>搜索交易记录</h1>

    <div class="center-button">
      <a href="/" class="button">返回主页</a>
    </div>

    <form @submit.prevent="search" class="search-form">
      <input
        v-model="q"
        @keyup.enter="search"
        type="text"
        placeholder="输入名称关键词..."
      />
      <button type="submit">搜索</button>
    </form>

    <div v-if="trades.length">
      <p>找到 {{ count }} 条与 “{{ q }}” 匹配的交易记录：</p>
      <table>
        <thead>
          <tr>
            <th>名称</th>
            <th>Float</th>
            <th>购买价</th>
            <th>出售价</th>
            <th>毛利润</th>
            <th>净利润</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(trade, index) in trades" :key="index">
            <td>{{ trade.name }}</td>
            <td>{{ trade.float || '-' }}</td>
            <td>{{ trade.purchase_price || '-' }}</td>
            <td>{{ trade.sell_price || '-' }}</td>
            <td>{{ trade.gross_income || '-' }}</td>
            <td>{{ trade.net_income || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      q: '',
      count: 0,
      trades: []
    }
  },
  methods: {
    async search() {
      try {
        const res = await axios.get('/api/search', {
          params: { q: this.q },
          withCredentials: true
        })
        this.trades = res.data.trades || []
        this.count = res.data.count || 0
      } catch (err) {
        console.error('搜索失败', err)
      }
    }
  }
}
</script>

<style scoped>


h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.center-button {
  text-align: center;
  margin-bottom: 1.5rem;
}

.button {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.button:hover {
  background-color: #0056b3;
}

.search-form {
  text-align: center;
  margin-bottom: 2rem;
}

input[type="text"] {
  padding: 0.6rem;
  width: 300px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.6rem 1rem;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  margin-left: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.container {
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  padding: 1rem;
}
button:hover {
  background-color: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  margin-top: 1rem;
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

.no-result {
  text-align: center;
  color: #888;
  margin-top: 2rem;
}
</style>