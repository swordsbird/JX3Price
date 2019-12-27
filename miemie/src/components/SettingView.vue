<template>
    <v-container fluid class="pa-0">
        <v-row class="fill-width ma-0 pa-0 mb-12" justify="center">
            <v-col cols="12" md="9" class="pa-2">
            </v-col>
        </v-row>
    </v-container>
</template>
<script>

import { mapState, mapActions, mapGetters } from "vuex"

export default {
  data: () => ({
  }),
  computed: {
    ...mapGetters(['useFullName', 'useClassicFont', 'last']),
  },
  components: {
  },
  methods: {
    ...mapActions(['queryPriceByText', 'changeQueryedAccount']),
    onClick() {
      this.changeQueryedAccount()
      this.$router.push('/customize')
    }
  }
}

</script>