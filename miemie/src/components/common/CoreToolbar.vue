<template>
  <v-card color="white" height="56px" class="white" flat >
    <v-app-bar height="56px" app color="indigo lighten-2">
        <v-btn class="ml-1" icon>
          <img src="../../assets/sheep.png" width="56px" height="56px"/>
        </v-btn>
        <span class="white-font text-20 ml-3 mr-5" :class="{ 'classic-font': useClassicFont }">咩咩估价</span>
        <v-spacer/>

        <v-menu
          left
          bottom
        >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" dark text class="ml-0 hidden-md-and-up">
              {{ currentPage }}
              <v-icon>mdi-menu</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-item
              v-for="(link, i) in links"
              :key="i"
              :to="link.route"
            >
              <v-list-item-title>{{ link.text }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn
            v-for="(link, i) in links"
            :key="i"
            :to="link.route"
            class="white-font ml-0 hidden-sm-and-down"
            text
        >
            {{ link.text }}
        </v-btn>
    </v-app-bar>
  </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex"

export default {
  data: () => ({
  }),
  computed: {
    ...mapGetters(['useClassicFont', 'links']),
    currentPage(val) {
      for (let x of this.links) {
        if (this.$route.path == x.route) {
          return x.text
        }
      }
      return this.links[0].text
    }
  }
};
</script>
