import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import VueCharts from 'vue-chartjs';
import VueMoment from 'vue-moment';


import App from './App.vue';
import router from './router';

import SearchMain from './components/SearchMain.vue';
import Navbar from './components/Navbar.vue';
import Treinos from './views/dashboard/TreinosEfetividade.vue';


const moment = require('moment');

Vue.use(VueMoment, {
  moment,
});

Vue.component('search-main', SearchMain);
Vue.component('side-menu', Navbar);


library.add(fas);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.use(BootstrapVue);


Vue.config.productionTip = false;

Vue.use(VueCharts);
Vue.component('chartjs-line', VueCharts.Line);
Vue.component('chartjs-bar', VueCharts.Bar);
Vue.component('chartjs-radar', VueCharts.Radar);


new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
