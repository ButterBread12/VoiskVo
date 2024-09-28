<template>
  <div class="kiosk-menu">
    <div class="grid-container">
      <div v-for="item in paginatedItems" :key="item.id" class="grid-item" @click="addToCart(item)">
        <div class="product-info">
          <img :src="item.p_photourl" alt="Product Image" class="product-image" />
          <h2>{{ item.p_name }}</h2>
          <p class="ingredients">{{ item.p_ingredient }}</p>
        </div>
        <div class="item-price" :class="{'discounted': item.p_discount}">
          <div v-if="item.p_discount">
            <span class="original-price">{{ Math.floor(item.p_price) }}원</span>
            <span class="discounted-price">{{ Math.floor(discountedPrice(item)) }}원</span>
          </div>
          <div v-else>
            {{ Math.floor(item.p_price) }}원
          </div>
        </div>
      </div>
    </div>
    <div class="pagination-buttons">
      <v-btn @click="prevPage" color="primary" class="page-btn">이전</v-btn>
      <v-btn @click="nextPage" color="primary" class="page-btn">다음</v-btn>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../main';

export default {
  data() {
    return {
      currentPage: 0,
      itemsPerPage: 12, // 2x6 행렬
      shoppingCart: [],
    };
  },
  computed: {
    paginatedItems() {
      const start = this.currentPage * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.shoppingCart.slice(start, end);
    }
  },
  mounted() {
    EventBus.$on('sendMenuCategory', this.getDataFromServer);
  },
  methods: {
    addToCart(item) {
      if (item.p_division == 'set') {
        this.settingSetMenu(item);
      }
      EventBus.$emit('add-to-cart', item);
    },

    settingSetMenu(item) {
      // alert(`이것은 ${item.p_name}다.`)
    },

    async getDataFromServer(category) {
      try {
        const response = await axios.get(`http://localhost:8000/data/${category}`);
        const data = response.data;
        this.shoppingCart = data;
        console.log('서버에서 받은 데이터:', this.shoppingCart);
      } catch (error) {
        console.error('데이터를 가져오는 중 오류 발생:', error);
      }
    },
    nextPage() {
      if ((this.currentPage + 1) * this.itemsPerPage < this.shoppingCart.length) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
    },
    discountedPrice(item) {
      return item.p_price - (item.p_price * (item.p_discount / 100));
    }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.kiosk-menu {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  font-family: 'Roboto', sans-serif;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  height: 100%;
}

.grid-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.product-info {
  padding: 20px;
  text-align: center;
}

.product-image {
  width: 100%;
  height: auto;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.ingredients {
  margin-top: 10px;
  color: #777;
}

.item-price {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ff6f61;
  color: #fff;
  padding: 15px;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  font-weight: bold;
  margin-top: auto; /* Flexbox를 사용하여 item-price를 아래로 이동 */
}

.original-price {
  text-decoration: line-through;
  color: #999;
  font-size: 14px;
}

.discounted-price {
  font-size: 18px;
  color: #ff0000;
}

.pagination-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-btn {
  padding: 15px 30px;
  margin: 0 10px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease-in-out;
}

.page-btn:hover {
  background-color: #ff6f61;
  color: #fff;
}
</style>