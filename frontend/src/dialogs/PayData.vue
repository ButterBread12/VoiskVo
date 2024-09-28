<template>
  <div>
    <!-- 카드결제화면 -->
    <v-dialog v-model="localDialog1" class="payment-dialog">
      <v-card class="order-summary">
        <v-card-title class="order-summary-title">카드 결제</v-card-title>
        <v-card class="payment-content">
          <h3>다음 그림과 같이 신용/체크카드를 넣어주세요</h3>
          <v-img src="https://cdn0.iconfinder.com/data/icons/business-collection-2027/60/atm-1-512.png" height="200"
            width="200"></v-img>
        </v-card>
        <v-card class="total-price">
          <span class="total-price-label">총 결제 금액</span>
          <span class="total-price-value">{{ totalPrice }}원</span>
        </v-card>
        <v-card-actions class="card-actions">
          <v-btn @click="pay" class="pay-btn" dark>
            <v-img src="../components/p/card_insert_moving.png" height="100" width="100" class="movecard"></v-img>
          </v-btn>
          <v-btn @click="closeDialog" class="close-btn" dark>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 쿠폰결제화면 -->
    <v-dialog v-model="localDialog2" class="payment-dialog">
      <v-card class="order-summary">
        <v-card-title class="order-summary-title">쿠폰 결제</v-card-title>
        <v-card class="payment-content">
          <h3>쿠폰의 바코드를 대주세요</h3><br>
          <v-img src="https://cdn-icons-png.flaticon.com/512/25/25350.png" height="180" width="400"></v-img><br>
        </v-card>
        <v-card class="total-price">
          <span class="total-price-label">총 결제 금액</span>
          <span class="total-price-value">{{ totalPrice }}원</span>
        </v-card>
        <v-card-actions class="card-actions">
          <v-btn @click="pay" class="pay-btn" dark>
            <v-img max-width="90" src="../components/p/barcode.png"></v-img>
          </v-btn>
          <v-btn @click="closeDialog" class="close-btn" dark>닫기</v-btn>
        </v-card-actions>
        <h5 class="bartext">바코드를 대주세요</h5>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { EventBus } from '../main.js';
import axios from 'axios';

export default {
  props: {
    dialog1: Boolean,
    dialog2: Boolean,
    totalPrice: Number
  },
  data() {
    return {
      localDialog1: this.dialog1,
      localDialog2: this.dialog2,
    };
  },
  watch: {
    //checkOrderDialog.vue에서 변경된 dialog1,2 prop의 값을 localDialog1,2에 반영
    dialog1(newVal) {
      this.localDialog1 = newVal;
    },
    dialog2(newVal) {
      this.localDialog2 = newVal;
    }
  },
  mounted() {
    EventBus.$on('select-payment', (method) => { // 이벤트 버스로 해당 페이지(카드결제 OR 쿠폰결제) 화면 불러오기
      if (method === '카드결제') {
        this.localDialog1 = true;
      }
      else if (method === '쿠폰결제') {
        this.localDialog2 = true;
      }
    });
  },
  methods: {
    closeDialog() { // 팝업창을 닫는 함수
      this.localDialog1 = false;
      this.localDialog2 = false;
    },
    async pay() {
      const selectedItems = this.$store.state.items.map(item => `${item.name}(${item.count}개)`).join(', ');
      setTimeout(() => {
        const message = `주문내역: ${selectedItems}\n총 금액: ${this.totalPrice}원`;
        if (confirm(message)) {
          console.log("message: ", message)
          // API를 호출하여 아두이노로 데이터 전송
          axios.post('http://localhost:8000/order', {
            message: message            
          });
        }
        this.$store.commit('delAllItem');
        location.href = "http://localhost:8080/";
      }, 1000);
    },
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.order-summary {
  max-width: 600px;
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 25px;
  font-family: 'Roboto', sans-serif;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.order-summary-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
  color: #34495e;
}

.payment-content h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #34495e;
}

.payment-content img {
  margin-bottom: 20px;
}

.total-price {
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 2px solid #3498db;
  background-color: #ecf9ff;
}

.total-price-label {
  font-size: 16px;
}

.total-price-value {
  font-size: 18px;
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
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 25px;
  padding: 10px 20px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.pay-btn:hover {
  background-color: #2980b9;
  transform: translateY(-3px);
}

.close-btn {
  background-color: #e74c3c;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 25px;
  padding: 10px 20px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.close-btn:hover {
  background-color: #c0392b;
  transform: translateY(-3px);
}

.payment-dialog {
  width: 80%;
  max-width: 500px;
}

.payment-content {
  display: flex;
  padding: 20px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.movecard {
  top: 25px;
}

.bartext {
  margin-top: 20px;
  text-align: center;
  color: #34495e;
}
</style>
