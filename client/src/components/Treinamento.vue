<template>
  <div class="container">
    <h3>Modelo: {{ title }}</h3>
    <div class="row">
      <div class="col-lg-6">
        <div class="form-group">
          <label for="texto">Texto</label>
          <input v-model="title" class="form-control">
        </div>
      </div>
      <div class="col-lg-2">
        <div class="form-group">
          <label for="qtd">Quantidade</label>
          <input v-model="qtd" class="form-control">
        </div>
      </div>

      <div class="col-lg-1">
        <br>
        <button type="button" class="btn btn-primary" @click="getTweets">Buscar</button>
      </div>
    </div>

    <div class="row" v-if="tweets">
      <table class="table table-hover table-bordered table-striped">
        <thead>
          <tr>
            <td>Data</td>
            <td>Texto</td>
            <td>Usuário</td>
            <td>Sentimento</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tweet in tweets" v-bind:key="tweet">
            <td>{{tweet.title}}</td>
            <td>{{tweet.tweet}}</td>
            <td>{{tweet.sentimento}}</td>
            <td>
              <button class="btn btn-danger" @click="tweet.avaliacao = 'N'">Errou</button>
              <button class="btn btn-success" @click="tweet.avaliacao = 'P'">Acertou</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Treinamento',
  data() {
    return {
      title: '',
      qtd: '',
      showMessage: false,
      tweets: '',
    };
  },
  methods: {
    getTweets() {
      const path = 'http://localhost:5000/analisar';

      const payload = {
        title: this.title,
        qtd: this.qtd,
      };
      axios
        .post(path, payload)
        .then((res) => {
          this.tweets = JSON.parse(res.data.resultado);
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
