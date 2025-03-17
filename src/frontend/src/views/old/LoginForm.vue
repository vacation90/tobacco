<template>
  <div class="loginForm">
    <va-form
      tag="form"
      autofocus
      @submit.prevent="OpenEditWindow()"
      style="width: 300px;"
    >
      <va-input
        label="Username"
        v-model="username"
        :rules="[(value) => (value && value.length > 0) || 'Field is required']"
      />

      <va-input
        class="mt-3"
        type="password"
        label="Password"
        v-model="password"
        :rules="[(value) => (value && value.length > 0) || 'Field is required']"
      />
      <va-button type="submit" class="mt-3">
        Login
      </va-button>
    </va-form>
  </div>
</template>


<script>
import axios from "axios";
import { useStoreAuth } from '../stores/auth';
const baseURL = 'http://localhost:8000'

export default {
  data () {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async OpenEditWindow() {
      
      const storeAuth = useStoreAuth();
      const filterParam = new URLSearchParams();
      filterParam.append("username",this.username);
      filterParam.append("password",this.password);

      await axios.post(baseURL + "/auth/token", filterParam)
        .then(function (response) {
          // 送信成功時の処理
          //Storeに認証情報を格納
          storeAuth.name = filterParam.get("username");
          storeAuth.token = response.data.access_token;
          //TODO: 認証切れた時の対応
          storeAuth.isAuth = true;
        })
        .catch(function (error) {
          // 送信失敗時の処理
          alert('-- login error --')
          console.log(error);
        });
    },
  },
}
</script>