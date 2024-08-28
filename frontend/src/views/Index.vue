<script setup>
import {
  NInput, NButton, NCard, NDatePicker, NSelect, NFormItem,
  NInputNumber, NTabs, NTabPane, NDrawer, NDrawerContent,
  createDiscreteApi
} from 'naive-ui'
import { watch, ref, onMounted } from "vue";
import MarkdownIt from 'markdown-it';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { useStorage } from '@vueuse/core';
import { Solar } from 'lunar-javascript'

import { useIsMobile } from '../utils/composables'
import About from '../components/About.vue'

import { DIVINATION_OPTIONS } from "../config/constants";

const isMobile = useIsMobile()

// 创建独立的通知 API
const { notification } = createDiscreteApi(['notification'])

const state_jwt = useStorage('jwt')
const prompt = ref("");
const result = useStorage("result", ""); // 用于存储占卜结果
const tmp_result = ref("");
const prompt_type = useStorage("prompt_type", "tarot-3");
const menu_type = useStorage("menu_type", "divination");
const lunarBirthday = ref("");
const birthday = useStorage("birthday", "2000-08-17 00:00:00");
const loading = ref(false);
const API_BASE = import.meta.env.VITE_API_BASE || "";
const md = new MarkdownIt();
const showDrawer = ref(false);
const showResultButtonEnabled = ref(false); // 控制"点击打开占卜结果页面"按钮的可用状态
const sex = ref("")
const surname = ref("")
const new_name_prompt = ref("")
const sexOptions = [
  { label: "男", value: "男" },
  { label: "女", value: "女" },
]
const plum_flower = useStorage("plum_flower", { num1: 0, num2: 0 })
const fate_body = useStorage("fate_body", { name1: "", name2: "" })

const selectedTarotCards = ref([]); // 记录选择的塔罗牌

