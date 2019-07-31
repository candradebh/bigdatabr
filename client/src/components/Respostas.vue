<template>
  <div class="container">
    <h2>Tweets que você treinou</h2>
    <h3>Conteúdo: {{ title }}</h3>
    <hr>
    <button
      type="button"
      class="btn btn-primary"
      @click="enviarRespostas"
      v-if="showMessage==false" >Gravar modelo</button>
    <router-link
      :to="{ name: 'NovosTweets', params: { title: this.title }}"
      class="btn btn-danger"
      v-if="showMessage==true">Buscar novos Tweets</router-link>

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
          <tr v-for="tweet in tweets" v-bind:key="tweet.id">
            <td>{{moment(tweet.tweet.created_at).format("DD/MM/YYYY")}}</td>
            <td>{{tweet.text || tweet.tweet.full_text}}</td>
            <td>{{tweet.tweet.user.name}}</td>
            <td align="center">
              <font-awesome-icon icon="thumbs-down" color="red" size="xs" v-if="tweet.sentimento=='N'"/>
              <font-awesome-icon icon="thumbs-up" color="green" size="xs" v-if="tweet.sentimento=='P'"/>
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
  name: 'Respostas',
  props: {
    title: String,
    tweets: Array,
  },

  data() {
    return {
      showMessage: false,
    };
  },
  created() {
    if (this.title === null || this.tweets.length === 0) {
      this.$router.push('/');
    }
  },

  methods: {
    enviarRespostas() {
      const path = 'http://localhost:5000/respostas';

      const payload = {
        title: this.title,
        tweets: this.tweets,
      };
      axios
        .post(path, payload, { ContentType: 'application/json' })
        .then(
          this.showMessage = true,
        )
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
