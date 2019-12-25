<template>
  <v-card class="pa-0 fill-height main-card">
  <v-container fluid>
    <v-row class="fill-width ma-0 pa-0 mb-12" justify="center">
      <template v-if="!showReport">
        <v-col cols="12" md="9" class="pa-2" v-if="history.length == 0">
          <v-alert
            color="indigo lighten-3 text-3"
            align="center"
            dark
            height="80px"
            prominent
          >
            还没有查询记录呢
          </v-alert>
        </v-col>
        <v-col cols="9" md="6" class="pa-2" v-for="(x, i) in history" :key="i">
            <info-card :data="x" analysis simple></info-card>
        </v-col>
      </template>
      <template v-else>
        <v-col cols="11" md="7" class="pa-2">
          <v-card class="pa-0 report-card" ref="reportview" style="min-height: 300px" v-if="report && report.userProps.length && report.userProps[0].date < new Date()">
            <v-card-title class="text-30" style="color: purple">那些年错穿的海景房</v-card-title>
            <v-card-text>
              <v-card color="rgba(255,255,255,0.5)" class="pa-2">
                <div>现在是{{currentDateString}}，从你购买第一件外观<span class="jx3-prop">{{report.userProps[0].fullname}}</span>算起，已经过去了
                {{ yearsPassed ? `${yearsPassed}年` : ''}} {{ `${daysPassed}`}} 天。</div>
                <div>{{ yearsPassed ? `${yearsPassed}年` : `${daysPassed}天`}}来，
                  你共计花了<span style="color: #EC407A;font-size: 16px;">{{report.totalPrice0}}元</span>购买外观，
                  如果你没有穿上它们，这些外观市价高达<span style="color: #EC407A;font-size: 16px;">{{report.totalPrice}}元</span>。
                  然而，因为它们穿在你的身上，你的{{report.summary.school}}{{report.summary.body}}目前价值<span style="color: #EC407A;font-size: 16px;">{{Math.floor(report.summary.price)}}元</span>，
                  你因此{{ priceDeltaPercent > 0 ? `损失了` : `赚了`}}<span style="color: #EC407A;font-size: 16px;">{{ priceDeltaPercent > 0 ? priceDeltaPercent : -priceDeltaPercent }}%</span>。
                  这些外观里，有<span style="color: #EC407A;font-size: 16px;">{{propsUpNum}}</span>件开车外观，
                  <span style="color: #EC407A;font-size: 16px;">{{propsDownNum}}</span>件翻车外观，
                  翻车指数<span style="color: #EC407A;font-size: 16px;">{{propsDownRate}}</span>，
                  超越了<span style="color: #EC407A;font-size: 16px;">
                    {{Number(Math.sqrt((100 - propsDownRate)/100)*100).toFixed(2)}}%</span>的剑三玩家。
                </div>
                <br/>
                <div><span style="color: #EC407A;font-size: 26px;">惨！</span></div>
              </v-card>
              <br/>
              <template v-for="x in propsByYear">
                <div :key="x.year"><span style="color: #BA68C8; font-size: 18px;">{{x.year}}</span>,
                {{x.props.length == 0 ? '是不幸的一年，你买的外观全部翻车。' : ''}}
                </div>
                <div v-for="(y, i) in x.props" :key="y.name">
                  {{i == 0 || y.date.getMonth() != x.props[i-1].date.getMonth() ? 
                    `${y.date.getMonth() + 1}月, ` : ''}}你穿上了江湖人称<span class="jx3-prop">{{y.name}}</span>的{{y.fullname}}
                  ，目前市价{{y.price}}元{{ i == x.props.length - 1 || y.date.getMonth() != x.props[i+1].date.getMonth() ? '。' : '；' }}
                </div>
                <template v-if="x.props2.length">
                  <div :key="`${x.year}props2`">
                    问君能有几多愁，恰似一筐翻车向东流，
                    <template v-for="k in x.props2">
                      {{k.price}}元的
                      <span class="jx3-prop" :key="k.name">{{k.name}}</span>,
                    </template>
                    欲语泪千行。
                  </div>
                </template>
              </template>
              <span 
                class="subheading"
                style="color: lightgray; position: absolute; bottom: 10px; right: 10px;"
              >
                来咩咩估价试试看！http://jx3.in
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </template>
    </v-row>
  </v-container>
      <v-speed-dial
        v-model="fab"
        left bottom
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
          @click="saveReportScreen()"
          fab>
          <v-icon class="white-font">mdi-content-save</v-icon>
        </v-btn>
        <v-btn
          color="pink"
          @click="toggleAnalysisReport()"
          fab>
          <v-icon class="white-font">mdi-backspace</v-icon>
        </v-btn>
      </v-speed-dial>
  </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex"
import InfoCard from "./InfoCard.vue"
import html2canvas from "html2canvas"

export default {
  data: () => ({
    fab: false,
  }),
  computed: {
    ...mapState(["history", "showReport", "report"]),
    currentDateString() {
      return `${new Date().getFullYear()}年${new Date().getMonth() + 1}月${new Date().getDate() + 1}日`
    },
    yearsPassed() {
      return Math.floor((new Date() - this.report.userProps[0].date) / 86400000 / 365)
    },
    daysPassed() {
      return Math.floor((new Date() - this.report.userProps[0].date) / 86400000) % 365 + 1
    },
    priceDeltaPercent() {
      return Number((this.report.totalPrice - this.report.summary.price) / this.report.totalPrice * 100).toFixed(2)
    },
    propsUpNum() {
      return this.report.userProps.filter(d => d.price != 0 && d.price >= d.price0 * 1.2).length
    },
    propsDownNum() {
      return this.report.userProps.filter(d => d.price != 0 && d.price <= d.price0 * 0.8).length
    },
    propsDownRate() {
      return Math.floor(this.propsDownNum*100/(this.propsDownNum + this.propsUpNum))
    },
    propsByYear() {
      let ret = []
      let props = this.report.userProps.filter(d => d.date != new Date('2020/12/12'))
      let others = this.report.userProps.filter(d => d.date == new Date('2020/12/12'))
      let currentYear = new Date().getFullYear()
      for (let i = props[0].date.getFullYear(); i < currentYear; ++i) {
        let t = props.filter(d => d.date.getFullYear() == i)
        ret.push({
          year: `${i}年`,
          props: t.filter(d => d.price != 0 && d.price >= d.price0 * 1.5),
          props2: t.filter(d => d.price != 0 && d.price < d.price0 * 0.8),
        })
      }
      if (others.length) {
        ret.push({
          year: '其他',
          props: others.filter(d => d.price != 0 && d.price >= d.price0 * 1.5),
          props2: others.filter(d => d.price != 0 && d.price <= d.price0 * 0.8),
        })
      }
      return ret
    }
  },
  components: {
    InfoCard
  },
  methods: {
    ...mapActions(["toggleAnalysisReport"]),
    async saveReportScreen() {
      this.$vuetify.goTo(0)
      setTimeout(() => {
        html2canvas(this.$refs.reportview.$el, { scale: 2 }).then((canvas) => {
          const imgurl = canvas.toDataURL()
          if (!imgurl) return
          const a = document.createElement('a')
          a.setAttribute('download', 'report')
          a.setAttribute('href', imgurl)
          a.setAttribute('target', '_self')
          a.click()
        })
      }, 100)
    }
  }
}
</script>
<style scoped>
.report-card {
  font-family: XinQingNian;
}
.jx3-prop {
  font-weight: 500;
  font-size: 18px;
  color: #AB47BC;
}
</style>