<template>
  <div>
    <menu-category/>
    <menu-c/>
    <v-row>
      <v-col>
        <voiceorder/>
      </v-col>
      <v-col>
        <count/>
      </v-col>
    </v-row>
  </div>
</template>
  
<script>
import MenuC from '../components/Menu.vue'
import voiceorder from '@/components/VoiceOrder.vue'
import Count from '@/components/Count.vue'
import menuCategory from '@/components/menuCategory.vue'
import axios from 'axios';
import { EventBus } from '../main.js';

export default {
  name: 'App',
  components: {
    MenuC,
    voiceorder,
    Count,
    menuCategory
  },
  data() {
    return {
      recognition: null,
    };
  },
  created(){
    //this.speak('주문해주세요');
  },
  mounted() {
    this.startRecognition();
  },
  methods: {
    startRecognition() {
      this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      this.recognition.lang = 'ko-KR';
      this.recognition.start();

      this.recognition.onresult = async (event) => {
        const speechResult = event.results[0][0].transcript.trim();
        console.log('Result:', speechResult);

        const response = await fetch('http://localhost:5001/recognize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ speech: speechResult }),
        });

        //const data = await response.json();
        //console.log('Order data:', data);

        if (speechResult.includes('세트') || speechResult.includes('새트')) {
            EventBus.$emit('sendMenuCategory', 'set')
          } else if (speechResult.includes('단품') || speechResult.includes('햄버거 단품') || speechResult.includes('단풍')) {
            EventBus.$emit('sendMenuCategory', 'burger')
          } else if (speechResult.includes('사이드')) {
            EventBus.$emit('sendMenuCategory', 'side')
          } else if (speechResult.includes('음료') || speechResult.includes('음요')) {
            EventBus.$emit('sendMenuCategory', 'drink')
          } else if (speechResult.includes('결제') || speechResult.includes('골랐어')) {
            EventBus.$emit('openWindow')
          } else if (speechResult.includes('전체 삭제')) {
            EventBus.$emit('deleteOrder')
          } else if (speechResult.includes('이전')) {
            EventBus.$emit('prev')
          } else if (speechResult.includes('다음')) {
            EventBus.$emit('next')
          } else if (speechResult.includes('더블 불고기 버거') || speechResult.includes('더블불고기버거')) {
            this.speechItem('더블 불고기 버거')
          } else if (speechResult.includes('슈슈 버거') || speechResult.includes('슈슈버거')) {
            this.speechItem('슈슈 버거')
          } else if (speechResult.includes('더블 빅맥')) {
            this.speechItem('더블 빅맥');
          } else if (speechResult.includes('빅맥 BLT')) {
            this.speechItem('빅맥® BLT');
          } else if (speechResult.includes('더블 쿼터파운더 치즈버거')) {
            this.speechItem('더블 쿼터파운더® 치즈');
          } else if (speechResult.includes('쿼터파운더 치즈버거')) {
            this.speechItem('쿼터파운더® 치즈 세트버거');
          } else if (speechResult.includes('맥크리스피 디럭스 버거')) {
            this.speechItem('맥크리스피™ 디럭스 버거 세트');
          } else if (speechResult.includes('맥크리스피 클래식 버거')) {
            this.speechItem('맥크리스피™ 클래식 버거');
          } else if (speechResult.includes('트리플 치즈 버거')) {
            this.speechItem('트리플 치즈 버거');
          } else if (speechResult.includes('맥스파이시 상하이 버거')) {
            this.speechItem('맥스파이시® 상하이 버거');
          } else if (speechResult.includes('1955 버거')) {
            this.speechItem('1955® 버거');
          } else if (speechResult.includes('맥치킨 모짜렐라 버거')) {
            this.speechItem('맥치킨® 모짜렐라');
          } else if (speechResult.includes('맥치킨')) {
            this.speechItem('맥치킨®');
          } else if (speechResult.includes('에그 불고기 버거')) {
            this.speechItem('에그 불고기 버거');
          } else if (speechResult.includes('불고기 버거 두 개') || speechResult.includes('불고기버거 두 개')) {
            this.speechItem('불고기 버거', 2);
          } else if (speechResult.includes('불고기 버거 세 개') || speechResult.includes('불고기버거 세 개')) {
            this.speechItem('불고기 버거', 3);
            this.speak('불고기 버거 세개를 담았습니다.');
          } else if (speechResult.includes('불고기 버거') || speechResult.includes('불고기버거')) {
            this.speechItem('불고기 버거');
          } else if (speechResult.includes('슈비 버거')) {
            this.speechItem('슈비 버거');
          } else if (speechResult.includes('베이컨 토마토 디럭스')) {
            this.speechItem('베이컨 토마토 디럭스');
          } else if (speechResult.includes('치즈버거')) {
            this.speechItem('치즈버거');
          } else if (speechResult.includes('더블 치즈버거')) {
            this.speechItem('더블 치즈버거');
          } else if (speechResult.includes('햄버거')) {
            this.speechItem('햄버거');
          } else if (speechResult.includes('매장')) {
            EventBus.$emit('select-option', '매장')
            this.speak('매장을 골랐습니다');
          } else if (speechResult.includes('포장')) {
            EventBus.$emit('select-option', '포장')
          } else if (speechResult.includes('카드')) {
            EventBus.$emit('select-payment', '카드결제');
            this.speak('카드로 결제하겠습니다');
          } else if (speechResult.includes('쿠폰')) {
            EventBus.$emit('select-payment', '쿠폰결제');
          } else {
            this.speak('다시한번 말해주세요');
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
    async speechItem(item, cnt=1) {  // 음성인식으로 물품 고를때 이 함수 사용 (코드 수 감소)
      const response = await axios.get(`http://localhost:8000/price/${item}`);
      const data = {p_name: item, p_price: response.data};
      EventBus.$emit('add-to-cart', data);
      console.log('cnt:', cnt)
      EventBus.$emit('itemCount', {name: item, count: cnt-1});
    },
    speak(message) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = 'ko-KR';
      window.speechSynthesis.speak(utterance);
    },
  }
}
  
</script>