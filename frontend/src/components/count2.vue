<template>
  <div class="kiosk-buttons">
    <v-btn @click="clearAll" class="action-button" color="primary" dark>전체삭제</v-btn>
    <v-btn @click="openDialog" class="action-button" color="success" dark>{{ totalPrice }}원 결제하기</v-btn>

    <v-dialog v-model="dialog">
      <!-- 팝업 창 내용 시작 -->
      <v-card class="order-summary">
        <v-card-title class="order-summary-title">주문 내역 확인</v-card-title>
        <v-card class="order-details">
          <span>주문 내역</span>
          <span>수량</span>
          <span>금액</span>
        </v-card>
        <li v-for="(item, itemName) in orderList" :key="itemName" class="order-item">
          <div class="item-name">{{ itemName }}</div>
          <div class="item-count">{{ item.count }}</div>
          <div class="item-price">{{ item.price * item.count }}원</div>
        </li><br><br>
        <v-card class="total-price">
          <span class="total-price-label">결제 금액</span>
          <span class="total-price-value">{{ totalPrice }}원</span>
        </v-card>
        <v-card-actions class="card-actions">
          <v-btn v-if="!paymentOptionSelected" class="pay-btn" @click="selectOption('매장')">
            <v-img src="https://cdn-icons-png.flaticon.com/512/5452/5452940.png" height="30" width="30"></v-img>
            <span style="color: black;">매장</span>
          </v-btn>
          <v-btn v-if="!paymentOptionSelected" class="pay-btn" @click="selectOption('포장')">
            <v-img src="https://cdn-icons-png.flaticon.com/512/3081/3081098.png" height="30" width="30"></v-img>
            <span style="color: black;">포장</span>
          </v-btn>
          <v-btn v-if="paymentOptionSelected" class="pay-btn" @click="selectPayment('카드결제')">
            <v-img src="https://cdn-icons-png.flaticon.com/512/4341/4341764.png" height="30" width="30"></v-img>
            <span style="color: black;">카드결제</span>
          </v-btn>
          <v-btn v-if="paymentOptionSelected" class="pay-btn" @click="selectPayment('쿠폰')">
            <v-img src="https://cdn-icons-png.flaticon.com/512/2089/2089363.png" height="30" width="30"></v-img>
            <span style="color: black;">쿠폰</span>
          </v-btn>
          <v-btn dark @click="resetButtons">뒤로가기</v-btn>
          <v-btn @click="closeDialog" class="close-btn" dark>닫기</v-btn>
        </v-card-actions>
      </v-card>
      <!-- 팝업 창 내용 끝 -->
    </v-dialog>

    <!--결제화면-->
    <v-dialog v-model="dialog1" class="payment-dialog">
      <v-card class="order-summary">
        <v-card-title>카드 결제</v-card-title>
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
          <v-btn @click="pay" dark>결제하기</v-btn>
          <v-btn @click="closeDialog" class="close-btn" dark>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!--결제화면 끝-->

    <!--쿠폰화면-->
    <v-dialog v-model="dialog2" class="payment-dialog">
      <v-card class="order-summary">
        <v-card-title>쿠폰 결제</v-card-title>
        <v-card class="payment-content">
          <h3>다음 그림과 같이 해주세요</h3>
          <v-img src="https://cdn-icons-png.flaticon.com/512/2089/2089363.png" height="200" width="200"></v-img>
        </v-card>
        <v-card class="total-price">
          <span class="total-price-label">총 결제 금액</span>
          <span class="total-price-value">{{ totalPrice }}원</span>
        </v-card>
        <v-card-actions class="card-actions">
          <v-btn @click="pay" dark>결제하기</v-btn>
          <v-btn @click="closeDialog" class="close-btn" dark>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!--쿠폰화면 끝-->

  </div>
</template>

<script>
import { EventBus } from '../main.js';
export default {
  data() {
    return {
      orderList: {},
      totalPrice: 0,
      dialog: false,
      dialog1: false,
      dialog2: false,
      paymentDialog: false,
      paymentOptionSelected: false,
    };
  },
  mounted() {
    EventBus.$on('add-to-cart', this.addToOrder); // 이벤트 버스로 메뉴의 물품 데이터를 받아옴
    EventBus.$on('sendList', (orderList) => {     // (현재 사용 안함)
      this.orderList = orderList
    });
    EventBus.$on('sendItemName', (itemName) => {  // 삭제할 물품의 이름을 받아옴
      this.$delete(this.orderList, itemName);
    });
    EventBus.$on('clearAll', this.clearAll); // 'clearAll' 이벤트를 수신하고 전체 삭제 함수 호출

    EventBus.$on('select-option', (option) => {
      console.log('선택한 옵션:', option);
      this.paymentOptionSelected = true;
    });
  },
  methods: {
    clearAll() {  // 물품 데이터 전체를 삭제하는 함수
      this.orderList = {};
      this.totalPrice = 0; // 전체 삭제 시 총 금액도 초기화
      this.$store.commit('delAllItem');
      EventBus.$emit('clearAll');
    },

    checkout() {  // 결제하는 기능의 함수
      console.log('결제하기');
      //this.$router.push('/calculateh');
    },

    openDialog() {  // 팝업창을 여는 함수
      this.dialog = true;
    },

    closeDialog() { // 팝업창을 닫는 함수
      this.dialog = false;
      this.dialog1 = false;
      this.dialog2 = false;
    },

    selectOption(option) {
      EventBus.$emit('select-option', option);
    },

    selectPayment(method) {
      console.log('선택한 결제 방식:', method);
      if (method === '카드결제') {
        this.dialog1 = true;
      }
      else if (method === '쿠폰') {
        this.dialog2 = true;
      }
    },
    resetButtons() {
      this.paymentOptionSelected = false;
    },
    
    addToOrder(item) {  // 주문 내역 확인에 물품 데이터를 추가하는 함수
      if (!this.orderList[item.p_name]) {
        this.$set(this.orderList, item.p_name, { count: 0, price: 0, unitPrice: item.p_price });
      }
      this.orderList[item.p_name].count += 1;
      this.orderList[item.p_name].price = this.orderList[item.p_name].unitPrice;
      this.totalPrice += item.p_price; // 물품 추가 시 총 금액도 업데이트
    },

    pay() {
      let selectedItems = this.$store.state.items.map(item => `${item.name}(${item.count}개)`).join(', ');
      alert(`주문내역: ${selectedItems}\n총 금액: ${this.totalPrice}원\n감사합니다. 결제가 완료되었습니다.`);
      this.$store.commit('delAllItem');
      location.href = "http://localhost:8080/";
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
.kiosk-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  max-width: 600px;
  margin: 20px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #f8f8f8;
}

.action-button {
  margin-top: 10px;
  width: 200px;
  height: 50px;
  font-size: 18px;
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

.order-summary {
  max-width: 600px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.order-summary-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
}

.order-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 16px;
  background-color: #eee;
  padding: 10px;
  border-radius: 5px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.item-name,
.item-count,
.item-price {
  flex: 1;
  font-size: 16px;
}

.item-count {
  margin-left: 35px;
  text-align: center;
}

.item-price {
  text-align: right;
  font-weight: bold;
}

.total-price {
  font-size: 18px;
  font-weight: bold;
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 2px solid #3498db;
}

.total-price-label {
  font-size: 16px;
}

.total-price-value {
  font-size: 18px;
  font-weight: bold;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.pay-btn {
  background-color: #4caf50;
  color: #fff;
}

.close-btn {
  background-color: #f44336;
  color: #fff;
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
</style>
