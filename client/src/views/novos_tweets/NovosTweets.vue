<template>
  <div class="container">
    <div class="row" v-if="buscou == false">
      <div class="col-lg-6">
        <div class="form-group">
          <label for="texto">Texto</label>
          <input v-model="title" class="form-control" />
        </div>
      </div>
      <div class="col-lg-2">
        <div class="form-group">
          <label for="qtd">Quantidade</label>
          <input v-model="qtd" class="form-control" />
        </div>
      </div>

      <div class="col-lg-1">
        <br />
        <button type="button" class="btn btn-primary" @click="getTweets">Buscar</button>
      </div>
    </div>
    <div class="row" v-else>
      <div class="col-lg-4">
        <div class="card text-white bg-success mb-3" style="max-width: 18rem;">
          <div class="card-header">Positivos</div>
          <div class="card-body">
            <h5 class="card-title">{{numeros.num_positivos}} tweets</h5>
            <p class="card-text">Média de conteúdos positivos {{numeros.media_positivos}}</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4">
        <div class="card text-white bg-danger mb-3" style="max-width: 18rem;">
          <div class="card-header">Negativos</div>
          <div class="card-body">
            <h5 class="card-title">{{numeros.num_negativos}} tweets</h5>
            <p class="card-text">Média de conteúdos negativos {{numeros.media_negativos}}</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4">
        <div class="card text-white bg-info mb-3" style="max-width: 18rem;">
          <div class="card-header">Indice de Acertos</div>
          <div class="card-body">
            <h5 class="card-title">{{indice}} %</h5>
              <p class="card-text">Você avaliou {{avaliados}}
                      tweets de {{ total }} tweets no total
              </p>
          </div>
        </div>
      </div>
    </div>

    <div class="row" v-if="tweets">
      <h3>Avalie as respostas classificadas automaticamente e submeta novamente</h3>
      <table class="table table-hover table-bordered table-striped">
        <thead>
          <tr>
            <td>Data</td>
            <td>Texto</td>
            <td>sentimento</td>
            <td>Avaliar</td>
            <td>Res. Avaliação</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tweet in tweets" v-bind:key="tweet.id">
            <td>{{tweet.title}}</td>
            <td>{{tweet.tweet}}</td>
            <td>{{tweet.sentimento}}</td>
            <td>
              <div class="btn-group">
                <button
                  class="btn btn-sm btn-secondary"
                  v-bind:class="{ 'btn-danger': tweet.avaliacao != ''
                                  && tweet.avaliacao != tweet.sentimento }"
                  @click="avaliar(tweet,'errou')"
                >Errou</button>
                <button
                  class="btn btn-sm btn-secondary"
                  v-bind:class="{ 'btn-success': tweet.avaliacao != ''
                                  && tweet.avaliacao == tweet.sentimento }"
                  @click="avaliar(tweet,'acertou')"
                >Acertou</button>
              </div>
            </td>
            <td>{{tweet.avaliacao}}</td>
          </tr>
        </tbody>
      </table>
      <button
        type="button"
        class="btn btn-primary"
        @click="enviarAvaliacao"
        v-if="avaliados > 0"
      >Enviar Avaliação</button>
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
        this.num_acertos++;
      } else {
        if (tweet.sentimento == 'P') {
          tweet.avaliacao = 'N';
        } else {
          tweet.avaliacao = 'P';
        }
      }

      if (tweet.avaliacao != '') {
        this.avaliados++;
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