// 卡片数据初始化时不带 orientation
const tarotCards = ref([
   { name: '愚者', imageFront: '/cards/the-fool.png', imageBack: '/cards/back.png' },
  { name: '魔术师', imageFront: '/cards/the-magician.png', imageBack: '/cards/back.png' },
  { name: '女祭司', imageFront: '/cards/the-high-priestess.png', imageBack: '/cards/back.png' },
  { name: '皇后', imageFront: '/cards/the-empress.png', imageBack: '/cards/back.png' },
  { name: '皇帝', imageFront: '/cards/the-emperor.png', imageBack: '/cards/back.png' },
  { name: '教皇', imageFront: '/cards/the-hierophant.png', imageBack: '/cards/back.png' },
  { name: '恋人', imageFront: '/cards/the-lovers.png', imageBack: '/cards/back.png' },
  { name: '战车', imageFront: '/cards/the-chariot.png', imageBack: '/cards/back.png' },
  { name: '力量', imageFront: '/cards/strength.png', imageBack: '/cards/back.png' },
  { name: '隐者', imageFront: '/cards/the-hermit.png', imageBack: '/cards/back.png' },
  { name: '命运之轮', imageFront: '/cards/wheel-fortune.png', imageBack: '/cards/back.png' },
  { name: '正义', imageFront: '/cards/justice.png', imageBack: '/cards/back.png' },
  { name: '倒吊人', imageFront: '/cards/the-hanged-man.png', imageBack: '/cards/back.png' },
  { name: '死神', imageFront: '/cards/death.png', imageBack: '/cards/back.png' },
  { name: '节制', imageFront: '/cards/temperance.png', imageBack: '/cards/back.png' },
  { name: '恶魔', imageFront: '/cards/the-devil.png', imageBack: '/cards/back.png' },
  { name: '高塔', imageFront: '/cards/the-tower.png', imageBack: '/cards/back.png' },
  { name: '星星', imageFront: '/cards/the-star.png', imageBack: '/cards/back.png' },
  { name: '月亮', imageFront: '/cards/the-moon.png', imageBack: '/cards/back.png' },
  { name: '太阳', imageFront: '/cards/the-sun.png', imageBack: '/cards/back.png' },
  { name: '审判', imageFront: '/cards/judgement.png', imageBack: '/cards/back.png' },
  { name: '世界', imageFront: '/cards/the-world.png', imageBack: '/cards/back.png' },

  { name: '权杖首牌', imageFront: '/cards/small/quan-zhang-shou-pai.png', imageBack: '/cards/back.png' },
  { name: '权杖二', imageFront: '/cards/small/quan-zhang-2.png', imageBack: '/cards/back.png' },
  { name: '权杖三', imageFront: '/cards/small/quan-zhang-3.png', imageBack: '/cards/back.png' },
  { name: '权杖四', imageFront: '/cards/small/quan-zhang-4.png', imageBack: '/cards/back.png' },
  { name: '权杖五', imageFront: '/cards/small/quan-zhang-5.png', imageBack: '/cards/back.png' },
  { name: '权杖六', imageFront: '/cards/small/quan-zhang-6.png', imageBack: '/cards/back.png' },
  { name: '权杖七', imageFront: '/cards/small/quan-zhang-7.png', imageBack: '/cards/back.png' },
  { name: '权杖八', imageFront: '/cards/small/quan-zhang-8.png', imageBack: '/cards/back.png' },
  { name: '权杖九', imageFront: '/cards/small/quan-zhang-9.png', imageBack: '/cards/back.png' },
  { name: '权杖十', imageFront: '/cards/small/quan-zhang-10.png', imageBack: '/cards/back.png' },
  { name: '权杖侍从', imageFront: '/cards/small/quan-zhang-shi-cong.png', imageBack: '/cards/back.png' },
  { name: '权杖骑士', imageFront: '/cards/small/quan-zhang-qi-shi.png', imageBack: '/cards/back.png' },
  { name: '权杖皇后', imageFront: '/cards/small/quan-zhang-huang-hou.png', imageBack: '/cards/back.png' },
  { name: '权杖国王', imageFront: '/cards/small/quan-zhang-guo-wang.png', imageBack: '/cards/back.png' },


  { name: '圣杯首牌', imageFront: '/cards/small/sheng-bei-shou-pai.png', imageBack: '/cards/back.png' },
  { name: '圣杯二', imageFront: '/cards/small/sheng-bei-2.png', imageBack: '/cards/back.png' },
  { name: '圣杯三', imageFront: '/cards/small/sheng-bei-3.png', imageBack: '/cards/back.png' },
  { name: '圣杯四', imageFront: '/cards/small/sheng-bei-4.png', imageBack: '/cards/back.png' },
  { name: '圣杯五', imageFront: '/cards/small/sheng-bei-5.png', imageBack: '/cards/back.png' },
  { name: '圣杯六', imageFront: '/cards/small/sheng-bei-6.png', imageBack: '/cards/back.png' },
  { name: '圣杯七', imageFront: '/cards/small/sheng-bei-7.png', imageBack: '/cards/back.png' },
  { name: '圣杯八', imageFront: '/cards/small/sheng-bei-8.png', imageBack: '/cards/back.png' },
  { name: '圣杯九', imageFront: '/cards/small/sheng-bei-9.png', imageBack: '/cards/back.png' },
  { name: '圣杯十', imageFront: '/cards/small/sheng-bei-10.png', imageBack: '/cards/back.png' },
  { name: '圣杯侍从', imageFront: '/cards/small/sheng-bei-shi-cong.png', imageBack: '/cards/back.png' },
  { name: '圣杯骑士', imageFront: '/cards/small/sheng-bei-qi-shi.png', imageBack: '/cards/back.png' },
  { name: '圣杯皇后', imageFront: '/cards/small/sheng-bei-huang-hou.png', imageBack: '/cards/back.png' },
  { name: '圣杯国王', imageFront: '/cards/small/sheng-bei-guo-wang.png', imageBack: '/cards/back.png' },

  { name: '宝剑首牌', imageFront: '/cards/small/bao-jian-shou-pai.png', imageBack: '/cards/back.png' },
  { name: '宝剑二', imageFront: '/cards/small/bao-jian-2.png', imageBack: '/cards/back.png' },
  { name: '宝剑三', imageFront: '/cards/small/bao-jian-3.png', imageBack: '/cards/back.png' },
  { name: '宝剑四', imageFront: '/cards/small/bao-jian-4.png', imageBack: '/cards/back.png' },
  { name: '宝剑五', imageFront: '/cards/small/bao-jian-5.png', imageBack: '/cards/back.png' },
  { name: '宝剑六', imageFront: '/cards/small/bao-jian-6.png', imageBack: '/cards/back.png' },
  { name: '宝剑七', imageFront: '/cards/small/bao-jian-7.png', imageBack: '/cards/back.png' },
  { name: '宝剑八', imageFront: '/cards/small/bao-jian-8.png', imageBack: '/cards/back.png' },
  { name: '宝剑九', imageFront: '/cards/small/bao-jian-9.png', imageBack: '/cards/back.png' },
  { name: '宝剑十', imageFront: '/cards/small/bao-jian-10.png', imageBack: '/cards/back.png' },
  { name: '宝剑侍从', imageFront: '/cards/small/bao-jian-shi-cong.png', imageBack: '/cards/back.png' },
  { name: '宝剑骑士', imageFront: '/cards/small/bao-jian-qi-shi.png', imageBack: '/cards/back.png' },
  { name: '宝剑皇后', imageFront: '/cards/small/bao-jian-huang-hou.png', imageBack: '/cards/back.png' },
  { name: '宝剑国王', imageFront: '/cards/small/bao-jian-guo-wang.png', imageBack: '/cards/back.png' },

  { name: '钱币首牌', imageFront: '/cards/small/qian-bi-shou-pai.png', imageBack: '/cards/back.png' },
  { name: '钱币二', imageFront: '/cards/small/qian-bi-2.png', imageBack: '/cards/back.png' },
  { name: '钱币三', imageFront: '/cards/small/qian-bi-3.png', imageBack: '/cards/back.png' },
  { name: '钱币四', imageFront: '/cards/small/qian-bi-4.png', imageBack: '/cards/back.png' },
  { name: '钱币五', imageFront: '/cards/small/qian-bi-5.png', imageBack: '/cards/back.png' },
  { name: '钱币六', imageFront: '/cards/small/qian-bi-6.png', imageBack: '/cards/back.png' },
  { name: '钱币七', imageFront: '/cards/small/qian-bi-7.png', imageBack: '/cards/back.png' },
  { name: '钱币八', imageFront: '/cards/small/qian-bi-8.png', imageBack: '/cards/back.png' },
  { name: '钱币九', imageFront: '/cards/small/qian-bi-9.png', imageBack: '/cards/back.png' },
  { name: '钱币十', imageFront: '/cards/small/qian-bi-10.png', imageBack: '/cards/back.png' },
  { name: '钱币侍从', imageFront: '/cards/small/qian-bi-shi-cong.png', imageBack: '/cards/back.png' },
  { name: '钱币骑士', imageFront: '/cards/small/qian-bi-qi-shi.png', imageBack: '/cards/back.png' },
  { name: '钱币皇后', imageFront: '/cards/small/qian-bi-huang-hou.png', imageBack: '/cards/back.png' },
  { name: '钱币国王', imageFront: '/cards/small/qian-bi-guo-wang.png', imageBack: '/cards/back.png' },

]);

