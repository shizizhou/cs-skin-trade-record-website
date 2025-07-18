<template>
  <div>
    <h1>添加交易记录</h1>

    <form @submit.prevent="submitForm">
      <div>
        <label for="name">名称：</label>
        <input v-model="form.name" type="text" id="name" required />
      </div>

      <div>
        <label for="float">Float：</label>
        <input v-model="form.float" type="text" id="float" required />
      </div>

      <div>
        <label for="purchase_price">购买价：</label>
        <input
          v-model.number="form.purchase_price"
          type="number"
          step="0.01"
          id="purchase_price"
          required
        />
      </div>

      <div>
        <label for="sell_price">出售价：</label>
        <input
          v-model.number="form.sell_price"
          type="number"
          step="0.01"
          id="sell_price"
          required
        />
      </div>

      <div class="radio-group">
        <p>请选择交易平台：</p>

        <label><input type="radio" value="buff" v-model="form.trade_type" /> Buff</label>
        <label><input type="radio" value="youyou" v-model="form.trade_type" /> YouYou</label>
        <label><input type="radio" value="cs_float" v-model="form.trade_type" /> CS Float</label>
      </div>

      <button type="submit">提交</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>

    <router-link to="/">返回主页</router-link>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddTrade',
  data() {
    return {
      form: {
        name: '',
        float: '',
        purchase_price: null,
        sell_price: null,
        trade_type: ''
      },
      errorMessage: ''
    }
  },
  methods: {
    async submitForm() {
      this.errorMessage = ''
      try {
        await axios.post('/api/add_trade', this.form, { withCredentials: true })
        this.$router.push('/')
      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          this.errorMessage = error.response.data.message
        } else {
          this.errorMessage = '提交失败，请稍后再试'
        }
      }
    }
  }
}
</script>

<style scoped>
body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f0f2f5;
  color: #333;
  padding: 2rem;
  max-width: 600px;
  margin: auto;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="number"] {
  padding: 0.6rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.radio-group {
  margin-top: 1rem;
}

button {
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

a {
  margin-top: 1.5rem;
  text-align: center;
  text-decoration: none;
  color: #007bff;
  display: block;
}

a:hover {
  text-decoration: underline;
}

.error {
  color: red;
  font-weight: bold;
}
</style>