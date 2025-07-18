<template>
  <div class="import-page">
    <h2>导入交易记录</h2>

    <form @submit.prevent="submitFile">
      <input type="file" @change="handleFileChange" accept=".csv" required /><br /><br />
      <input type="submit" value="导入" :disabled="loading" />
    </form>

    <p v-if="message" :class="{ error: isError }">{{ message }}</p>
    <a href="/">返回首页</a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
      message: '',
      isError: false,
      loading: false
    }
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0]
    },
    async submitFile() {
      if (!this.file) {
        this.message = '请先选择文件'
        this.isError = true
        return
      }

      const formData = new FormData()
      formData.append('file', this.file)

      this.loading = true
      this.message = ''

      try {
        const res = await fetch('/api/import_csv', {
          method: 'POST',
          body: formData,
          credentials: 'include'
        })

        if (res.redirected) {
          // 如果 Flask 返回 redirect，跳转主页
          window.location.href = res.url
        } else {
          const text = await res.text()
          if (res.ok) {
            this.message = text
            this.isError = false
          } else {
            this.message = text || '导入失败'
            this.isError = true
          }
        }
      } catch (err) {
        this.message = '网络错误：' + err.message
        this.isError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.import-page {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f0f2f5;
  color: #333;
  padding: 2rem;
  max-width: 600px;
  margin: auto;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
}

form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

input[type="file"] {
  padding: 0.5rem;
  margin-bottom: 1rem;
}

input[type="submit"] {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

input[type="submit"]:hover {
  background-color: #0056b3;
}

a {
  display: inline-block;
  margin-top: 1rem;
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

p {
  margin-top: 1rem;
  text-align: center;
}

.error {
  color: red;
}
</style>