import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { createVuestic, createIconsConfig } from 'vuestic-ui'
import 'vuestic-ui/dist/vuestic-ui.css'
import 'material-design-icons-iconfont/dist/material-design-icons.min.css'
import { Icon } from '@iconify/vue'

const app = createApp(App).component('Icon', Icon )
app.use(createPinia())
app.use(router)
app.use(createVuestic({
  config: {
    icons: createIconsConfig({ 
      aliases: [
        {
          name: "bell",
          color: "#FFD43A",
          to: "fa4-bell",
        },
        {
          name: "ru",
          to: "flag-icon-ru small",
        },
      ],
      fonts: [
        {
          name: "fa4-{iconName}",
          resolve: ({ iconName }) => ({ class: `fa fa-${iconName}` }),
        },
        {
          name: "flag-icon-{countryCode} {flagSize}",
          resolve: ({ countryCode, flagSize }) => ({
            class: `flag-icon flag-icon-${countryCode} flag-icon-${flagSize}`,
          }),
        },
      ],
    }),
    colors: {
      variables: {
        // Default colors
        secondary: "#002c85",
        success: "#40e583",
        info: "#2c82e0",
        danger: "#e34b4a",
        warning: "#ffc200",
        gray: "#babfc2",
        dark: "#34495e",

        // Custom colors
        yourCustomColor: "#d0f55d",
      },
    },
  },
})
)
app.mount('#app')
