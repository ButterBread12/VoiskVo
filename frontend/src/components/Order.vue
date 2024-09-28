<template>
  <div class="order-container">
    <h1>주문 목록</h1>
    <ul>
      <li v-for="(item, itemName) in orderList" :key="itemName" class="order-item">
        <div class="item-name">{{ itemName }}</div>
        <div class="item-price">{{ item.price }}원</div>
        <div class="item-quantity">
          <button @click="decreaseCount(itemName)" class="quantity-button decrease">-</button>
          {{ item.count }}
          <button @click="increaseCount(itemName)" class="quantity-button increase">+</button>
          <v-btn @click="deleteItem(itemName)" class="quantity-button delete">삭제</v-btn>
        </div>
      </li>
      <div class="total-price">
        총 가격: {{ totalPrice }}원
      </div>
    </ul>
  </div>
</template>

<script>
import { EventBus } from '../main';

export default {
  data() {
    return {
      orderList: {},
      dialog: false,
    };
  },
  mounted() {
    EventBus.$on('add-to-cart', this.addToOrder);   // 이벤트 버스로 메뉴의 물품 데이터를 받아옴
    EventBus.$on('clearAll', this.clearOrderList);  // count 컴포넌트에서 전체삭제 버튼을 누를 경우 이벤트 버스를 받아옴
  },
  methods: {
    addToOrder(item) {  // 주문 목록에 물품 데이터를 추가하는 함수
      if (!this.orderList[item.p_name]) { // orderList에 데이터가 없으면
        this.$set(this.orderList, item.p_name, { name: item.p_name, count: 0, price: 0, unitPrice: item.p_price });
        this.$store.commit('addItem', this.orderList[item.p_name]);
        console.log("추가된 물품: ", this.orderList[item.p_name])
      }
      this.orderList[item.p_name].count += 1;
      this.orderList[item.p_name].price = this.orderList[item.p_name].unitPrice * this.orderList[item.p_name].count;
    },

    decreaseCount(itemName) { // 물품 개수를 감소하는 함수
      if (this.orderList[itemName].count > 1) {
        this.orderList[itemName].count -= 1;
        this.orderList[itemName].price = this.orderList[itemName].unitPrice * this.orderList[itemName].count;
        //this.$store.commit('updateItemPrice', itemName, this.orderList[itemName].price); (필요 없음)
        console.log("이름: ", itemName, "가격: ", this.orderList[itemName].price)
      } else {
        this.deleteItem(itemName);
      }
    },

    increaseCount(itemName) { // 물품 개수를 증가하는 함수
      this.orderList[itemName].count += 1;
      this.orderList[itemName].price = this.orderList[itemName].unitPrice * this.orderList[itemName].count;
      //this.$store.commit('updateItemPrice', {itemName: itemName, price: this.orderList[itemName].price}); (필요 없음)
      console.log("이름: ", itemName, "가격: ", this.orderList[itemName].price)
    },

    deleteItem(itemName) {  // 물품을 삭제하는 함수
      this.$delete(this.orderList, itemName);
      this.$store.commit('delItem', itemName);
      EventBus.$emit('sendItemName', itemName);
    },

    clearOrderList() {  // 주문목록 내의 물품 전체를 삭제하는 함수
      this.orderList = {};
    },
    
  },
  computed: {
    totalPrice() {  // 합계를 구하는 데이터
      const total = Object.values(this.orderList).reduce((total, item) => total + item.price, 0);
      return total
    },
  },
  watch: {
    totalPrice(newPrice) {  // 합계를 vuex로 전달하는 함수
      this.$store.commit('updateTotalPrice', newPrice);
    },
  },
};
</script>

<style scoped>
.order-container {
  /* 주문 목록을 감싸는 컨테이너 스타일 */
  max-width: 600px;
  margin: 20px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #f8f8f8;
}

.order-container h1 {
  /* 주문 목록 제목 스타일 */
  font-size: 24px;
  margin-bottom: 20px;
}

.order-container ul {
  /* 주문 목록을 담는 ul 요소 스타일 */
  list-style-type: none;
  padding: 0;
}

.order-item {
  /* 주문 아이템 스타일 */
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.order-container button {
  /* 주문 버튼 스타일 */
  margin: 0 5px;
}

.item-name {
  /* 주문 아이템 이름 스타일 */
  font-size: 18px;
}

.item-quantity {
  /* 주문 아이템 수량 스타일 */
  font-size: 16px;
}

.item-price {
  /* 주문 아이템 가격 스타일 */
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
}

.quantity-button {
  /* 수량 조절 버튼 스타일 */
  padding: 8px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.decrease {
  /* 수량 감소 버튼 스타일 */
  background-color: #dc3545;
  color: white;
}

.increase {
  /* 수량 증가 버튼 스타일 */
  background-color: #28a745;
  color: white;
}

.total-price {
  /* 총 가격 스타일 */
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
  text-align: right;
}
</style>
