<template>
  <!-- Filter -->
  <div class="row">
    <va-input
      class="flex mb-2 md6 my-3 px-3"
      placeholder="Filter..."
      v-model="input"
    />
    <va-checkbox
      class="flex mb-2 md6 my-3 px-3"
      label="Use custom filtering function (looks for an exact match)"
      v-model="useCustomFilteringFn"
    />
  </div>
  <!-- List -->
  <va-data-table
    :items="dbItems"
    :filter="filter"
    :hoverable="true"
    :striped="true"
    :footerClone="true"
    :animated="true"
    :filter-method="customFilteringFn"
    :columns="listColumns"
  >
    <template #cell(image)="{ value }">
      <va-badge
        class="mr-6"
      >
        <va-avatar
          square
          :src="value"
        />
      </va-badge>
    </template>
  </va-data-table>
</template>

<script>
import { defineComponent } from "vue";
import debounce from 'lodash/debounce.js'
export default defineComponent({
  name: "ListView",
  props: {
    dbColumns: Object,
    listColumns: Object,
    dbItems: Object,
  },
  setup(props) {
    console.log("props");
    console.log(props);
  },
  data () {

    return {
      input:'',
      filter:'',
      useCustomFilteringFn: false,
      isDebounceInput: true,
    }
  },
	computed: {
    customFilteringFn () {
      return this.useCustomFilteringFn ? this.filterExact : undefined
    },
  },

  methods: {
    filterExact (source) {
      if (this.filter === '') {
        return true
      }

      return source?.toString?.() === this.filter
    },
    updateFilter (filter) {
      this.filter = filter
    },
    debouncedUpdateFilter: debounce(function (filter) {
      this.updateFilter(filter)
    }, 600),
  },
  watch: {
    input (newValue) {
      if (this.isDebounceInput) {
        this.debouncedUpdateFilter(newValue)
      } else {
        this.updateFilter(newValue)
      }
    },
  },
});
</script>
