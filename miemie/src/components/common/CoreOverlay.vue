<template>
    <v-container v-show="isLoading">
        <v-overlay overlay></v-overlay>
        <v-row class="fill-height" align-content="center" justify="center">
            <v-col
            class="subtitle-1 text-center mt-12"
            :class="{ 'classic-font': useClassicFont }"
            cols="12"
            >咩咩正在估价……</v-col>
            <v-col cols="8">
            <v-progress-linear color="indigo" indeterminate rounded height="10"></v-progress-linear>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import { mapGetters } from "vuex"
export default {
  data: () => ({
  }),
  computed: {
    ...mapGetters(['isLoading', 'useClassicFont']),
  },
}
</script>