<template>
    <v-card class="pa-0 fill-height main-card">
      <v-container fluid class="pa-0 fill-height">
          <v-row class="fill-width ma-0 pa-0 mb-12" justify="center" >
              <v-dialog v-model="dialog" persistent max-width="400">
                <v-card>
                  <v-card-title class="headline">问题回答</v-card-title>
                  <v-card-text>
                    <p class="text-16 font-weight-black">1. 为什么我加了红年轮/ 脚气马/ 里飞沙价格反而变低了呢？</p>
                    <p>咩咩估价只能获取大致的价格范围，不会特别精确，毕竟是人工智能模型（通俗地说）自动算的……我也不知道人工智障是怎么想的！目前还是娱乐为主</p>
                    <p class="text-16 font-weight-black">2. 为什么我的白板号都能有2000块？</p>
                    <p>因为2000以下的号，和2000以上的号，价格构成比例差别很大。在几百元、一千元这个级别的选手，装备、拓印占了比较大的比重，而这些在当前的咩咩估价里面没有做很多的考虑。</p>
                    <p>为了追求更高的准确度，当前的咩咩估价抛弃了2000元以下的账号数据，只参考了2000元以上的账号数据，所以会出现这种“白板号都有2000块的现象”。</p>
                    <p class="text-16 font-weight-black">3. 向作者提意见</p>
                    <p>QQ群: <a target="_blank" href="https://jq.qq.com/?_wv=1027&k=5LGp6kl">284973854</a></p>
                    <p>百度贴吧: <a href="https://tieba.baidu.com/p/6401209068">https://tieba.baidu.com/p/6401209068</a></p>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="indigo darken-1" text @click="dialog = false">好的</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-col cols="12" sm="10" md="7" class="pa-2" v-if="last">
                  <info-card editable :data="last"></info-card>
              </v-col>
              <v-col cols="12" sm="10" md="7" class="pa-2 pt-5">
                <v-card class="pa-0 ma-0">
                  <v-card-text class="pa-0 ma-0">
                  <v-btn
                    color="purple"
                    right
                    bottom
                    :disabled="text.length < 10"
                    absolute
                    @click="queryPriceByText(text)"
                    fab>
                    <v-icon class="white-font">mdi-magnify</v-icon>
                  </v-btn>
                  <v-textarea
                      filled
                      v-model="text"
                      name="input-7-4"
                      label="账号信息"
                      placeholder="例如: 刀爹九红八红七红狗金国金考金5金黄年轮二代七夕狄仁杰锦夜游月华玫瑰云飞兰若望云14限18成衣拓印2页8白2黑11披风龙头星空炸毛·红盒唐盒貂盒3盒子资历5W6挂宠大雕霸刀脚印·新亭侯95CW"
                      auto-grow
                      hide-details
                      no-resize
                      color="indigo lighten-2"
                      background-color="rgba(255,255,255,0.9)"
                      value
                  ></v-textarea>
                  </v-card-text>
                </v-card>
              </v-col>
          </v-row>
      </v-container>
      <v-speed-dial
        v-model="fab"
        right bottom
        fixed
        fab
        direction="top"
        transition="slide-y-reverse-transition"
      >
        <template v-slot:activator>
          <v-btn
            v-model="fab"
            color="pink lighten-1"
            dark
            fab
          >
            <img v-if="!fab" src="../assets/sheep.png" width="56px" height="56px"/>
            <v-icon v-else>mdi-close</v-icon>
          </v-btn>
        </template>
        <v-btn
          color="pink"
          @click="dialog = true"
          fab>
          <v-icon class="white-font">mdi-heart</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-card>
</template>
<script>

import { mapState, mapActions, mapGetters } from "vuex"
import InfoCard from "./InfoCard.vue"

export default {
  data: () => ({
    text: "",
    fab: false,
    dialog: false,
  }),
  computed: {
    ...mapGetters(['useFullName', 'useClassicFont', 'last']),
  },
  components: {
    InfoCard,
  },
  methods: {
    ...mapActions(['queryPriceByText']),
    onFeedback() {

    }
  }
}

</script>