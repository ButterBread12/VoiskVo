<template>
  <div class="kiosk-buttons">
    <v-btn @click="clearAll" class="action-button" color="primary" dark>전체삭제</v-btn>
    <v-btn @click="addContact" class="action-button" color="success" dark>{{ totalPrice }}원 결제하기</v-btn>
    <v-dialog v-model="dialog">
      <!-- 팝업 창 내용 시작 -->
      <v-card>
        <v-card-title>주문 방식 선택</v-card-title>
        <v-card-text>
          <!-- 팝업 창의 내용을 이곳에 추가하세요 -->
          <!-- 예시로 간단한 텍스트 추가 -->
          주문 방식을 선택해주세요.
        </v-card-text>
        <li v-for="(item, itemName) in orderList" :key="itemName" class="order-item">
        <div class="item-name">{{ itemName }}</div>
        <div class="item-price">{{ item.price * item.count }}원</div>
      </li>
        <v-card-actions>
          <v-btn @click="closeDialog" color="primary" dark>닫기</v-btn>
        </v-card-actions>
      </v-card>
      <!-- 팝업 창 내용 끝 -->
    </v-dialog>
  </div>

  
</template>

<script>
import { EventBus } from '../main.js';
export default {
  data() {
    return {
      orderList: {},   // 주문 목록을 저장하는 객체
      totalPrice: 0,   // 총 가격
      dialog: false,   // 다이얼로그의 표시 여부를 관리하는 변수
    };
  },
  created() {
    //EventBus.$on('add-to-cart', this.addToOrder);
  },
  mounted() {
    // 이벤트 버스에서 발생한 이벤트에 대한 리스너 등록
    EventBus.$on('totalPriceUpdated', this.updateTotalPrice);
    EventBus.$on('add-to-cart', this.addToOrder);
    EventBus.$on('sendList', () => {this.orderList}); // 이벤트를 통해 주문 목록을 전송
  },
  methods: {
    clearAll() {
      // 이벤트를 통해 전체 삭제를 알림
      EventBus.$emit('clearAll');
    },
    checkout() {
      console.log('결제하기');
      //this.$router.push('/calculateh');
    },
    updateTotalPrice(newPrice) {
      // 총 가격 업데이트
      this.totalPrice = newPrice;
    },
    addContact() {
      // 다이얼로그 표시
      this.dialog = true;
    },
    closeDialog() {
      // 다이얼로그 닫기
      this.dialog = false;
    },
    addToOrder(item) {
      // 주문 목록에 상품 추가
      if (!this.orderList[item.p_name]) {
        this.$set(this.orderList, item.p_name, { count: 0, price: 0, unitPrice: item.p_price });
      }
      this.orderList[item.p_name].count += 1;
      this.orderList[item.p_name].price = this.orderList[item.p_name].unitPrice;
      console.log("성곤!!!!!")
    },
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
</style>