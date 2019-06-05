import Vue from 'vue';
import Router from 'vue-router';

import Books from './components/Books.vue';
import Coleta from './components/Coleta.vue';
import Dashboard from './views/dashboard/Dashboard.vue';
import Ping from './components/Ping.vue';
import Respostas from './components/Respostas.vue';
import Treinamento from './components/Treinamento.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path: '/coleta',
      name: 'Coleta',
      component: Coleta,
    },
    {
      path: '/respostas',
      name: 'Respostas',
      component: Respostas,
      props: true,
    },
    {
      path: '/treinamento',
      name: 'Treinamento',
      component: Treinamento,
      props: true,
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
