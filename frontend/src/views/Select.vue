<template>
  <v-container fill-height fluid>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4 text-xs-center>
        <h1>취식 방법 선택</h1>
        <v-btn large @click="selectInStore" class="action-button mr-3" color="primary" dark>매장 식사</v-btn>
        <v-btn large @click="selectTakeout" class="action-button ml-3" color="success" dark>포장 주문</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  methods: {
    selectInStore() {
      this.$router.push('/home');
    },
    selectTakeout() {
      this.$router.push('/home');
    }
  }
}
</script>

<style scoped>
.action-button {
  margin-top: 20px; /* 위 아래 간격 */
}
.mr-3 {
  margin-right: 1rem; /* 오른쪽 간격 */
}
.ml-3 {
  margin-left: 1rem; /* 왼쪽 간격 */
}
</style>
