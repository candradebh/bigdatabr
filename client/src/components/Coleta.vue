<template>
  <div class="container">
    <alert :message=message v-if="showMessage"></alert>
    <div class="row">
      <div class="col-lg-4">
        <div class="form-group">
          <label for="texto">Texto</label>
          <input type="text" v-model="texto" class="form-control">
        </div>
      </div>
      <div class="col-lg-4">
        <div class="form-group">
          <label for="tipo">Tipo</label>
          <select id="tipo" v-model="tipo" class="form-control">
              <option value="conteudo">Conteúdo</option>
              <option value="hashtag">HashTag</option>
              <option value="usuario">Usuário</option>
          </select>
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
            <tr>Data</tr>
            <tr>Texto</tr>
            <tr>Usuário</tr>
            <tr></tr>
          </thead>
          <tbody>
            <tr v-for="tweet in tweets">
              <td>{{tweet.tweet.created_at}}</td>
              <td>{{tweet.tweet.text}}</td>
              <td>{{tweet.tweet.user.name}}</td>
              <td>
                <button class="btn btn-danger" @click="tweet.sentimento = 'N'">Negativo</button>
                <button class="btn btn-success" @click="tweet.sentimento = 'P'">Positivo</button>
              </td>
            </tr>
          </tbody>
        </table>

    </div>
    <router-link :to="{ name: 'Respostas', params: { title: this.texto, tweets:this.tweets }}" class="btn btn-danger"  v-if="tweets" >Enviar Respostas</router-link>
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
      tipo: '',
      tweets:'',
      showMessage: false,
    };
  },
  methods: {
    getTweets() {
      const path = 'http://localhost:5000/coleta';

      const payload = {
        title: this.texto,
        tipo: this.tipo
      };

      axios.post(path,payload)
        .then((res) => {
          console.log(res.data)
          this.tweets = res.data.data;
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }


  },

};
</script>
