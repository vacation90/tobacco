<template>
  <div id="app" class="grid-container">
    <div class="header">
      <NavBar/>
    </div>
    <div class="menu">
      <va-sidebar textColor="dark" v-show="stateManager.isMenuToggle">
        <va-accordion
          class="sidebar-accordion"
          v-model="accordionValue"
          multiple
        >
          <div
            v-for="(route, idx) in dbColumns"
            :key="idx"
            :class="{ expanded: accordionValue && dbColumns[idx].list_value }"
          >
            <va-collapse
              v-show="!route.data_type.includes('url') &&
              !route.data_type.includes('image')"
            >
              <template #header>
                <va-sidebar-item>
                  <va-sidebar-item-content>
                    <va-sidebar-item-title>
                      {{ route.name }}
                    </va-sidebar-item-title>
                    <va-icon
                      v-if="dbColumns[idx].list_value"
                      :name="accordionValue[idx] ? 'expand_less' : 'expand_more'"
                    />
                  </va-sidebar-item-content>
                </va-sidebar-item>
              </template>

              <div>
                <va-sidebar-item v-if="
                  route.data_type.includes('num') ||
                  route.data_type.includes('int')
                ">
                  <va-sidebar-item-content>
                    <va-sidebar-item-title>
                      <va-slider
                        v-model="dbColumns[idx].num_filter"
                        range
                        track-label-visible
                        :track-label="processTrackLabel"
                        :min="route.value_range[0]"
                        :max="route.value_range[1]"
                        :step="route.data_type == 'num' ? 0.1 : 1"
                        @drag-end="getFilterItems"
                      />
                    </va-sidebar-item-title>
                  </va-sidebar-item-content>
                </va-sidebar-item>

                <va-sidebar-item v-if="
                  route.data_type.includes('date')
                ">
                  <va-sidebar-item-content>
                    <va-date-picker
                      v-model="dbColumns[idx].date_filter"
                      @update:model-value="getFilterItems"
                      mode='range'
                    />
                  </va-sidebar-item-content>
                </va-sidebar-item>

                <va-sidebar-item v-if="
                  route.data_type.includes('text') &&
                  !route.list_value.length
                ">
                  <va-sidebar-item-content>
                    <va-sidebar-item-title>
                      <va-input
                        v-model="dbColumns[idx].search_filter"
                        label="検索"
                        placeholder="Search"
                        @update:model-value="getFilterItems"
                        style="max-width: 200px;"
                      >
                        <template #prependInner>
                          <va-icon name="search" />
                        </template>
                      </va-input>
                    </va-sidebar-item-title>
                  </va-sidebar-item-content>
                </va-sidebar-item>
              </div>

              <div>
              <va-sidebar-item
                v-for="(list_value, index) in route.list_value"
                :key="index"
              >
                <va-sidebar-item-content>
                  <va-checkbox
                    class="ml-2"
                    v-model="list_value.filter"
                    :label="list_value.name"
                    @update:model-value="getFilterItems"
                  />
                </va-sidebar-item-content>
              </va-sidebar-item>
              </div>

            </va-collapse>
          </div>
        </va-accordion>
      </va-sidebar>
    </div>
    <div class="body">
      <div class="d-flex mt-3 px-3">
        <va-switch
        size="large"
        v-model="currentToggle"
        color="#2c82e0"
        off-color="#ffd300"
        style="--va-switch-checker-background-color: #252723;"
        >
          <template #innerLabel>
            <div class="va-text-center">
              <va-icon
                size="24px"
                :name="currentToggle ? 'space_dashboard' : 'format_list_bulleted'"
              />
              {{ currentToggle ? 'Tile' : 'List' }}
            </div>
          </template>
        </va-switch>
        <va-spacer/>
        <va-card
          color="secondary"
          gradient
          style="max-height: 50px;"
        >
          <div class="d-flex">
            <va-card-title>Total items </va-card-title>
            <va-card-content style="font-size: 50px;">
              {{ dbItems.length }}
            </va-card-content>
          </div>
        </va-card>
      </div>
      <!-- Tile -->
      <div v-show="currentToggle">
        <TileView
          :dbColumns="dbColumns"
          :dbItems="dbItems"
        />
      </div>
      <!-- List -->
      <div v-show="!currentToggle">
        <ListView :dbColumns="dbColumns" :dbItems="dbItems" :listColumns="listColumns"/>
      </div>
      <!-- Pagination -->
      <div
        class="flex md12 ma-5"
        v-show="currentToggle"
        style="width: 100%"
      >
        <va-pagination
          :visible-pages="7"
          v-model="stateManager.pageIndex"
          :total="dbItems.length"
          boundary-numbers
          :page-size="stateManager.pageSize"
          gapped
        />
      </div>
    </div>
    <div class="footer">
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive } from "vue";
import { useStateManager } from "../stores/StateManager";
import axios from "axios";
import TileView from "./TileView.vue";
import ListView from "./ListView.vue";
import Footer from "./Footer.vue";
import NavBar from "./NavBar.vue";
export default defineComponent({
  data () {
    return {
      currentToggle: true,
    }
  },
  components: {
    TileView,
    ListView,
    Footer,
    NavBar
  },
    setup() {
    const baseURL = "http://localhost:8000";
    const stateManager = useStateManager();
    let dbColumns = reactive([]);
    let listColumns = reactive([]);
    let dbItems = reactive([]);
    const getColumns = async () => {
      let response = await axios.get(baseURL + "/columns/all");
      console.log("response.data", response);
      listColumns.push('image');
      listColumns.push('name');
      for (let key in response.data) {
        var response_column = response.data[key];
        if (response_column.value_range) {
          response_column.num_filter = response_column.value_range;
        }
        else if (response_column.date_range) {
          response_column.date_filter = {
            start: new Date(response_column.date_range['start']),
            end: new Date(response_column.date_range['end'])
          }
        }
        dbColumns.push(response_column);
        if (!['name', 'image'].includes(response_column.code) && response_column.data_type!='url') {
          listColumns.push(response_column.code);
        }
      }
      console.log('listColumns', listColumns)
    };
    const getItems = async () => {
      let response = await axios.get(baseURL + "/items/all");
      console.log("response.data", response.data);
      for (let key in response.data) {
        dbItems.push(response.data[key]);
      }
    };
    getColumns();
    getItems();
    return {
      accordionValue: [],
      dbColumns,
      listColumns,
      dbItems,
      stateManager,
    };
  },
  methods: {
    formatDate (date) {
      return `${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}`
    },
    async getFilterItems() {
      var today = new Date();
      today.setDate(today.getDate());
      var filterParams = [];
      console.log(this.dbColumns);
      for (var columnIndex in this.dbColumns) {
        var filterParam = {};
        var column = this.dbColumns[columnIndex];
        if (column.list_value.length) {
          for (var listValueIndex in column.list_value) {
            if (column.list_value[listValueIndex].filter) {
              if (!Object.keys(filterParam).length) {
                filterParam[column.code] = [];
              }
              filterParam[column.code].push(
                column.list_value[listValueIndex].name
              );
            }
          }
        } else if (column.num_filter) {
          filterParam[column.code] = [
            column.num_filter[0] + "~" + column.num_filter[1],
          ];
        } else if (column.search_filter) {
          filterParam[column.code] = column.search_filter;
        } else if (column.date_filter) {
          console.log('column.date_filter')
          console.log(column.date_filter)
          filterParam[column.code] = [`${column.date_filter.start.getFullYear()}-${column.date_filter.start.getMonth() + 1}-${column.date_filter.start.getDate()}~${column.date_filter.end.getFullYear()}-${column.date_filter.end.getMonth() + 1}-${column.date_filter.end.getDate()}`];
        }
        if (Object.keys(filterParam).length) {
          filterParams.push(filterParam);
        }
      }
      const baseURL = "http://localhost:8000";
      console.log(baseURL, filterParams);
      let response = await axios.post(baseURL + "/items/filter", filterParams);
      this.dbItems.splice(0);
      for (let key in response.data) {
        this.dbItems.push(response.data[key]);
      }
      console.log(this.dbItems);
      //表示アイテム変更時にページインデックスを1に戻す
      this.stateManager.setPageIndex(1);
    },
  },
});
</script>