const getRandomOrientation = () => {
  return Math.random() > 0.5 ? '正位' : '逆位';
};

const shuffleCards = () => {
  tarotCards.value = tarotCards.value.map(card => ({
    ...card,
    orientation: null, // 每次洗牌时清除 orientation
    flipped: false // 确保所有卡片重置为未翻转状态
  })).sort(() => Math.random() - 0.5);
  selectedTarotCards.value = []; // 清空已选择的牌
  showResultButtonEnabled.value = false; // 禁用"点击打开占卜结果页面"按钮
  drawer_closable.value = true; // 请求结束后重置为false
  
  // 添加洗牌成功的通知
  notification.success({
    title: '洗牌成功',
    content: `卡牌已经重新洗混,请重新选择${prompt_type.value === 'tarot-venus' ? '八张' : '三张'}卡片。`,
    duration: 3000
  });
};

const shuffleCardsWithoutNotification = () => {
  tarotCards.value = tarotCards.value.map(card => ({
    ...card,
    orientation: null, // 每次洗牌时清除 orientation
    flipped: false // 确保所有卡片重置为未翻转状态
  })).sort(() => Math.random() - 0.5);
  selectedTarotCards.value = []; // 清空已选择的牌
  showResultButtonEnabled.value = false; // 禁用"点击打开占卜结果页面"按钮
};

