<template>
  <v-app id="miemie">
    <CoreToolbar></CoreToolbar>
    <CoreOverlay></CoreOverlay>
    <MainView v-if="loaded"></MainView>
    <!--BottomNav/-->
    <BottomSheet></BottomSheet>
  </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex"
import BottomNav from "./components/common/BottomNav"
import BottomSheet from "./components/common/BottomSheet"
import CoreToolbar from "./components/common/CoreToolbar"
import CoreOverlay from "./components/common/CoreOverlay"
import MainView from "./components/common/MainView"

export default {
  data: () => ({
    loaded: false,
    fab: false,
  }),
  components: {
    BottomNav,
    BottomSheet,
    CoreToolbar,
    CoreOverlay,
    MainView,
  },
  async mounted() {
    await this.init()
    this.loaded = true
  },
  methods: {
    ...mapActions(['init']),
  }
};
</script>

<style>
html,
body {
  width: 100%;
}
* {
  font-family: "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB",
    "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
}
.main-card {
  background-image: url("./assets/bg4.jpg"); 
  background-position: center center; 
  background-repeat: no-repeat; 
  background-attachment: fixed;
  background-size: cover;
}
</style>