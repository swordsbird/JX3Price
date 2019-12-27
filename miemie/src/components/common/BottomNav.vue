<template>
  <!--v-card color="white" height="56px" class="white hidden-md-and-up" flat>
    <v-bottom-navigation
      v-model="bottomNav"
      class="elevation-2"
      app>
      <v-btn :value="item.title"
        v-for="item in links" :key="item.title"
        router
        height="56px"
        text
        :to="item.route">
        <span :class="{ 'classic-font': useClassicFont }">{{ item.text }}</span>
        <v-icon>{{ item.icon }}</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-card>    
  --->
  <v-speed-dial
    v-model="fab"
    left bottom
    fab
    fixed
    direction="top"
    class="hidden-md-and-up"
    transition="slide-y-reverse-transition"
  >
    <template v-slot:activator>
      <v-btn
        v-model="fab"
        color="indigo lighten-2"
        dark
        fab
      >
        <img v-if="!fab" src="../../assets/sheep.png" width="56px" height="56px"/>
        <v-icon v-else>mdi-close</v-icon>
      </v-btn>
    </template>
    <v-btn :value="item.title"
      v-for="item in links" :key="item.title"
      router
      color="indigo lighten-2"
      dark
      height="56px"
      fab
      :to="item.route">
      <v-icon>{{ item.icon }}</v-icon>
    </v-btn>
  </v-speed-dial>
</template>


<script>
  import { mapGetters } from 'vuex'

  export default {
    data () {
      return {
        fab: false,
        bottomNav: 'text',
      }
    },
    computed: {
      ...mapGetters(['useClassicFont', 'links']),
    },
  }
</script>