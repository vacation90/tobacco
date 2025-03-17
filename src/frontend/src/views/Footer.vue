<template>
  <va-config
      :components="{
        VaButton: { preset: 'primary', borderColor: 'primary', flat: true },
      }"
  >
  <div class="footer">
    <div class="row justify-space-evenly">
      <va-button class="mr-3 mb-2">
        <Icon icon="bxs:component" class="pr-4"/>
        About  This Page
      </va-button>
      <va-button class="mr-3 mb-2">
        <Icon icon="circle-flags:jp" class="pr-4"/>
        About  MSP17
      </va-button>
      <va-button class="mr-3 mb-2" @click="externalLink()">
        <Icon icon="material-symbols:admin-panel-settings-outline" class="pr-4" />
        Admin
      </va-button>
    </div>
    <div class="footer__socials">
        <va-button class="footer__social__items" >
        <Icon icon="brandico:twitter" />
        </va-button>
      <va-button class="footer__social__items" >
        <Icon icon="brandico:github" />
      </va-button>
      <va-button class="footer__social__items" >
        <Icon icon="fa-brands:discord" />
      </va-button>
      <va-button class="footer__social__items" >
        <Icon icon="brandico:instagram" />
      </va-button>
    </div>
    <div class="footer__subtitle">
      Open source, free to use. Development inquiries:
      <a href="https://github.com/project17msp">
        https://github.com/project17msp
      </a>
    </div>
  </div>
  </va-config>
</template>

<script>
import { defineComponent } from 'vue';
export default defineComponent({
  components: {
  },
  methods: {
    externalLink() {
      const url = 'http://localhost:8000/docs#/default'
      window.open(url, '_blank')
    }
  },
});

</script>

<style>
.footer__socials {
    box-sizing: border-box;
    word-wrap: break-word;
    margin-left: 15px;
    margin-right: 15px;
    width: calc(100% - 30px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
.footer__social__items
{
    font-weight: 600;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    font-size: 1rem;
}
</style>