const selectCard = (card) => {
  const maxSelection = prompt_type.value === 'tarot-venus' ? 8 : 3;
  if (selectedTarotCards.value.find(selectedCard => selectedCard.name === card.name)) {
    return; // 如果已经选择过该牌，不进行任何操作
  }

  if (selectedTarotCards.value.length < maxSelection) {
    // 点击时随机生成 orientation，并将卡片加入选中数组
    const orientation = getRandomOrientation();
    selectedTarotCards.value.push({
      ...card,
      orientation
    });

    // 更新卡片的 orientation 和翻转状态
    card.orientation = orientation;
    card.flipped = true;

    // 添加选牌成功的通知
    notification.info({
      title: '选择卡片',
      content: `你选择了 ${card.name} (${orientation})`,
      duration: 2000
    });

    // 如果选够了指定张数的牌，显示一个通知
    if (selectedTarotCards.value.length === maxSelection) {
      notification.success({
        title: '选牌完成',
        content: `你已经选择了${maxSelection}张卡片，可以开始占卜了。`,
        duration: 3000
      });
    }
  }
};

const drawer_closable = ref(true);

const handleDrawerUpdate = async(value) => {
  if(drawer_closable == false){
    showDrawer.value = true;
  }
}

const onSubmit = async () => {
  notification.success({
        title: '提交成功',
        content: `所选卡片已提交，请稍后...`,
        duration: 1000
      });
  try {
    drawer_closable.value = false; // 开始请求时设置为true
    loading.value = true;
    showResultButtonEnabled.value = false; // 占卜进行中禁用"点击打开占卜结果页面"按钮
    result.value = "占卜中，请稍后..."; // 显示占卜中的提示
    tmp_result.value = "";
    const selectedCardNames = selectedTarotCards.value.map(card => ({
      name: card.name,
      orientation: card.orientation
    }));

    // 添加开始占卜的通知
    notification.info({
      title: '开始占卜',
      content: '正在进行占卜，请稍候...',
      duration: 0 // 设置为 0 表示不自动关闭
    });

    // 构造请求体数据
  const requestBody = {
    prompt: prompt.value || "我的财务状况如何",
    prompt_type: prompt_type.value,
    birthday: birthday.value,
    selected_cards: selectedCardNames, // 发送选择的塔罗牌
    new_name: {
      surname: surname.value,
      sex: sex.value,
      birthday: birthday.value,
      new_name_prompt: new_name_prompt.value
    },
    plum_flower: prompt_type.value === "plum_flower" ? plum_flower.value : null,
    fate: prompt_type.value === "fate" ? fate_body.value : null
  };

  // 如果 prompt_type 以 "tarot" 开头，则添加特定的牌阵字段
  if (prompt_type.value.startsWith("tarot")) {
    // 使用 find 方法通过 tabName 匹配 DIVINATION_OPTIONS 中的 label
    const matchingOption = DIVINATION_OPTIONS.find(option => option.key === prompt_type.value);

    // 如果找到了匹配项，则显示对应的 label，否则显示 tabName
    const label = matchingOption ? matchingOption.label : prompt_type.value;
    requestBody.tarot_spread = label; // 例如，selectedSpreadName 表示具体的牌阵名称
    requestBody.prompt_type = "tarot"
  }

    await fetchEventSource(`${API_BASE}/api/divination`, {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: {
        "Authorization": `Bearer ${state_jwt.value || "xxx"}`,
        "Content-Type": "application/json"
      },
      async onopen(response) {
        if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
          return;
        } else if (response.status >= 400 && response.status < 500) {
          throw new Error(`${response.status} ${await response.text()}`);
        }
      },
      onmessage(msg) {
        if (msg.event === 'FatalError') {
          throw new FatalError(msg.data);
        }
        if (!msg.data) {
          return;
        }
        try {
          tmp_result.value += JSON.parse(msg.data);
          result.value = md.render(tmp_result.value); // 接收数据后显示实际结果
          showResultButtonEnabled.value = true; // 占卜完成后启用"点击打开占卜结果页面"按钮
        } catch (error) {
          console.error(error);
        }
      },
      onclose() {
        // 占卜完成，关闭之前的通知，显示新的通知
        notification.destroyAll();
        notification.success({
          title: '占卜完成',
          content: '点击"打开占卜结果页面"按钮查看结果。',
          duration: 5000
        });
      },
      onerror(err) {
        result.value = `占卜失败: ${err.message}`;
        // 占卜失败，显示错误通知
        notification.destroyAll();
        notification.error({
          title: '占卜失败',
          content: '请稍后重试。',
          duration: 5000
        });
        throw new Error(`占卜失败: ${err.message}`);
      }
    });
  } catch (error) {
    console.error(error);
    result.value = error.message || "占卜失败";
  } finally {
    loading.value = false;
    drawer_closable.value = true; // 请求结束后重置为false
  }
};

