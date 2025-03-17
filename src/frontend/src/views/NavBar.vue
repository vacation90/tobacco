<template>
  <va-navbar
    color="primary"
    id="nav">
    <template #left>
      <va-navbar-item>
        <va-button @click="stateManager.menuAction">
          <va-icon
            size="24px"
            :name="stateManager.isMenuToggle ? 'menu' : 'menu_open'"
          />
        </va-button>
        <img src="../assets/logo4.png"
          alt="Logo"
          style="max-width:25%;"
          @click="home()"/>
      </va-navbar-item>
    </template>
  </va-navbar>
</template>

<script>
import { useStateManager } from "../stores/StateManager";
export default{
    name: "NavBar",
    setup() {
        const stateManager = useStateManager();
        return { stateManager };
    },
    data() {
        return {
          value: false,
        };
    },
    methods: {
        home() {
            this.$router.go({ path: this.$router.currentRoute.path, force: true });
        }
    },
}
</script>
