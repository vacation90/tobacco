<template>
  <!-- Contents -->
  <div>
    <va-button-toggle style="width: fit-content" class="ma-3"
    :rounded="false"
    v-model="model"
    :options="[
      { label: 'One', value: 'one' },
      { label: 'Two', value: 'two' },
      { label: 'Three', value: 'three' },
    ]"
    />
    <div class="row">
    <div>
      <template v-for="data in models.data" :key="data.to">
        <div class="flex xs12 sm6 lg4 xl3 ma-3" style="width: 100%;">
        <va-card stripe stripe-color="info"
          @click="showFirstModal = !showFirstModal">
          <!-- Image -->
          <va-image
              :src="data.image"
              style="height: 200px;"/>
            <!-- Title -->
            <va-card-title>
              {{data.name}}
            </va-card-title>
            <!-- Disc -->
            <va-card-content class="card-disc">
              {{data.discription}}
            </va-card-content>
        </va-card>
      </div>
      </template>
    </div>
    <!-- Modal -->
    <va-modal v-model="showFirstModal" :message="firstMessage" hide-default-actions>
    <slot>
      <va-button class="mr-2" @click="$vaToast.init('Hello')">Basic notification</va-button>
      <va-popover message="Popover text"><va-button>Hover me</va-button></va-popover>
      <va-date-input class="mt-2" />

      <va-button class="mt-5" @click="showSecondModal = !showSecondModal" color="secondary">
        Show second modal
      </va-button>

      <va-modal v-model="showSecondModal" :message="secondMessage">
        <slot>
          <va-button class="mr-2" @click="$vaToast.init('Hello')">Show notification</va-button>
          <va-popover message="Popover text"><va-button>Hover me</va-button></va-popover>
          <va-select class="mt-2" v-model="value" :options="options" />
        </slot>
      </va-modal>
    </slot>
  </va-modal>

    </div>
  </div>
</template>

<style>

.card-cont {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  background: #d4ddf8;
}

.card-disc {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.container:after {
  clear: both;
  content: '';
  display: block;
}

</style>

<script>
import { defineComponent, reactive } from 'vue';

export default defineComponent({
  data () {
    return {
      showFirstModal: false,
      showSecondModal: false,
      firstMessage: 'First modal message',
      secondMessage: 'Second modal message',
      value: '',
      options: ['one', 'two', 'three'],
    }
  },
  setup() {
  },
});
</script>
