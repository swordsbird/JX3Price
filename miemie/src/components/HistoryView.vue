<template>
  <v-card class="pa-0 fill-height main-card">
  <v-container fluid>
    <v-row class="fill-width ma-0 pa-0 mb-12" justify="center">
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
        <v-col cols="12" md="9" class="pa-2" v-for="(x, i) in history" :key="i">
            <info-card :data="x" :color="colors[i % colors.length]"></info-card>
        </v-col>
    </v-row>
  </v-container>
  </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex"
import InfoCard from "./InfoCard.vue"

export default {
  data: () => ({
      group: 0,
      drawer: false,
      colors: ['grey lighten-3']
  }),
  computed: {
    ...mapState(["history"])
  },
  components: {
    InfoCard
  }
}
</script>