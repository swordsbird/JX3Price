<template>
  <v-card class="pa-0 fill-height main-card">
    <v-container fluid>
      <v-navigation-drawer v-model="drawer" fixed temporary right>
        <v-list dense rounded>
          <v-list-item
            v-for="(tg, index) in typeGroups"
            :key="`drawer${index}`"
            @click="group = index; drawer = false;"
            link
          >
            <v-list-item-content>
              <v-list-item-title>{{ tg.name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-row class="fill-width ma-0 pa-0 mb-12" justify="center">
        <v-col cols="12" md="9" class="pa-0">
          <info-card :data="current" ref="currentInfo"></info-card>
        </v-col>
        <v-col cols="12" md="9" class="pa-0 pt-3">
          <v-card
            class="fill-width ma-0 px-0 mb-12"
            color="rgba(255,255,255,0.9)"
            elevation="7">
            <v-card-title class="text-20">
              {{ typeGroups[group].name }}
              <v-btn small dark class="ml-3 mt-0" color="indigo lighten-2" @click.stop="changeFullName()" v-show="group >= 2">
                <span :class="{ 'classic-font': useClassicFont }">{{ useFullName ? '简写' : '全名' }}</span>
              </v-btn>
            </v-card-title>
            <template v-if="typeGroups[group].timeline">
              <v-timeline dense style="left: -6px">
                <v-timeline-item
                  :color="dategroup.timepoint ? 'indigo darken-2': 'indigo lighten-3'"
                  v-for="(dategroup, index) in typeGroups[group].group"
                  :key="`${dategroup.date}${typeGroups[group].name}${index}`"
                  small
                >
                  <v-row class="pa-0 ma-0">
                    <v-col cols="2" md="1" class="pa-0 ma-0">
                      <strong>{{dategroup.date}}</strong>
                    </v-col>
                    <v-col>
                      <span
                        v-for="x in dategroup.items"
                        :key="`typed${x.index}`"
                        class="pl-1 pr-1 jx3items"
                        :class="{ selected: current && current.v[x.index] > 0, 'classic-font': useClassicFont }"
                        @click="changeValueAndRefresh(x.index)"
                      >{{ useFullName ? x.fullname : x.name.replace('复刻', '') }}</span>
                    </v-col>
                  </v-row>
                </v-timeline-item>
              </v-timeline>
            </template>
            <template v-else-if="typeGroups[group].name!='统计'">
              <v-card-text v-for="type in typeGroups[group].group" :key="type.name">
                <v-row>
                  <v-col cols="12" class="d-flex justify-space-between">
                    <span
                      class="text-18"
                      :class="{ 'classic-font': useClassicFont }"
                    >{{ typeGroups[group].index != 2 || !useClassicFont ? type.name : type.name.replace(/发/g, '髮') }}</span>
                    <span
                      v-if="typeGroups[group].index > 2"
                      class="subtitle"
                      :class="{ 'classic-font': useClassicFont }"
                      @click="changeGroupValue(type.name)"
                    >全选</span>
                  </v-col>
                  <v-col cols="12" class="ma-1 pa-1">
                    <span
                      v-for="x in type.items"
                      :key="`typed${x.index}`"
                      class="pl-1 pr-0 jx3items"
                      :class="{ selected: current && current.v[x.index] > 0, 'classic-font': useClassicFont }"
                      @click="changeValueAndRefresh(x.index)"
                    >{{ useFullName ? x.fullname : x.name }}</span>
                  </v-col>
                </v-row>
              </v-card-text>
            </template>
            <template v-else>
              <v-card-text v-for="type in typeGroups[group].group" :key="type.name">
                <v-row align="center">
                  <v-col cols="11" class="ma-2 pa-1" v-for="(x, i) in type.items" :key="i">
                    <v-slider
                      color="indigo lighten-2"
                      :label="x.name"
                      :min="type.range[i][0]"
                      :max="type.range[i][1]"
                      :step="type.range[i][1] > 10000 ? 1000 : 1"
                      v-model="values[i]"
                      track-color="gray"
                      @change="changeValueToAndRefresh(x.index, values[i])"
                    >
                      <template v-slot:append>
                        <v-chip label> {{ values[i] }} </v-chip>
                      </template>
                    </v-slider>
                  </v-col>
                </v-row>
              </v-card-text>
            </template>
            <v-card-actions>
              <v-list-item class="grow">
                <v-row justify="end">
                  <v-btn
                    small
                    dark
                    color="indigo lighten-1"
                    @click.stop="changePage(-1)"
                  >
                    <span :class="{ 'classic-font': useClassicFont }">上一页</span>
                  </v-btn>
                  <v-btn
                    small
                    dark
                    color="indigo lighten-1"
                    @click.stop="changePage(1)"
                  >
                    <span :class="{ 'classic-font': useClassicFont }">下一页</span>
                  </v-btn>
                </v-row>
              </v-list-item>
            </v-card-actions>
            <v-btn
              color="purple"
              absolute
              bottom left
              :disabled="!current || !current.school || !current.body"
              @click="onSearchPrice()"
              fab>
              <v-icon class="white-font">mdi-magnify</v-icon>
            </v-btn>
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
        @click="drawer = true"
        fab>
        <v-icon class="white-font">mdi-menu-open</v-icon>
      </v-btn>
    </v-speed-dial>
  </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";
import InfoCard from "./InfoCard.vue";

export default {
  data: () => ({
    group: 0,
    fab: false,
    drawer: false,
    values: [],
  }),
  computed: {
    ...mapGetters(["typeGroups", "useFullName", "useClassicFont"]),
    ...mapState(["current"])
  },
  mounted() {
    for (let i = 0; i < 10; ++i) this.values.push(0)
  },
  components: {
    InfoCard
  },
  methods: {
    ...mapActions(["queryCurrentPrice", "changeFullName", "changeValue", "changeValueTo", "changeGroupValue"]),
    changeValueAndRefresh(index) {
      this.changeValue(index);
      this.$forceUpdate();
      this.$refs.currentInfo.$forceUpdate()
    },
    changeValueToAndRefresh(index, value) {
      this.changeValueTo({ index, value });
      this.$forceUpdate();
      this.$refs.currentInfo.$forceUpdate()
    },
    changePage(d) {
      this.group = (this.group + d + this.typeGroups.length) % this.typeGroups.length
    },
    onSearchPrice() {
      this.$vuetify.goTo(0)
      this.queryCurrentPrice()
    }
  }
};
</script>
<style scoped>
.jx3items {
  font-size: 14px;
  background: none;
  font-weight: 400;
}
.jx3items.selected {
  background: lightgray;
}
</style>