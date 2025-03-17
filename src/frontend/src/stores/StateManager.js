import { defineStore } from 'pinia';

export const useStateManager = defineStore('stateManager', {
  state: () => ({
    menuToggle: true,
    pageIndex: 1,
    pageSize: 15,
    modalItem: null
  }),
  getters: {
    isMenuToggle: (state) => state.menuToggle,
    getPageIndex: (state) => state.pageIndex,
    getPageSize: (state) => state.pageSize,
    getModalItem: (state) => state.modalItem,
  },
  actions: {
    menuAction() {
      this.menuToggle=!this.menuToggle;
    },
    setPageIndex(num) {
      this.pageIndex=num;
    },
    setPageSize(num) {
      this.pageSize=num;
    }
  },
});
