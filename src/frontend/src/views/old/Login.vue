
<template>
<div class="welcome container">
  <!-- header -->
  <h1>
    <va-icon class="ml-3" name="home" /> Welcome</h1>
  <div class="flex xs12 pa-3">
    <!-- Loginform -->
    <va-card stripe stripe-color="success">
      <div v-if="showLogin">
        <va-card-title>
          Login
        </va-card-title>
        <va-card-content>
          <LoginForm @login="enterChat" />
          <div class="va-separator"></div>
          <p> No accout yet? </p>
          <va-config :components="{ VaIcon: { color: '#ffffff' } }">
            <va-button @click="showLogin = false" size="small" :rounded="false" class="mr-2" space-between-items>
              <va-icon size="small" name="gavel" />
              Signup instead
              <va-icon size="small" name="shield" />
            </va-button>
          </va-config>
        </va-card-content>
      </div>

      <!-- SignUform -->
      <div v-else>
        <va-card-title>
          Signup
        </va-card-title>
        <SignupForm @signup="enterChat" />
        <div class="va-separator"></div>
        <p> Already refisterd? </p>
        <va-config :components="{ VaIcon: { color: '#ffffff' } }">
          <va-button @click="showLogin = true" size="small" :rounded="false" class="mr-2" space-between-items>
            <va-icon size="small" name="gavel" />
            Login instead
            <va-icon size="small" name="shield" />
          </va-button>
        </va-config>
      </div>
    </va-card>
  </div>
</div>
</template>


<script>
import SignupForm from './SignupForm.vue'
import LoginForm from './old/LoginForm.vue'
import {
  ref
} from 'vue'
import {
  useRouter
} from 'vue-router'

export default {
  components: {
    SignupForm,
    LoginForm
  },
  setup() {
    const showLogin = ref(true)
    const router = useRouter()
    const enterChat = () => {
      router.push({
        name: 'Main'
      })
    }
    return {
      showLogin,
      enterChat
    }
  }
}
</script>
