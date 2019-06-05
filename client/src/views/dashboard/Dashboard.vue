<template>
  <div class="container">
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap
                  align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2">Dashboard</h1>
        <div class="btn-toolbar mb-2 mb-md-0">
          <div class="btn-group mr-2">
            <button type="button" class="btn btn-sm btn-outline-secondary">Compartilhar</button>
            <button type="button" class="btn btn-sm btn-outline-secondary">Exportar</button>
          </div>
          <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
            <span data-feather="calendar"></span>
            Nessa semana
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <h2>Positivos</h2>
          <div class="table-responsive">
            <table class="table table-striped table-sm">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Texto</th>
                  <th>Usuário</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="positivo in positivos" :key="positivo" >
                  <td>{{ positivo.tweet.created_at}} </td>
                  <td>{{ positivo.tweet.text}}</td>
                  <td>{{ positivo.tweet.user.name}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="col-md-6">
          <h2>Negativos</h2>
          <div class="table-responsive">
            <table class="table table-striped table-sm">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Texto</th>
                  <th>Usuário</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="negativo in negativos" :key="negativo" >
                  <td>{{ negativo.tweet.created_at}} </td>
                  <td>{{ negativo.tweet.text}}</td>
                  <td>{{ negativo.tweet.user.name}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      negativos: '',
      positivos: '',
    };
  },
  created() {
    this.getTweets();
  },
  methods: {
    getTweets() {
      const path = 'http://localhost:5000/dashboard';

      axios.get(path)
        .then((res) => {
          // eslint-disable-next-line
          this.negativos = JSON.parse(res.data.data.tweets_negativos);
          this.positivos = JSON.parse(res.data.data.tweets_positivos);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },


  },

};
</script>
