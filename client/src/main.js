import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';


import moment from 'moment';
import VueNumerals from 'vue-numerals';
import VueChartJs from 'vue-chartjs';
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

Vue.component('stream-chart', {
  extends: VueChartJs.HorizontalBar,
  props: ['labels', 'data', 'options'],
  mounted() {
    this.renderLineChart();
  },
  computed: {
    chartData() {
      return this.data;
    },
    chartLabel() {
      return this.labels;
    },
  },
  methods: {
    renderLineChart() {
      this.renderChart(
        {
          labels: this.chartLabel,
          datasets: [
            {
              label: 'Data One',
              backgroundColor: '#f87979',
              data: this.chartData,
            },
          ],
        },
        { responsive: true, maintainAspectRatio: false },
      );
    },
  },
  watch: {
    data() {
      this._chart.destroy();
      // this.renderChart(this.data, this.options);
      this.renderLineChart();
    },
  },
});


new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
