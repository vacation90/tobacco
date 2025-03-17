<template>
  <div id="app" data-v-app style="position: fixed; height: 100vh; width: 100%;">
    <!-- Navigation Bar -->
      <va-navbar color="primary" id="nav" class="mb-2" >
        <template #left>
        </template>
        <template #center>
          <va-icon name="home" size="2rem" />
        </template>
        <template #right>
          <va-button-group>
            <!-- Setting -->
            <va-button-dropdown icon="settings" >
              <div>
                <va-button :rounded="false" outline="false" flat>Contents</va-button>
              </div>
            </va-button-dropdown>
            <!-- Sample -->
            <va-button-dropdown label="Sample" keep-anchor-width="true">
              <div>
                <va-button :rounded="false" outline="false" flat>Sign in</va-button>
              </div>
              <div>
                <va-button :rounded="false" outline="false" flat>Logout</va-button>
              </div>
            </va-button-dropdown>
          </va-button-group>
        </template>
      </va-navbar>

    <!-- Main Body -->
    <div id="flex" style="position: relative; height: 100%; width: 100%">
      <!-- Side Bar -->
        <va-sidebar textColor="dark" style = "overflow-x: scroll;">
          <va-accordion class="sidebar-accordion" v-model="accordionValue" multiply>
            <va-collapse
                v-for="(route, idx) in dbColumns"
                :key="idx"
                :class="{ expanded: accordionValue && dbColumns[idx].list_value }"
            >

              <template #header>
                <va-sidebar-item>
                  <va-sidebar-item-content>
                    <va-sidebar-item-title>
                      {{ route.name }}
                    </va-sidebar-item-title>
                  <va-icon v-if="dbColumns[idx].list_value" :name="accordionValue[idx] ? 'expand_less' : 'expand_more'" />
                  </va-sidebar-item-content>
                </va-sidebar-item>
              </template>

              <div>
                <va-sidebar-item v-if="route.data_type.includes('num') || route.data_type.includes('int')">
                  <va-sidebar-item-content>
                    <va-sidebar-item-title>
                      <va-slider
                        v-model="dbColumns[idx].filter"
                        range
                        track-label-visible
                        :track-label="processTrackLabel"
                        :min="route.value_range[0]"
                        :max="route.value_range[1]"
                        :step="route.data_type=='num' ? 0.1 : 1"
                        @drag-end="getFilterItems"
                      />
                    </va-sidebar-item-title>
                  </va-sidebar-item-content>
                </va-sidebar-item>
              </div>

              <va-sidebar-item v-for="(list_value, index) in route.list_value" :key="index">
                <va-sidebar-item-content>
                  <va-checkbox class="ml-2" v-model="list_value.filter" :label="list_value.name" @update:model-value="getFilterItems"/>
                </va-sidebar-item-content>
              </va-sidebar-item>

            </va-collapse>
          </va-accordion>
        </va-sidebar>
      <!-- Main Content -->
        <div style="position: relative; display: flex; top:0; left:0; height: 100%; width: 100%">
          <div style = "overflow: scroll;">
              <!-- Toggle -->
              <va-button-toggle class="ma-3"
                :rounded="false"
                v-model="currentToggle"
                :options="toggles" >
              </va-button-toggle>
              <!-- Pagination -->
              <div class="flex md12 ma-5" style="width: 100%;">
                <va-pagination
                  :visible-pages="7"
                  v-model="pageIndex"
                  :total="dbItems.length"
                  boundary-numbers
                  :page-size="pageSize"
                />
              </div>
              <!-- Tile -->
              <div v-show="currentToggle=='tile'">
                <TileView :dbColumns="dbColumns" :dbItems="dbItems" :pageIndex="pageIndex" :pageSize="pageSize"/>
              </div>
              <!-- List -->
              <div v-show="currentToggle=='list'">
                <ListView :dbColumns="dbColumns" :dbItems="dbItems"/>
              </div>
              <!-- Pagination -->
              <div class="flex md12 ma-5" style="width: 100%;">
                <va-pagination
                  :visible-pages="7"
                  v-model="pageIndex"
                  :total="dbItems.length"
                  boundary-numbers
                  :page-size="pageSize"
                />
              </div>
          </div>
        </div>
    </div>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
// import SideBar from './SideBar.vue'
import TileView from '.../TileView.vue'
import ListView from '.../ListView.vue'
import Footer from '.../Footer.vue'
import { defineComponent, reactive, ref } from 'vue';
import axios from 'axios';
export default defineComponent({
  components: {
    // SideBar,
    TileView,
    ListView,
    Footer,
  },
  data () {
    return {
      page: 1,
    }
  },
  setup() {
    const baseURL = 'http://localhost:8000';
    // let data = reactive({})
    let dbColumns = reactive([])
    let dbItems = reactive([])
    let displayLists = reactive([])
    let pageSize = ref(15)
    let pageIndex = ref(1)
    // let sidebarData = reactive([]);
    let currentToggle = ref('tile');
    let toggles = [
      { label: 'Tile', value: 'tile' },
      { label: 'List', value: 'list' },
    ]
    const getColumns = async () => {
      let response = await axios.get(baseURL + '/columns/all');
      console.log('response.data', response.data);
      for (let key in response.data) {
        var response_column = response.data[key]
        if (response_column.value_range) {
          response_column.filter = response_column.value_range
        }
        dbColumns.push(response_column);
      }
      // dbColumns = reactive(response.data);
    };
    const getItems = async () => {
      let response = await axios.get(baseURL + '/items/all');
      console.log('response.data', response.data);
      for (let key in response.data) {
        dbItems.push(response.data[key]);
      }
      // dbItems = reactive(response.data);
      let tempList = dbItems.slice(0,pageSize);
      for(let index in tempList){
        displayLists.push(tempList[index]);
      }
    };
    getColumns();
    getItems();
    return {
      accordionValue: [],
      toggles,
      currentToggle,
      dbColumns,
      dbItems,
      displayLists,
      pageSize,
      pageIndex,
    };
  },
  methods: {
    async getFilterItems(){
      var filterParams = [];
      console.log(this.dbColumns)
      for (var columnIndex in this.dbColumns) {
        var filterParam = {};
        var column = this.dbColumns[columnIndex]
        console.log(column.filter)
        if (column.list_value.length) {
          for (var listValueIndex in column.list_value) {
            if (column.list_value[listValueIndex].filter) {
              if (!Object.keys(filterParam).length) {
                filterParam[column.code] = [];
              }
              filterParam[column.code].push(column.list_value[listValueIndex].name);
            }
          }
        }
        else if (column.filter) {
          filterParam[column.code] = [column.filter[0]+'-'+column.filter[1]]
        }
        if (Object.keys(filterParam).length) {
          filterParams.push(filterParam);
        }
      }
      const baseURL = 'http://localhost:8000';
      console.log(baseURL, filterParams);
      let response = await axios.post(baseURL + '/items/filter', filterParams);
      this.pageIndex = 1
      this.dbItems.splice(0);
      for (let key in response.data) {
        this.dbItems.push(response.data[key]);
      }
      console.log(this.dbItems);
    },
    pageChange(page){//表示用のアイテムリスト作成
      this.displayLists.splice(0);
      let tempList = this.dbItems.slice(page - 1, page + this.pageSize - 1);
      for(let index in tempList){
        this.displayLists.push(tempList[index]);
      }
    },
  },
});
</script>
