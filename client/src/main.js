import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';


import moment from 'moment';
import VueNumerals from 'vue-numerals';
import App from './App.vue';
import router from './router';

import SearchMain from './components/SearchMain.vue';
import Navbar from './components/Navbar.vue';

Vue.use(VueNumerals); // default locale is 'en'


Vue.prototype.moment = moment;

Vue.component('search-main', SearchMain);
Vue.component('side-menu', Navbar);
// Vue.component('line-chart', LineChart);

library.add(fas);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.use(BootstrapVue);


Vue.config.productionTip = false;


new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
