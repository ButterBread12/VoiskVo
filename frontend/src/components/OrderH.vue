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
  methods: {
    addToOrder(item) {
      if (!this.orderList[item.p_name]) {
        this.$set(this.orderList, item.p_name, { count: 0, price: 0, unitPrice: item.p_price });
      }
      this.orderList[item.p_name].count += 1;
      this.orderList[item.p_name].price = this.orderList[item.p_name].unitPrice * this.orderList[item.p_name].count;
    },
    decreaseCount(itemName) {
      if (this.orderList[itemName].count > 1) {
        this.orderList[itemName].count -= 1;
        this.orderList[itemName].price = this.orderList[itemName].unitPrice * this.orderList[itemName].count;
      } else {
        this.deleteItem(itemName);
      }
      // 값이 변경될 때마다 EventBus를 통해 이벤트 발생
      EventBus.$emit('orderItemChanged', this.orderList[itemName]);
    },
    increaseCount(itemName) {
      this.orderList[itemName].count += 1;
      this.orderList[itemName].price = this.orderList[itemName].unitPrice * this.orderList[itemName].count;
      // 값이 변경될 때마다 EventBus를 통해 이벤트 발생
       EventBus.$emit('orderItemChanged', this.orderList[itemName]);
    },

    deleteItem(itemName) {
      this.$delete(this.orderList, itemName);
    },
    clearOrderList() {
      this.orderList = {};
    },
    
  },
  mounted() {
    EventBus.$on('add-to-cart', this.addToOrder);
    EventBus.$on('clearAll', this.clearOrderList);
  },
  computed: {
    totalPrice() {
      const total = Object.values(this.orderList).reduce((total, item) => total + item.price, 0);
      return total
    },
  },
  watch: {
    totalPrice(newPrice) {
      EventBus.$emit('totalPriceUpdated', newPrice);
    },
  },
};
</script>

<style scoped>
.order-container {
  max-width: 600px;
  margin: 20px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #f8f8f8;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.item-name {
  font-size: 18px;
}

.item-quantity {
  font-size: 16px;
}

.item-price {
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
}

.quantity-button {
  padding: 8px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.decrease {
  background-color: #dc3545;
  color: white;
}

.increase {
  background-color: #28a745;
  color: white;
}

button {
  margin: 0 5px;
}

.total-price {
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
  text-align: right;
}
</style>
