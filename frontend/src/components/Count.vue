<template>
  <div class="kiosk-count">
    <v-btn @click="clearAll" class="action-button" color="primary" dark x-large>전체 삭제</v-btn>
    <v-btn @click="openDialog" class="action-button" color="success" dark x-large>{{ totalPrice }}원 결제</v-btn>
    <checkOrderDialog :dialog="dialog" :orderList="orderList" :totalPrice="totalPrice"
      @update:dialog="dialog = $event" />
    <PayData @update:dialog1="dialog1 = $event" :totalPrice="totalPrice" @update:dialog2="dialog2 = $event" />
  </div>
</template>

<script>
import { EventBus } from '../main.js';
import checkOrderDialog from '../dialogs/checkOrderDialog.vue';
import PayData from '../dialogs/PayData.vue'
export default {
  components: {
    checkOrderDialog,
    PayData
  },
  data() {
    return {
      orderList: {},
      totalPrice: 0,
      dialog: false,
      dialog1: false,
      dialog2: false,
    };
  },
  mounted() {
    EventBus.$on('add-to-cart', this.addToOrder); // 이벤트 버스로 메뉴의 물품 데이터를 받아옴
    EventBus.$on('sendItemName', (itemName) => {  // 삭제할 물품의 이름을 받아옴
      this.$delete(this.orderList, itemName);
    });
    EventBus.$on('openWindow', this.openDialog);
    EventBus.$on('deleteOrder', this.clearAll);
  },
  methods: {
    clearAll() {  // 물품 데이터 전체를 삭제하는 함수
      this.orderList = {};
      this.$store.commit('delAllItem');
      EventBus.$emit('clearAll');
    },

    openDialog() {  // 팝업창을 여는 함수
      if (this.totalPrice == 0) {
        alert("총 금액이 0원입니다. 메뉴를 선택하세요.")
      }
      else this.dialog = true;
    },

    addToOrder(item) {  // 주문 내역 확인에 물품 데이터를 추가하는 함수
      if (!this.orderList[item.p_name]) {
        this.$set(this.orderList, item.p_name, { count: 0, price: 0, unitPrice: item.p_price });
      }
      this.orderList[item.p_name].count += 1;
      this.orderList[item.p_name].price = this.orderList[item.p_name].unitPrice;
      console.log("성곤!!!!!", this.orderList[item.p_name].price)
    },
  },
  computed: {
    updateCount() { // vuex에서 받은 객체 형식의 제품이름, 카운트 데이터
      return this.$store.getters.itemCount;
    },

    updateTotalPrice() {  // vuex에서 받은 합계
      return this.$store.getters.getTotalPrice;
    }
  },
  watch: {
    updateCount(newCount) { // 물품의 개수를 반영하는 함수
      console.log('updateCount 함수가 호출되었습니다.', newCount);
      for (const itemName in this.orderList) {
        if (this.orderList.hasOwnProperty(itemName)) {
          const item = this.orderList[itemName];
          const updatedItem = newCount.find(item => item.name === itemName);
          if (updatedItem) {
            item.count = parseInt(updatedItem.count);
            console.log("vuex로 받은 카운트 갯수: ", item.count);
          }
        }
      }
    },

    updateTotalPrice(newPrice) {  // 합계를 반영하는 함수
      this.totalPrice = newPrice
      console.log("vuex로 받은 합계: ", newPrice)
    }
  },

};
</script>

<style scoped>
.kiosk-count {
  /* 전체 영역 스타일 */
  padding: 2em;
  margin-top: 1em;
  background-color: #f8f8f8;
}

.action-button {
  /* 버튼 스타일 */
  margin-bottom: 0.1em;
  width: 100%;
  height: 100%;
  font-size: 18px;
}
</style>