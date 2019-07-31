<template>
  <div class="container">
    <alert :message=message v-if="showMessage"></alert>
    <div class="row">
      <div class="col-lg-6">
        <div class="form-group">
          <label for="texto">Conteúdo para analise</label>
          <input type="text" v-model="texto" class="form-control">
        </div>
      </div>

      <div class="col-lg-1">
        <br>
        <button type="button" class="btn btn-primary" @click="getTweets">Buscar</button>
      </div>
    </div>

    <div class="row" v-if="tweets">
        <table class="table table-hover table-bordered">
          <thead>
            <tr>
              <td>Data</td>
              <td>Texto</td>
              <td>Usuário</td>
              <td>Positivo|Negativo</td>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tweet in tweets" v-bind:key="tweet.id">
              <td>{{tweet.tweet.created_at}}</td>
              <td>{{tweet.tweet.text}}</td>
              <td>{{tweet.tweet.user.name}}</td>
              <td align="center">
                <div class="btn-group">
                  <button class="btn btn-secondary" aria-pressed="true"
                           v-bind:class="{ 'btn-danger': tweet.sentimento == 'N' }"
                          @click="tweet.sentimento = 'N'">
                    <font-awesome-icon icon="thumbs-down" size="xs" />
                  </button>
                  <button class="btn btn-secondary" aria-pressed="true"
                          v-bind:class="{ 'btn-success': tweet.sentimento == 'P' }"
                          @click="tweet.sentimento = 'P'">
                    <font-awesome-icon icon="thumbs-up" size="xs" />
                  </button>
                </div>

              </td>
            </tr>
          </tbody>
        </table>

    </div>
    <router-link :to="{ name: 'Respostas',
                  params: { title: this.texto, tweets:this.tweets }}"
                  class="btn btn-danger"
                  v-if="tweets" >Enviar Respostas</router-link>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Coleta',
  components: {
    alert: Alert,
  },
  data() {
    return {
      texto: '',
      tweets: '',
      showMessage: false,
    };
  },
  methods: {
    getTweets() {
      const path = 'http://localhost:5000/coleta';

      const payload = {
        title: this.texto,
        tipo: this.tipo,
      };

      axios.post(path, payload)
        .then((res) => {
          // eslint-disable-next-line
          //console.log(res.data.data);
          this.tweets = res.data.data;
          this.message = res.data.message;
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
