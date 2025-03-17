<template>
  <div class="row">
    <template v-for="(item, itemIndex) in dbItems" :key="item.to">
      <div class="flex my-3 px-3" 
        v-show="(stateManager.pageIndex-1) <= itemIndex && itemIndex < stateManager.pageIndex+stateManager.pageSize-1">
        <va-card 
          stripe
          stripe-color="info"
          style="width: 250px;"
          @click="showModal(item)"
        >
          <!-- Image -->
          <va-image
              class="justify-center"
              :src="item.image"
              style="height: 200px;"
          />
          <!-- Title -->
          <va-card-title style="height: 50px">
            {{item.name}}
          </va-card-title>
          <!-- Disc -->
          <va-card-content class="cardContent">
            {{item.discription}}
          </va-card-content>
        </va-card>
      </div>
    </template>
    <SubContent v-model="show" :dbColumns="this.dbColumns" :dbItems="dbItems"/>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useStateManager } from "../stores/StateManager";
import SubContent from './SubContent.vue'
export default defineComponent({
  name: "TileView",
  props: {
    dbColumns: Object,
    dbItems: Object,
  },
  components: {
    SubContent
  },
  setup() {
        const stateManager = useStateManager();
        return { stateManager };
    },
  data(){
    return{
      show: false,
      modalitem: null,
    }
  },
  methods: {
    showModal(item){
      this.show = !this.show
      this.stateManager.modalItem = item
    }
  },
});
</script>