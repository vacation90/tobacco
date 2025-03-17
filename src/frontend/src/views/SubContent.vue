<template>
  <!-- Modal -->
  <va-modal
    v-model="show"
    hide-default-actions
    overlay-opacity="0.2"
  >
    <template #header>
      <h2>{{ stateManager.modalItem.name }}</h2>
    </template>
    <va-divider />
    <div class="layout gutter--xl row">
      <div class="flex md6">
        <va-image
          :src="stateManager.modalItem.image"
          style="height: 200px; width: 200px;"
        />
      </div>
      <div class="flex md6">
        <div v-for="column in dbColumns" :key="column">
          <div v-if="column.data_type!='url' && column.data_type!='image'">{{ column.name }} : {{ stateManager.modalItem[column.code] }} {{ column.unit }}
          </div>
        </div>
      </div>
    </div>
    <va-divider />

  </va-modal>
</template>

<script>
import { defineComponent } from 'vue';
import { useStateManager } from "../stores/StateManager";
export default defineComponent({
  name: "SubContent",
  props: {
    dbColumns: Object,
  },
  setup() {
        const stateManager = useStateManager();
        return { stateManager };
    },
  data () {
    return {
    }
  },
});
</script>