const computeLunarBirthday = (newBirthday) => {
  try {
    let date = new Date(newBirthday)
    let solar = Solar.fromYmdHms(
      date.getFullYear(), date.getMonth() + 1, date.getDate(),
      date.getHours(), date.getMinutes(), date.getSeconds());
    lunarBirthday.value = solar.getLunar().toFullString();
  } catch (error) {
    console.error(error)
    lunarBirthday.value = '转换失败'
  }
}

watch(birthday, async (newBirthday, oldBirthday) => {
  computeLunarBirthday(newBirthday)
})

const changeTab = async (delta) => {
  let curIndex = DIVINATION_OPTIONS.findIndex((option) => option.key === prompt_type.value);
  let newIndex = curIndex + delta;
  if (newIndex < 0) {
    newIndex = DIVINATION_OPTIONS.length - 1;
  } else if (newIndex >= DIVINATION_OPTIONS.length) {
    newIndex = 0;
  }
  prompt_type.value = DIVINATION_OPTIONS[newIndex].key;
}

const handleBeforeLeaveTab = async (tabName) => {
  // 使用 find 方法通过 tabName 匹配 DIVINATION_OPTIONS 中的 label
  const matchingOption = DIVINATION_OPTIONS.find(option => option.key === tabName);

  // 如果找到了匹配项，则显示对应的 label，否则显示 tabName
  const label = matchingOption ? matchingOption.label : tabName;

  

  try{
    const rule = matchingOption.rule

    shuffleCardsWithoutNotification();
      // 显示通知
      notification.success({
        title: '切换完成',
        content: '当前牌组：' + label + ', 占卜结果和牌组已重置。\n\n占卜规则：' + rule,
        duration: 5000
      });
  }catch(error){

  }
  

  return true;
}

onMounted(async () => {
  shuffleCards(); // 页面加载时自动洗牌
  computeLunarBirthday(birthday.value);



  shuffleCardsWithoutNotification();

  try{
       // 使用 find 方法通过 tabName 匹配 DIVINATION_OPTIONS 中的 label
  const matchingOption = DIVINATION_OPTIONS.find(option => option.key === prompt_type.value);

  // 如果找到了匹配项，则显示对应的 label，否则显示 tabName
  const label = matchingOption ? matchingOption.label : prompt_type.value;

    const rule = matchingOption.rule

    // 显示通知
    notification.success({
      title: '占卜规则',
      content: '当前牌组：' + label + ', \n\n占卜规则：' + rule,
      duration: 10000
    });
  } catch(error){

  }
 
});
</script>

