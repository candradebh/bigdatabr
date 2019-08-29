<template>
  <div class="container">
    <div class="row" >
      <div class="col-lg-6">
        <div class="form-group">
          <label for="texto">Texto</label>
          <input v-model="title" class="form-control" />
        </div>
      </div>
      <div class="col-lg-1">
        <br />
        <button type="button" class="btn btn-primary" @click="getTweets">Monitorar</button>
      </div>
    </div>

      <div class="row">

        <canvas id="chartjs"></canvas>

      </div>


  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NovosTweets',
  data() {
    return {
      title: '',
      qtd: '',
      showMessage: false,
      tweets: '',
      avaliou: false,
      buscou: false,
      numeros: '',
      total: '',
      indice: 0,
      num_acertos: 0,
      avaliados: 0
    };
  },
  methods: {
    avaliar(tweet, avaliacao) {
      if (avaliacao == 'acertou') {
        tweet.avaliacao = tweet.sentimento;

      } else {
        if (tweet.sentimento == 'P') {
          tweet.avaliacao = 'N';
        } else {
          tweet.avaliacao = 'P';
        }
      }

      this.getIndicadores();


    },
    getIndicadores(){
      this.avaliados = 0;
      this.num_acertos = 0;
      for (var prop in this.tweets) {
          if ( this.tweets.hasOwnProperty(prop) ) {
              //console.log(this.tweets[prop])
              if(this.tweets[prop].avaliacao != ''){
                this.avaliados++;
                if(this.tweets[prop].avaliacao == this.tweets[prop].sentimento){
                  this.num_acertos++;
                }
              }
          }
      }
      this.indice = (this.num_acertos * 100) / this.total;

    },
    getTweets() {
      const path = 'http://localhost:5000/novostweets';

      const payload = {
        title: this.title,
        qtd: this.qtd,
      };
      axios
        .post(path, payload)
        .then((res) => {
          this.tweets = JSON.parse(res.data.resultado);
          this.numeros = res.data.numeros;
          this.total = this.numeros.num_positivos + this.numeros.num_negativos;
          this.showMessage = true;
          this.buscou = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    enviarAvaliacao() {
      const path = 'http://localhost:5000/avaliacao';

      const payload = {
        title: this.title,
        tweets: this.tweets,
        avaliacao: {
          title: this.title,
          indice: this.indice,
          num_acertos: this.num_acertos,
          tam_modelo: this.numeros.tam_modelo,
        },
      };
      axios
        .post(path, payload, { ContentType: 'application/json' })
        .then((this.showMessage = true), this.$router.push('/'))
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
