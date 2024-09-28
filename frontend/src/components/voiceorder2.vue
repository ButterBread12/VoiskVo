<template>
  <div class="order-container">
    <h1>주문 목록</h1>
    <ul>
      <li v-for="item in orderList" :key="item.name" class="order-item">
        <span class="item-name">{{ item.name }}</span>
        <span class="item-quantity">{{ item.quantity }}</span>
        <span class="item-price">{{ item.price }}원</span>
        <button @click="removeItem(item.name)">삭제</button>
      </li>
    </ul>
    <div class="total-price">총 가격: {{ totalPrice }}원</div>
    <button @click="clearOrderList">전체 삭제</button>
    <button @click="placeOrder">주문하기</button>
    <button @click="startRecognition">음성 인식</button>
  </div>
</template>

<script>
import { EventBus } from '../main.js';
export default {
  data() {
    return {
      orderList: [],
      recognition: null,
    };
  },
  mounted() {
    this.startRecognition();
  },
  computed: {
    totalPrice() {
      return this.orderList.reduce((acc, item) => acc + item.price * item.quantity, 0);
    },
  },
  methods: {
    removeItem(name) {
      this.orderList = this.orderList.filter(item => item.name !== name);
    },
    clearOrderList() {
      this.orderList = [];
    },
    placeOrder() {
      // 주문 로직 추가
    },
    addItemToOrder(itemName, itemPrice, itemCount) {
      const existingItem = this.orderList.find(item => item.name === itemName);
      if (existingItem) {
        existingItem.quantity += itemCount;
      } else {
        this.orderList.push({ name: itemName, quantity: itemCount, price: itemPrice });
      }
    },
    startRecognition() {
      this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      this.recognition.lang = 'ko-KR';
      this.recognition.start();

      this.recognition.onresult = async (event) => {
        const speechResult = event.results[0][0].transcript;
        console.log('Result:', speechResult);

        const response = await fetch('http://localhost:5001/recognize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ speech: speechResult }),
        });

        const data = await response.json();
        console.log('Order data:', data);

        if (data.item === '더블 불고기 버거') {
          if (data.type === 'add') {
            this.addItemToOrder(data.item, 5400, data.count);
            EventBus.$emit('openWindow');
          } else if (data.type === 'new') {
            this.addItemToOrder(data.item, 5400, data.count);
            EventBus.$emit('openWindow');
          }
        }
      };

      this.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event);
      };

      // 음성 인식이 종료될 때 다시 시작
      this.recognition.onend = () => {
        this.recognition.start();
      };
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
