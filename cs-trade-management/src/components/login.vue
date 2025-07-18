<template>
  <div class="container">
    <h1>CS 交易管理系统</h1>
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <label for="username">用户名：</label>
      <input v-model="username" type="text" id="username" required />

      <label for="password">密码：</label>
      <input v-model="password" type="password" id="password" required />

      <input type="submit" value="登录" />
    </form>

    <div class="login-link">
      <p>没有账号？<router-link to="/register">点击注册</router-link></p>
    </div>

    <p v-if="errorMsg" :class="{ success: false, error: true }">{{ errorMsg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import '../style.css'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errorMsg: ''
    }
  },
  methods: {
    async handleLogin() {
      this.errorMsg = ''
      try {
        const res = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        })
        if (res.status === 200) {
          this.$router.push('/')
        }
      } catch (error) {
        this.errorMsg = '用户名或密码错误'
      }
    }
  }
}
</script>