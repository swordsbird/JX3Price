<template>
  <v-card class="mx-auto pa-2 info-card" style="min-height: 200px;" :color="color" elevation="5">
    <v-card-text v-if="data">
      <p
        class="text-1 text--primary"
        :class="{ 'classic-font': useClassicFont }"
      >{{ data.school || '门派' }}·{{ data.body || '体型' }}</p>
      <p
        :class="{ 'classic-font': useClassicFont }"
        v-if="data.price"
      >{{Math.floor(data.price * 0.98 / 10) * 10}}~{{Math.floor(data.price * 1.02 / 10) * 10}}元</p>
      <div class="text--primary" v-if="!simple">
        <template v-for="(x, i) in data.v">
            <span
            v-if="x"
            :key="i"
            :class="{ 'classic-font': useClassicFont }"
            class="pa-1"
            >{{ rawitems[i].name }} {{ x == 1 ? '' : `× ${Math.floor(x)}` }}
            </span>
        </template>
      </div>
      <span v-if="data.time"
        class="subheading"
        :class="{ 'classic-font': useClassicFont }"
        style="position: absolute; bottom: 10px; left: 10px;"
      >
        {{ `${data.time.getMonth()}月${data.time.getDate()}日 ${data.time.toLocaleTimeString()}` }}
      </span>
      <span v-if="!simple"
        class="subheading"
        :class="{ 'classic-font': useClassicFont }"
        style="position: absolute; bottom: 10px; right: 10px;"
      >
        咩咩估价
        <span class="pl-2 text-12">http://jx3.in</span>
      </span>
    </v-card-text>

    <svg style="position: absolute; top: 20px; right: 0px; opacity: 0.2;" width="200" height="200">
      <use width="200" height="200" :xlink:href="`#${(data && data.school)}`" />
    </svg>
    <v-btn v-if="editable"
      color="indigo"
      right
      top
      absolute
      :disabled="!data.school || !data.body"
      @click="onClick()"
      fab>
      <v-icon class="white-font">mdi-pencil</v-icon>
    </v-btn>
    <v-btn v-if="analysis"
      color="success"
      right
      bottom
      absolute
      :disabled="!data.school || !data.body"
      @click="onAnalysis()"
      fab>
      <v-icon class="white-font">mdi-chart-bubble</v-icon>
    </v-btn>
  </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  data: () => ({}),
  props: {
    data: {
      type: Object
    },
    color: {
      type: String,
      default: "indigo lighten-5",
    },
    editable: {
      type: Boolean,
      default: false,
    },
    simple: {
      type: Boolean,
      default: false,
    },
    analysis: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    ...mapState(["rawitems"]),
    ...mapGetters(["useFullName", "useClassicFont",])
  },
  methods: {
    ...mapActions(["changeAccount", "addAnalysisReport"]),
    onClick() {
      this.changeAccount(this.data)
      this.$router.push('/customize')
    },
    onAnalysis() {
      this.addAnalysisReport(this.data)
    }
  }
};
</script>
<style scoped>
</style>