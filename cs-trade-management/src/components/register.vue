<template>
  <div class="container">
    <h1>CS 交易管理系统</h1>
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <label for="username">用户名：</label>
      <input v-model="username" type="text" id="username" required />

      <label for="password">密码：</label>
      <input v-model="password" type="password" id="password" required />

      <input type="submit" value="注册" />
    </form>

    <div class="login-link">
      <p>已有账号？<router-link to="/login">点击登录</router-link></p>
    </div>

    <p v-if="message" :class="{ success: success, error: !success }">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import '../style.css'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      message: '',
      success: false
    }
  },
  methods: {
    async handleRegister() {
      try {
        const res = await axios.post('/api/register', {
          username: this.username,
          password: this.password
        })
        this.success = true
        this.message = res.data.message
      } catch (err) {
        this.success = false
        if (err.response) {
          this.message = err.response.data.message
        } else {
          this.message = '注册请求失败'
        }
      }
    }
  }
}
</script>