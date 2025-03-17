<template>
  <div class="api">
    <va-form
    style="width: 300px;"
    tag="form"
    @submit.prevent="getApi"
    >

      <va-input
        label="id"
        v-model="id"
      />

      <va-input
        class="mt-3"
        label="name"
        v-model="name"
      />

      <va-input
        class="mt-3"
        label="disc"
        v-model="disc"
      />

      <va-input
        class="mt-3"
        label="price"
        v-model="price"
      />

      <va-input
        class="mt-3"
        label="amount"
        v-model="amount"
      />

      <va-input
        class="mt-3"
        label="nicotine"
        v-model="nicotine"
      />

      <va-input
        class="mt-3"
        label="tar"
        v-model="tar"
      />

      <va-button type="submit" class="mt-3">
        Submit
      </va-button>
    </va-form>
  </div>
</template>

<script>
import { defineComponent, reactive } from 'vue';
import axios from 'axios';
import { useStoreAuth } from '../stores/auth';

const baseURL = 'http://localhost:8000/items/update';

export default defineComponent({
  name: 'Api',
  setup() {
    const state = reactive({
      id: 0,
      name: '',
      disc: null,
      price: null,
      amount: null,
      nicotine: null,
      tar: null,
    });

    const getApi = () => {// eslint-disable-line no-unused-vars

      //認証情報
      const storeAuth = useStoreAuth();
      const config = {
        headers:{
          accept: 'application/json',
          Authorization: 'Bearer ' + storeAuth.token,
          'Content-Type': 'application/json',
        }
      };
      const data =[{
        "id": "3",
        "name": "ピアニッシモ",
        "discription": "楽しい彩りを味わおう",
        "price": "80",
        "amount": "1",
        "nicotine": "5",
        "tar": "5",
      }]

      axios.post(baseURL, data, config)
        .then(function (response) {
          // 送信成功時の処理
          console.log(response);
        })
        .catch(function (error) {
          if (error.response) {
            // 要求がなされたとサーバがステータスコードで応答した
            // 2XXの範囲外
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            // 要求がなされたが、応答が受信されなかった
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            console.log(error.request);
          } else {
            // トリガーしたリクエストの設定に何かしらのエラーがある
            console.log('Error', error.message);
          }
          console.log(error.config);
        });
    };
    return{ state,getApi };
  },
});
</script>