<template>
  <div>
    <n-tabs v-model:value="prompt_type" type="card" animated placement="top" @before-leave="handleBeforeLeaveTab">
      <template v-if="isMobile" #prefix>
        <n-button @click="changeTab(-1)">←</n-button>
      </template>
      <template v-if="isMobile" #suffix>
        <n-button @click="changeTab(1)">→</n-button>
      </template>
      <n-tab-pane v-for="option in DIVINATION_OPTIONS" :name="option.key" :tab="option.label">
        <n-card v-if="prompt_type != 'about'">
          <div v-if="prompt_type == 'tarot-3' || prompt_type == 'tarot-venus'">
            <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 3 }"
              placeholder="我的财务状况如何" />
            <div class="tarot-cards">
              <div v-for="card in tarotCards" :key="card.name" class="tarot-card" 
                   @click="selectCard(card)" :class="{ flipped: card.flipped }">
                <div class="card-inner" :style="{ transform: card.flipped ? (card.orientation === '逆位' ? 'rotateY(180deg) rotate(180deg)' : 'rotateY(180deg)') : 'none' }">
                  <div class="card-front">
                    <img :src="card.imageFront" alt="tarot card front" />
                  </div>
                  <div class="card-back">
                    <img :src="card.imageBack" alt="tarot card back" />
                  </div>
                </div>
              </div>
            </div>
            <div class="shuffle-button">
              <n-button @click="shuffleCards">洗牌</n-button>
            </div>
          </div>
          <!-- 其他占卜方式省略 -->
          <div v-if="menu_type != 'about'" class="button-container">
            <n-button class="button" @click="showDrawer = !showDrawer" tertiary type="primary" :disabled="!showResultButtonEnabled">
              点击打开占卜结果页面
            </n-button>
            <n-button class="button" @click="onSubmit" type="primary" :disabled="loading || selectedTarotCards.length !== (prompt_type === 'tarot-venus' ? 8 : 3) || showResultButtonEnabled">
              {{ loading ? "正在占卜中..." : "占卜" }}
            </n-button>
          </div>
        </n-card>
      </n-tab-pane>
      <n-tab-pane name="about" tab="关于">
        <About />
      </n-tab-pane>
    </n-tabs>
    <n-drawer v-model:show="showDrawer" style="height: 80vh;" placement="bottom" :trap-focus="false"
      :block-scroll="false" @update:show="handleDrawerUpdate">
      <n-drawer-content title="占卜结果" closable>
        <div class="result" v-html="result"></div>
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<style scoped>
.button-container {
  display: flex;
  justify-content: center;
}

.button {
  margin: 10px;
}

.result {
  text-align: left;
}

.tarot-cards {
  display: flex;
  flex-wrap: wrap; /* 使卡片容器支持换行 */
  justify-content: center;
  gap: 15px; /* 增加牌间距 */
  margin-top: 20px;
}

.tarot-card {
  width: 100px;
  height: 150px;
  cursor: pointer;
  perspective: 1000px; /* 添加3D翻转效果 */
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

.tarot-card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 4px; /* 添加圆角 */
}

.card-front {
  transform: rotateY(180deg); /* 正面图像初始状态为旋转180度 */
}

.card-back img,
.card-front img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tarot-card.flipped .card-front img {
  box-shadow: 0 0 15px 5px #ffd700; /* 减小光效 */
  animation: glow 1.5s infinite; /* 动态金光效果 */
}

@keyframes glow {
  0% {
    box-shadow: 0 0 15px 5px #ffd700;
  }
  50% {
    box-shadow: 0 0 20px 8px #ffae00;
  }
  100% {
    box-shadow: 0 0 15px 5px #ffd700;
  }
}

.shuffle-button {
  margin-top: 20px;
  text-align: center;
}
</style>
