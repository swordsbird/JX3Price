<template>
  <v-content id="home" class="pa-0">
    <v-slide-y-reverse-transition>
      <router-view v-show="show" />
    </v-slide-y-reverse-transition>
  </v-content>
</template>

<script>
export default {
  data: () => ({
    fab: false,
  }),
  created(){
   this.show = true
  }
}
</script>