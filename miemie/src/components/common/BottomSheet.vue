<template>
  <v-bottom-sheet v-model="showWarning">
    <v-sheet class="text-center pa-6" height="200px">
      <div :class="{ 'classic-font': useClassicFont }">
        咩咩估价是由玩家开发，用于剑网3游戏账号价格估计的游戏辅助工具，所提供价格估计仅供参考。咩咩估价暂时只支持
        两千元 以上账号的游戏账号估价。
      </div>
      <v-btn
        class="mt-6 white-font"
        color="indigo darken-3"
        @click="showWarning = !showWarning"
      ><span :class="{ 'classic-font': useClassicFont }">我已知晓</span></v-btn>
    </v-sheet>
  </v-bottom-sheet>   
</template>


<script>
  import { mapGetters } from 'vuex'

  export default {
    data () {
      return {
        showWarning: true,
      }
    },
    computed: {
      ...mapGetters(['useClassicFont']),
    },
  }
</script>