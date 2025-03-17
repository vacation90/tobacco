<template>
<va-form @submit.prevent="handleSubmit">
  <div class="mb-3">
    <va-input type="text" required placeholder="display name" v-model="displayName" :rules="[value => (value && value.length > 0) || 'Field is required']" />
  </div>

  <div class="mb-3">
    <va-input type="email" required placeholder="email" v-model="email" :rules="[value => (value && value.length > 0) || 'Field is required']" />
  </div>

  <div class="mb-3">
    <va-input type="password" required placeholder="password" v-model="password" :rules="[value => (value && value.length > 0) || 'Field is required']" />
  </div>

  <va-checkbox v-model="value" label="Show Password" />

  <div class="error">{{ error }}</div>
  <va-button>Sign up</va-button>
</va-form>
</template>

<script>
import {
  ref
} from 'vue'
import useSignup from '../../../components/useSignup'

export default {
  data() {
    return {
      value: false,
    }
  },
  setup(props, context) { //Welcome.vueにわたすemitを使えるようにするためcontextを引数に設定する
    const {
      error,
      signup
    } = useSignup()

    // refs
    const displayName = ref('')
    const email = ref('')
    const password = ref('')

    const handleSubmit = async () => {
      // console.log(displayName.value, email.value, password.value)
      await signup(email.value, password.value, displayName.value)
      if (!error.value) {
        // console.log('user signed up')
        context.emit('signup') //Welcome.vueにわたす
      }
    }

    return {
      displayName,
      email,
      password,
      handleSubmit,
      error
    }
  }
}
</script>
