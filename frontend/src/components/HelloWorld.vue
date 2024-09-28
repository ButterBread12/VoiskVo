<template>
  <v-app id="app">
    <div class="button-container">
      <v-btn @click="goToOrder" class="action-button" color="primary" dark>일반 주문</v-btn>
      <v-btn @click="goToVoice" class="action-button" color="success" dark>음성 주문</v-btn>
    </div>
  </v-app>
</template>

<script>
export default {
  methods: {
    goToOrder() {
      this.$router.push('/about');
    },
    goToVoice() {
      this.$router.push('/voice');
    },
  }
}
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.action-button {
  width: 150px; 
  height: 150px;
  margin: 0 10px;
}
</style>
