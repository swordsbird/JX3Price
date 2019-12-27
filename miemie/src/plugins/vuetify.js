import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import { Touch } from 'vuetify/lib/directives'

Vue.use(Vuetify, {
  directives: {
    Touch,
  },
  icons: {
    iconfont: 'mdi',
  },
});

export default new Vuetify({
  directives: {
    Touch,
  },
  icons: {
    iconfont: 'mdi',
  },
});
