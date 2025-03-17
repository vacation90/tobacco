<template>
  <div>
    <va-sidebar :minimized="!minimized" textColor="dark" minimizedWidth="0" >
      <va-sidebar-item>
        <va-sidebar-item-content>
          <va-icon name="search" />
          <va-sidebar-item-title>
            <va-input
              v-model="value"
              placeholder="Search"
            ></va-input>
          </va-sidebar-item-title>
        </va-sidebar-item-content>
      </va-sidebar-item>


      <va-accordion class="sidebar-accordion" v-model="columns" multiply>
        <va-collapse
          v-for="(route, idx) in columns"
          :key="idx"
          :class="{ expanded: route.accordionValue && route.listvalue }"
        >

          <template #header>
            <va-sidebar-item>
              <va-sidebar-item-content>
                <va-sidebar-item-title>
                  {{ route.name }}
                </va-sidebar-item-title>

                <va-icon v-if="route.listvalue" :name="route.accordionValue ? 'expand_less' : 'expand_more'" />
              </va-sidebar-item-content>
            </va-sidebar-item>
          </template>

          <div>
            <va-sidebar-item v-if="route.column_type.includes('DECIMAL')">
              <va-sidebar-item-content>
                <va-sidebar-item-title>
                  <va-slider
                    v-model="value"
                    range
                    track-label-visible
                    :track-label="processTrackLabel"
                  />
                </va-sidebar-item-title>
              </va-sidebar-item-content>
            </va-sidebar-item>
          </div>
          
          <div v-for="(listvalue, index) in route.listvalue" :key="index">
            <va-sidebar-item>
              <va-sidebar-item-content>
                <va-sidebar-item-title>
                  <va-checkbox class="ml-2" v-model="listvalue.filter" :label="listvalue.name" />
                </va-sidebar-item-title>
              </va-sidebar-item-content>
            </va-sidebar-item>
          </div>

        </va-collapse>
      </va-accordion>

    </va-sidebar>
  </div>
</template>


<script>
  import { defineComponent } from 'vue';
  export default defineComponent({
    name: "SideBar",
    props: {
        minimized: Object,
        dbColumns: Object,
    },
    setup(props){
        console.log(props);
        return {
          accordionValue: [false, true],
          columns: props.dbColumns,
        }
    },
  });
  // export default {
  //   props: ["minimized", "columns"],
  //   data () {
  //     console.log('columns', this.columns);
  //     return {
  //       accordionValue: [false, true],
  //       // columns: this.columns,
  //     }
  //   }
  // }
</script>
