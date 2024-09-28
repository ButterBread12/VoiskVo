<template>
    <section>
      <ul class="category-list">
        <li v-for="(category, index) in categories" :key="index">
          <v-btn x-large @click="openMenu(category.division)" color="primary" class="category-item">{{ category.name }}</v-btn>
        </li>
      </ul>
    </section>
</template>
  
<script>
import { EventBus } from '../main';
  export default {
    data() {
      return {
        categories: [
          { name: '세트',
            division: 'set' },
          { name: '버거',
            division: 'burger' },
          { name: '사이드',
            division: 'side' },
          { name: '음료',
            division: 'drink' },
        ],
      };
    },
    methods: {
      openMenu(category) {
        EventBus.$emit('sendMenuCategory', category);
        console.log('보낸 카테고리: ', category)
      },
    }
  };
</script>
  
<style scoped>

.category-list {
  /* 카테고리 목록 스타일 */
  display: flex;
  justify-content: center;
  list-style-type: none;
  padding: 0;
}

.category-item {
  /* 카테고리 버튼 스타일 */ 
  flex: 1;
  width: 23.5em;
  user-select: none; /* 텍스트 드래그 방지 */
  margin-right: 0.1em;
}
</style>