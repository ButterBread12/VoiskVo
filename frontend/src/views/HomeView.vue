<template>
  <!--<div class="payment-complete">
    <h1>결제가 완료되었습니다.</h1>
  </div>-->
  <hello-world/>
</template>

<script>
  import HelloWorld from '../components/HelloWorld'

  export default {
    name: 'Home',

    components: {
      HelloWorld,
    },
  }
</script>

<style>
.payment-complete {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

h1 {
  font-size: 24px;
  color: #333;
  text-align: center;
}
</style>