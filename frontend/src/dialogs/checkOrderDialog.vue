<template>
  <v-dialog v-model="dialog">
    <!-- 팝업 창 내용 시작 -->
    <v-card class="order-summary">
      <v-card-title class="order-summary-title">주문 내역 확인</v-card-title>
      <v-card class="order-details">
        <span>주문 내역</span>
        <span>수량</span>
        <span>금액</span>
      </v-card>
      <ul class="order-list">
        <li v-for="(item, itemName) in orderList" :key="itemName" class="order-item">
          <div class="item-name">{{ itemName }}</div>
          <div class="item-count">{{ item.count }}</div>
          <div class="item-price">{{ item.price * item.count }}원</div>
        </li>
      </ul>
      <v-card class="total-price">
        <span class="total-price-label">결제 금액</span>
        <span class="total-price-value">{{ totalPrice }}원</span>
      </v-card>
      <v-card-actions class="card-actions">
        <v-btn v-if="!paymentOptionSelected" class="pay-btn" @click="selectOption('매장')">
          <v-img src="https://cdn-icons-png.flaticon.com/512/5452/5452940.png" height="30" width="30"></v-img>
          <span>매장</span>
        </v-btn>
        <v-btn v-if="!paymentOptionSelected" class="pay-btn" @click="selectOption('포장')">
          <v-img src="https://cdn-icons-png.flaticon.com/512/3081/3081098.png" height="30" width="30"></v-img>
          <span>포장</span>
        </v-btn>
        <v-btn v-if="paymentOptionSelected" class="pay-btn" @click="selectPayment('카드결제')">
          <v-img src="https://cdn-icons-png.flaticon.com/512/4341/4341764.png" height="30" width="30"></v-img>
          <span>카드결제</span>
        </v-btn>
        <v-btn v-if="paymentOptionSelected" class="pay-btn" @click="selectPayment('쿠폰결제')">
          <v-img src="https://cdn-icons-png.flaticon.com/512/2089/2089363.png" height="30" width="30"></v-img>
          <span>쿠폰결제</span>
        </v-btn>
        <v-btn class="back-btn" @click="resetButtons">뒤로가기</v-btn>
        <v-btn class="close-btn" @click="closeDialog">닫기</v-btn>
      </v-card-actions>
    </v-card>
    <!-- 팝업 창 내용 끝 -->
  </v-dialog>
</template>

<script>
import { EventBus } from '../main.js';
export default {
  props: {
    dialog: Boolean,
    orderList: Object,
    totalPrice: Number
  },
  data() {
    return {
      paymentDialog: false,
      paymentOptionSelected: false,
    };
  },
  mounted() {
    EventBus.$on('select-option', (option) => {
      this.paymentOptionSelected = true;
    });
  },
  methods: {
    checkout() {
      console.log('Checkout');
    },
    closeDialog() {
      this.$emit('update:dialog', false);
    },
    selectOption(option) {
      console.log('선택한 옵션:', option);
      EventBus.$emit('select-option', option);
    },
    selectPayment(method) {
      console.log('선택한 결제 방식:', method);
      EventBus.$emit('select-payment', method);
      if (method === '카드결제') {
        this.$emit('update:dialog1', true);
      } else if (method === '쿠폰결제') {
        this.$emit('update:dialog2', true);
      }
    },
    resetButtons() {
      this.paymentOptionSelected = false;
    },
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.order-summary {
  max-width: 700px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 25px;
  font-family: 'Roboto', sans-serif;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.order-summary-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #2c3e50;
}

.order-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 18px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
}

.order-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 10px;
  background-color: #f8f9fa;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.item-name,
.item-count,
.item-price {
  flex: 1;
  font-size: 16px;
}

.item-count {
  text-align: center;
}

.item-price {
  text-align: right;
  font-weight: bold;
  color: #27ae60;
}

.total-price {
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 2px solid #3498db;
  background-color: #ecf9ff;
}

.total-price-label {
  font-size: 18px;
}

.total-price-value {
  font-size: 20px;
  font-weight: bold;
  color: #e74c3c;
}

.card-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.pay-btn {
  display: flex;
  align-items: center;
  background-color: #3498db;
  color: black;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 30px;
  padding: 12px 25px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.pay-btn:hover {
  background-color: #2980b9;
  transform: translateY(-3px);
}

.back-btn, .close-btn {
  background-color: #e74c3c;
  color: black;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 30px;
  padding: 12px 25px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.back-btn:hover, .close-btn:hover {
  background-color: #c0392b;
  transform: translateY(-3px);
}

.close-btn {
  margin-left: 10px;
}
</style>
