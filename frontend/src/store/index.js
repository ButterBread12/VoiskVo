import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        items: [],  // { name: item.p_name, count: 0, price: 0, unitPrice: item.p_price } 등등 장바구니 데이터가 담긴 곳
        totalPrice: 0,  // 합계
    },
    getters:{
        itemCount(state) {
            return state.items.map(item => ({ count: item.count, name: item.name }));
        },
        getTotalPrice(state) {
            return state.totalPrice;
        },
    },
    mutations: {
        addItem(state, newItem) {   // 물품 데이터 추가
            state.items.push(newItem);
        },

        delItem(state, itemName) {  // 물품 데이터 제거
            const index = state.items.findIndex(item => item.name == itemName);
            if (index !== -1) {
                state.items.splice(index, 1);
            }
        },

        delAllItem(state){  // 모든 물품 데이터 제거
            state.items = [];
        },

        updateItemPrice(state, {itemName, price}) { // 물품의 가격을 업데이트 (현재 사용안함)
            const item = state.items.find(item => item.name == itemName);
            if (item) {
                item.price = parseInt(price);
                console.log(item)
                console.log(item.price)
            }
        },

        updateTotalPrice(state, totalPrice) {    // 합계를 업데이트
            state.totalPrice = totalPrice;
        },
    },
});